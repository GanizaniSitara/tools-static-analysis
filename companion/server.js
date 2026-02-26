#!/usr/bin/env node
/**
 * companion/server.js
 *
 * Lightweight local companion agent for the hosted static-analysis viewer.
 * Runs on localhost so the browser-served viewer can request local editor launches.
 *
 * Endpoints:
 *   GET /_ping            - Health check (viewer uses this to detect the companion)
 *   GET /_open?editor=... - Launch an editor (same API as run.py)
 *
 * Usage:
 *   node companion/server.js                         # defaults: port 19280, config from ../config.yaml
 *   node companion/server.js --port 9090             # custom port
 *   node companion/server.js --config /path/to/config.yaml
 *
 * No external dependencies - uses only Node.js built-ins.
 */

const http = require("http");
const url = require("url");
const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");
const os = require("os");

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const DEFAULT_CONFIG = {
  claudePrompt:
    "Please analyze this code and propose improvements.",
  enableWslTools: false,
  wslDistro: "Ubuntu",
  wslPathPrefix: "\\\\wsl$\\Ubuntu",
  claudeCodeUseWsl: false,
  claudeCodePath: "claude",
  micromambaEnv: "",
  openCodePath: "/usr/local/bin/opencode",
  githubCopilotEnabled: false,
};

