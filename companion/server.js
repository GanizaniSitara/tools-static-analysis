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
const fixWorkflow = require("./fix-workflow");

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const DEFAULT_CONFIG = {
  claudePrompt:
    "Please analyze this code and propose improvements.",
  claudeCodePath: "claude",
  githubCopilotEnabled: true,
  copilotMode: "standalone",
  copilotCliPath: "copilot",
  copilotModel: "claude-opus-4.6",
  // Fix workflow
  vcsType: "svn",
  repoUrl: "",
  svnBranchBase: "",
  developerRoot: "",
  fixBranchPrefix: "fix/smell-",
  prTargetBranch: "main",
  testCommand: "",
  autoRunTests: true,
  buildCommand: "",
  testTimeoutSec: "300",
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

  // Make path relative to workspace for mention in prompt
  let relFile;
  try {
    relFile = path.relative(workspace, filePath);
    if (relFile.startsWith("..")) relFile = filePath;
  } catch (_) {
    relFile = filePath;
  }

  // File reference for mention in prompt (@file:line)
  let fileMention = "@" + relFile;
  if (line) fileMention += ":" + line;

  // Full file path for opening (absolute path)
  const fileToOpen = filePath;

  // Add file mention to prompt so Claude knows which file to focus on
  const fullPrompt = prompt + "\n\nPlease focus on: " + fileMention;

  const isWin = os.platform() === "win32";
  if (isWin) {
    const escapedPrompt = fullPrompt.replace(/"/g, '\\"');
    const argStr =
      "--add-dir " +
      '"' + workspace + '"' +
      " " +
      '"' + fileToOpen + '"' +
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

  // Linux/macOS native - pass absolute file path and add-dir for workspace
  const args = ["--add-dir", workspace, fileToOpen, "--append-system-prompt", fullPrompt];
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

/**
 * Launch a TUI application in a real terminal window.
 *
 * On Windows: uses Windows Terminal (wt.exe) if available, falls back to
 * cmd /c start which opens a conhost console.  Both give the TUI app a
 * proper PTY so it can draw its UI.
 *
 * On Linux/macOS: tries well-known terminal emulators in preference order.
 */
function launchInTerminal(shellCmd, targetDir, config) {
  const isWin = os.platform() === "win32";

  if (isWin) {
    // Prefer Windows Terminal (wt.exe) for proper PTY support
    if (which("wt")) {
      spawn("wt", ["cmd", "/k", "cd /d \"" + targetDir + "\" && " + shellCmd], {
        detached: true, stdio: "ignore",
      }).unref();
    } else {
      const cmdStr = 'start "" cmd /k "cd /d \\"' + targetDir + '\\" && ' + shellCmd + '"';
      spawn("cmd", ["/c", cmdStr], {
        detached: true, stdio: "ignore",
      }).unref();
    }
    return;
  }

  // Native Linux/macOS
  const terminals = [
    "x-terminal-emulator",
    "gnome-terminal",
    "konsole",
    "xfce4-terminal",
    "alacritty",
    "kitty",
    "xterm",
  ];
  let terminal = null;
  for (const t of terminals) {
    if (which(t)) { terminal = t; break; }
  }

  if (terminal === "gnome-terminal") {
    spawn(terminal, ["--working-directory", targetDir, "--", "bash", "-lc", shellCmd], {
      detached: true, stdio: "ignore",
    }).unref();
  } else if (terminal === "alacritty" || terminal === "kitty") {
    // Modern GPU-accelerated terminals
    spawn(terminal, ["--working-directory", targetDir, "-e", "bash", "-lc", shellCmd], {
      detached: true, stdio: "ignore",
    }).unref();
  } else if (terminal) {
    spawn(terminal, ["-e", "bash -lc " + shellQuote(shellCmd)], {
      cwd: targetDir, detached: true, stdio: "ignore",
    }).unref();
  } else {
    // No terminal emulator found - run headless (works for non-interactive -p mode)
    spawn("bash", ["-lc", shellCmd], {
      cwd: targetDir, detached: true, stdio: "ignore",
    }).unref();
  }
}

function openCopilot(filePath, line, project, smell, config, callback) {
  if (!config.githubCopilotEnabled) {
    return callback("GitHub Copilot is not enabled in config. Set githubCopilotEnabled: true");
  }
  const workspace = findWorkspace(filePath);
  const isWin = os.platform() === "win32";
  const mode = config.copilotMode || "standalone";
  const copilotPath = config.copilotCliPath || "copilot";
  const copilotModel = config.copilotModel || "claude-opus-4.6";

  if (mode === "gh-extension") {
    // Legacy gh copilot extension -- limited flags, just pass context
    let context = "Analyze file " + filePath;
    if (line) context += " at line " + line;
    if (smell) context += ". Issue: " + smell;
    if (project) context += " (Project: " + project + ")";

    if (isWin) {
      const winCmd = 'cd /d "' + workspace + '" && gh copilot suggest -t shell "' + context.replace(/"/g, '\\"') + '"';
      if (which("wt")) {
        spawn("wt", ["cmd", "/k", winCmd], { detached: true, stdio: "ignore" }).unref();
      } else {
        spawn("cmd", ["/c", 'start "" cmd /k ' + winCmd], { detached: true, stdio: "ignore" }).unref();
      }
    } else {
      const shellCmd = "cd " + shellQuote(workspace) + " && " +
        "gh copilot suggest -t shell " + shellQuote(context);
      launchInTerminal(shellCmd, workspace, config);
    }
    return callback(null, {
      status: "ok", editor: "copilot", workspace: workspace,
      mode: isWin ? "windows" : "native", copilotMode: mode,
    });
  }

  // Standalone mode: use -i (interactive + execute prompt) instead of -p (exits)
  // Build prompt using same claudePrompt config that Claude Code uses, since
  // Copilot CLI has no --system-prompt flag (instructions are baked into the prompt).

  // Make path relative to workspace
  let relFile;
  try {
    relFile = path.relative(workspace, filePath);
    if (relFile.startsWith("..")) relFile = filePath;
  } catch (_) {
    relFile = filePath;
  }

  let prompt;
  if (smell && smell.includes("\n")) {
    // Focused smell prompt (pre-built by the viewer) -- use as-is, same as Claude
    prompt = smell;
    if (project) prompt += "\n\nProject: " + project;
  } else {
    // Generic prompt from config -- same structure Claude receives
    prompt = config.claudePrompt || "You are analyzing a C# .NET project with architectural smells.\nPlease propose a refactoring solution that:\n- Addresses the specific smell identified\n- Maintains existing functionality\n- Follows SOLID principles and .NET best practices\n- Considers the broader architectural context";
    if (project) prompt += "\n\nProject: " + project;
    if (smell) prompt += "\n\nArchitectural Smell:\n" + smell;
  }
  prompt += "\n\nFile: " + relFile;
  if (line) prompt += " (line " + line + ")";
  prompt += "\n\nPlease read the file above and propose concrete code changes to address the issue.";

  if (isWin) {
    const escapedPrompt = prompt.replace(/"/g, '\\"');
    const winCmd = 'cd /d "' + workspace + '" && ' + copilotPath +
      " --model " + copilotModel +
      " --add-dir " + '"' + workspace + '"' +
      ' -i "' + escapedPrompt + '"';
    if (which("wt")) {
      spawn("wt", ["cmd", "/k", winCmd], { detached: true, stdio: "ignore" }).unref();
    } else {
      spawn("cmd", ["/c", 'start "" cmd /k ' + winCmd], { detached: true, stdio: "ignore" }).unref();
    }
  } else {
    const shellCmd = copilotPath +
      " --model " + copilotModel +
      " --add-dir " + shellQuote(workspace) +
      " -i " + shellQuote(prompt);
    launchInTerminal(shellCmd, workspace, config);
  }

  return callback(null, {
    status: "ok", editor: "copilot", workspace: workspace,
    mode: isWin ? "windows" : "native", copilotMode: mode,
    model: copilotModel,
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

  // ---- Pre-flight check endpoint ----

  if (pathname === "/_check") {
    const tools = {};
    const copilotPath = config.copilotCliPath || "copilot";

    if (config.githubCopilotEnabled) {
      tools.copilot = config.copilotMode === "gh-extension"
        ? !!which("gh")
        : !!which(copilotPath);
    }

    sendJSON(res, 200, {
      status: "ok",
      platform: os.platform(),
      tools,
      config: {
        githubCopilotEnabled: config.githubCopilotEnabled,
        copilotMode: config.copilotMode,
        copilotCliPath: config.copilotCliPath,
      },
    });
    return;
  }

  // ---- Fix workflow endpoints ----

  if (pathname === "/_fix/start") {
    const q = parsed.query;
    const result = fixWorkflow.startFix({
      smellType: q.smell_type || "",
      filePath: q.path || "",
      line: parseInt(q.line || "0", 10),
      project: q.project || "",
      smell: q.smell || "",
      editor: q.editor || "claude",
    }, config);

    if (result.error) {
      sendJSON(res, 400, result);
      return;
    }

    // After branching, launch the chosen editor in the fix working copy
    const fix = result.state;
    const fixDir = fix.localDir;
    const fixFile = path.join(fixDir, path.basename(fix.filePath || ""));
    const done = (err, data) => {
      if (err) {
        result.editorError = String(err);
      } else {
        result.editorLaunch = data;
      }
      sendJSON(res, 200, result);
    };

    const editor = fix.editor || "claude";
    switch (editor) {
      case "claude":
        openClaude(fixFile, fix.line, fix.project, fix.smell, config, done);
        break;
      case "copilot":
        openCopilot(fixFile, fix.line, fix.project, fix.smell, config, done);
        break;
      case "code":
        openVSCode(fixFile, fix.line, done);
        break;
      default:
        sendJSON(res, 200, result);
    }
    return;
  }

  if (pathname === "/_fix/status") {
    const q = parsed.query;
    const id = q.id || "";
    if (!id) {
      sendJSON(res, 400, { error: "Missing id parameter" });
      return;
    }
    const result = fixWorkflow.getFixStatus(id, config);
    sendJSON(res, result.error ? 404 : 200, result);
    return;
  }

  if (pathname === "/_fix/submit") {
    const q = parsed.query;
    const id = q.id || "";
    if (!id) {
      sendJSON(res, 400, { error: "Missing id parameter" });
      return;
    }
    const result = fixWorkflow.submitFix(id, config);
    sendJSON(res, result.error ? 400 : 200, result);
    return;
  }

  if (pathname === "/_fix/list") {
    sendJSON(res, 200, { fixes: fixWorkflow.listFixes() });
    return;
  }

  // ---- Editor launch endpoints ----

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

  // Initialize fix workflow state persistence
  fixWorkflow.initPersistence(path.resolve(__dirname, ".."));

  console.log("");
  console.log("Tools Viewer Companion Agent");
  console.log("============================");
  console.log("  Port:       " + opts.port);
  console.log("  Claude:     " + (config.claudeCodePath || "claude"));
  if (config.githubCopilotEnabled) {
    const cMode = config.copilotMode || "standalone";
    console.log("  Copilot:    " +
      (cMode === "gh-extension"
        ? "gh copilot (legacy extension)"
        : (config.copilotCliPath || "copilot") + " (standalone CLI)"));
  }
  if (config.developerRoot) {
    console.log("  Fix workflow:");
    console.log("    VCS:       " + (config.vcsType || "svn"));
    console.log("    Dev root:  " + config.developerRoot);
    if (config.repoUrl) console.log("    Repo URL:  " + config.repoUrl);
    if (config.testCommand) console.log("    Tests:     " + config.testCommand);
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