function loadConfig(configPath) {
  if (!configPath) {
    // Try config.yaml next to the companion directory (project root)
    configPath = path.resolve(__dirname, "..", "config.yaml");
  }
  if (!fs.existsSync(configPath)) {
    console.log("  No config.yaml found, using defaults.");
    return { ...DEFAULT_CONFIG };
  }
  try {
    // Simple YAML key: value parser (no dependencies needed)
    const text = fs.readFileSync(configPath, "utf-8");
    const cfg = { ...DEFAULT_CONFIG };
    for (const raw of text.split("\n")) {
      const line = raw.trim();
      if (!line || line.startsWith("#") || !line.includes(":")) continue;
      const idx = line.indexOf(":");
      const key = line.slice(0, idx).trim();
      let val = line.slice(idx + 1).trim();
      // Strip surrounding quotes
      if (
        (val.startsWith('"') && val.endsWith('"')) ||
        (val.startsWith("'") && val.endsWith("'"))
      ) {
        val = val.slice(1, -1);
      }
      // Skip multi-line indicators
      if (val === "|" || val === ">") continue;
      if (key in cfg) {
        if (val === "true") cfg[key] = true;
        else if (val === "false") cfg[key] = false;
        else cfg[key] = val;
      }
    }
    console.log("  Loaded config from " + configPath);
    return cfg;
  } catch (err) {
    console.error("  Warning: could not parse config.yaml:", err.message);
    return { ...DEFAULT_CONFIG };
  }
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function which(cmd) {
  const isWin = os.platform() === "win32";
  const envPath = process.env.PATH || "";
  const dirs = envPath.split(isWin ? ";" : ":");
  const exts = isWin ? [".exe", ".cmd", ".bat", ""] : [""];
  for (const dir of dirs) {
    for (const ext of exts) {
      const full = path.join(dir, cmd + ext);
      try {
        fs.accessSync(full, fs.constants.X_OK);
        return full;
      } catch (_) {
        // not found in this dir
      }
    }
  }
  return null;
}

function windowsToWslPath(winPath, distro) {
  // Convert C:\foo\bar to /mnt/c/foo/bar
  let p = winPath.replace(/\\/g, "/");
  const m = p.match(/^([A-Za-z]):\//);
  if (m) {
    p = "/mnt/" + m[1].toLowerCase() + "/" + p.slice(3);
  }
  return p;
}

/**
 * Walk up from filePath looking for a .sln, then .csproj.
 * Returns the directory containing the solution/project marker, or filePath's parent.
 */
function findWorkspace(filePath) {
  if (!filePath) return process.cwd();
  let dir = path.dirname(path.resolve(filePath));
  let check = dir;
  for (let i = 0; i < 20; i++) {
    try {
      const entries = fs.readdirSync(check);
      for (const ext of [".sln", ".csproj"]) {
        if (entries.some((e) => e.endsWith(ext))) return check;
      }
    } catch (_) {
      break;
    }
    const parent = path.dirname(check);
    if (parent === check) break;
    check = parent;
  }
  return dir;
}

function shellQuote(s) {
  return "'" + s.replace(/'/g, "'\\''") + "'";
}

// ---------------------------------------------------------------------------
// Editor launchers
// ---------------------------------------------------------------------------

function openVSCode(filePath, line, callback) {
  const codeExe = which("code");
  if (!codeExe) return callback("VS Code (code) not found in PATH");
  const workspace = findWorkspace(filePath);
  const args = [workspace, "--goto", filePath + ":" + (line || 1)];
  spawn(codeExe, args, { detached: true, stdio: "ignore" }).unref();
  callback(null, { status: "ok", editor: "code", workspace });
}

function openClaude(filePath, line, project, smell, config, callback) {
  const workspace = findWorkspace(filePath);
  const claudeCmd = config.claudeCodePath || "claude";

  // Build prompt
  let prompt;
  if (smell && smell.includes("\n")) {
    prompt = smell;
    if (project) prompt += "\n\nProject: " + project;
  } else {
    prompt = config.claudePrompt || "";
    if (project) prompt += "\n\nProject: " + project;
    if (smell) prompt += "\n\nArchitectural Smell:\n" + smell;
  }

  // Make path relative to workspace
  let relFile;
  try {
    relFile = path.relative(workspace, filePath);
    if (relFile.startsWith("..")) relFile = filePath;
  } catch (_) {
    relFile = filePath;
  }

  let fileRef = "@" + relFile;
  if (line) fileRef += ":" + line;

  if (config.claudeCodeUseWsl) {
    // WSL mode
    const distro = config.wslDistro || "Ubuntu";
    const wslWorkspace = windowsToWslPath(workspace, distro);
    const wslFile = windowsToWslPath(filePath, distro);

    let wslFileRef = "@" + wslFile;
    if (line) wslFileRef += ":" + line;

    let claudeArgs =
      claudeCmd +
      " --add-dir " +
      shellQuote(wslWorkspace) +
      " " +
      wslFileRef +
      " --append-system-prompt " +
      shellQuote(prompt);

    const micromambaEnv = config.micromambaEnv || "";
    let shellCmd;
    if (micromambaEnv) {
      shellCmd =
        'eval "$(micromamba shell hook --shell bash)" && micromamba activate ' +
        micromambaEnv +
        " && " +
        claudeArgs;
    } else {
      shellCmd = claudeArgs;
    }

    spawn("wsl", ["-d", distro, "--", "bash", "-c", shellCmd], {
      detached: true,
      stdio: "ignore",
    }).unref();

    return callback(null, {
      status: "ok",
      editor: "claude",
      workspace: wslWorkspace,
      mode: "wsl",
    });
  }

  // Native mode
  const isWin = os.platform() === "win32";
  if (isWin) {
    const escapedPrompt = prompt.replace(/"/g, '\\"');
    const argStr =
      "--add-dir " +
      '"' + workspace + '"' +
      " " +
      fileRef +
      ' --append-system-prompt "' +
      escapedPrompt +
      '"';
    const cmdStr = 'start "" /d "' + workspace + '" ' + claudeCmd + " " + argStr;
    spawn("cmd", ["/c", cmdStr], { detached: true, stdio: "ignore" }).unref();
    return callback(null, {
      status: "ok",
      editor: "claude",
      workspace,
      mode: "windows",
    });
  }

  // Linux/macOS native
  const args = ["--add-dir", workspace, fileRef, "--append-system-prompt", prompt];
  const terminals = [
    "x-terminal-emulator",
    "gnome-terminal",
    "konsole",
    "xfce4-terminal",
    "xterm",
  ];
  let terminal = null;
  for (const t of terminals) {
    if (which(t)) {
      terminal = t;
      break;
    }
  }

  if (terminal === "gnome-terminal") {
    spawn(terminal, ["--working-directory", workspace, "--", claudeCmd, ...args], {
      detached: true,
      stdio: "ignore",
    }).unref();
  } else if (terminal) {
    spawn(terminal, ["-e", [claudeCmd, ...args].join(" ")], {
      cwd: workspace,
      detached: true,
      stdio: "ignore",
    }).unref();
  } else {
    spawn(claudeCmd, args, {
      cwd: workspace,
      detached: true,
      stdio: "ignore",
    }).unref();
  }

  return callback(null, {
    status: "ok",
    editor: "claude",
    workspace,
    mode: "native",
  });
}

function openOpenCode(filePath, line, project, smell, config, callback) {
  if (!config.enableWslTools) {
    return callback("WSL tools are disabled in config. Set enableWslTools: true");
  }
  const workspace = findWorkspace(filePath);
  const distro = config.wslDistro || "Ubuntu";
  const opencodePath = config.openCodePath || "opencode";
  const wslWorkspace = windowsToWslPath(workspace, distro);
  const wslFile = windowsToWslPath(filePath, distro);

  let prompt = config.claudePrompt || "";
  if (smell && smell.includes("\n")) {
    prompt = smell;
    if (project) prompt += "\n\nProject: " + project;
  } else {
    if (project) prompt += "\n\nProject: " + project;
    if (smell) prompt += "\n\nArchitectural Smell:\n" + smell;
  }

  let fileRef = wslFile;
  if (line) fileRef += ":" + line;

  const shellCmd =
    opencodePath +
    " --dir " +
    shellQuote(wslWorkspace) +
    " " +
    fileRef +
    " --prompt " +
    shellQuote(prompt);

  spawn("wsl", ["-d", distro, "--", "bash", "-c", shellCmd], {
    detached: true,
    stdio: "ignore",
  }).unref();

  return callback(null, {
    status: "ok",
    editor: "opencode",
    workspace: wslWorkspace,
    mode: "wsl",
  });
}

function openCopilot(filePath, line, project, smell, config, callback) {
  if (!config.githubCopilotEnabled) {
    return callback("GitHub Copilot is not enabled in config");
  }
  if (!config.enableWslTools) {
    return callback("WSL tools are disabled in config. Set enableWslTools: true");
  }
  const workspace = findWorkspace(filePath);
  const distro = config.wslDistro || "Ubuntu";
  const wslFile = windowsToWslPath(filePath, distro);

  let context = "Analyze file " + wslFile;
  if (line) context += " at line " + line;
  if (smell) context += ". Issue: " + smell;
  if (project) context += " (Project: " + project + ")";

  const shellCmd = "gh copilot suggest -t shell " + shellQuote(context);
  spawn("wsl", ["-d", distro, "--", "bash", "-c", shellCmd], {
    detached: true,
    stdio: "ignore",
  }).unref();

  return callback(null, {
    status: "ok",
    editor: "copilot",
    mode: "wsl",
  });
}

// ---------------------------------------------------------------------------
// HTTP Server
// ---------------------------------------------------------------------------

function handleRequest(req, res, config) {
  const parsed = url.parse(req.url, true);
  const pathname = parsed.pathname;

  // CORS headers for hosted viewer
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    res.writeHead(204);
    res.end();
    return;
  }

  if (pathname === "/_ping") {
    sendJSON(res, 200, { status: "ok", agent: "tools-viewer-companion", version: "1.0.0" });
    return;
  }

  if (pathname === "/_open") {
    const q = parsed.query;
    const editor = q.editor || "";
    const filePath = q.path || "";
    const line = parseInt(q.line || "0", 10);
    const project = q.project || "";
    const smell = q.smell || "";

    if (!filePath) {
      sendJSON(res, 400, { error: "Missing path parameter" });
      return;
    }

    const done = (err, data) => {
      if (err) sendJSON(res, 500, { error: String(err) });
      else sendJSON(res, 200, data);
    };

    switch (editor) {
      case "code":
        openVSCode(filePath, line, done);
        break;
      case "claude":
        openClaude(filePath, line, project, smell, config, done);
        break;
      case "opencode":
        openOpenCode(filePath, line, project, smell, config, done);
        break;
      case "copilot":
        openCopilot(filePath, line, project, smell, config, done);
        break;
      case "studio":
        // Visual Studio requires Windows-only COM automation or devenv /edit
        // Fall back to simple devenv launch
        openVisualStudio(filePath, line, done);
        break;
      default:
        sendJSON(res, 400, { error: "Unknown editor: " + editor });
    }
    return;
  }

  sendJSON(res, 404, { error: "Not found" });
}

function openVisualStudio(filePath, line, callback) {
  if (os.platform() !== "win32") {
    return callback("Visual Studio is only supported on Windows");
  }
  const devenv = which("devenv");
  if (!devenv) {
    return callback("devenv.exe not found in PATH. Is Visual Studio installed?");
  }
  const args = ["/edit", filePath];
  if (line) args.push("/command", "Edit.GoTo " + line);
  spawn(devenv, args, { detached: true, stdio: "ignore" }).unref();
  callback(null, { status: "ok", editor: "studio" });
}

function sendJSON(res, status, data) {
  const body = JSON.stringify(data);
  res.writeHead(status, {
    "Content-Type": "application/json",
    "Content-Length": Buffer.byteLength(body),
  });
  res.end(body);
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { port: 19280, config: null };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--port" && args[i + 1]) {
      opts.port = parseInt(args[i + 1], 10);
      i++;
    } else if (args[i] === "--config" && args[i + 1]) {
      opts.config = args[i + 1];
      i++;
    } else if (args[i] === "--help" || args[i] === "-h") {
      console.log("Usage: node server.js [--port PORT] [--config PATH]");
      console.log("");
      console.log("Options:");
      console.log("  --port PORT     Listening port (default: 19280)");
      console.log("  --config PATH   Path to config.yaml (default: ../config.yaml)");
      console.log("");
      console.log("The companion agent lets the hosted viewer launch local editors.");
      console.log("Start it before opening the viewer, or when the viewer prompts you.");
      process.exit(0);
    }
  }
  return opts;
}

function main() {
  const opts = parseArgs();
  const config = loadConfig(opts.config);

  console.log("");
  console.log("Tools Viewer Companion Agent");
  console.log("============================");
  console.log("  Port:       " + opts.port);
  console.log("  Claude:     " + (config.claudeCodePath || "claude") +
    (config.claudeCodeUseWsl ? " (via WSL)" : ""));
  if (config.enableWslTools) {
    console.log("  WSL tools:  enabled (" + config.wslDistro + ")");
  }
  console.log("");
  console.log("  The hosted viewer will connect to http://localhost:" + opts.port);
  console.log("  Keep this running while using the viewer.");
  console.log("");

  const server = http.createServer((req, res) => handleRequest(req, res, config));
  server.listen(opts.port, "127.0.0.1", () => {
    console.log("  Listening on http://127.0.0.1:" + opts.port);
    console.log("  Press Ctrl+C to stop.");
    console.log("");
  });
}

main();
