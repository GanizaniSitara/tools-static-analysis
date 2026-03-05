/**
 * companion/fix-workflow.js
 *
 * Fix lifecycle orchestrator for the companion agent.
 * Manages the full smell-to-review workflow:
 *
 *   1. Ensure code checkout (SVN or Git)
 *   2. Create a fix branch
 *   3. Launch AI tool (Claude Code, OpenCode, Copilot)
 *   4. Watch for commits / wait for developer signal
 *   5. Run tests
 *   6. Submit for review (SVN diff/patch or Git PR)
 *
 * Designed for SVN-first workflows with Git as a pluggable alternative.
 * No external dependencies - uses only Node.js built-ins.
 */

const { execSync, spawn } = require("child_process");
const fs = require("fs");
const path = require("path");
const os = require("os");

// ---------------------------------------------------------------------------
// Fix state tracker
// ---------------------------------------------------------------------------

/**
 * In-memory fix state, keyed by fix ID.
 * Persisted to .companion-fixes.json in the project root.
 *
 * States: checkout -> branching -> fixing -> review -> building -> testing -> submitting -> done
 *         Failures: failed | build_failed | test_failed
 */
const fixes = {};
let persistPath = null;

function initPersistence(projectRoot) {
  persistPath = path.join(projectRoot, ".companion-fixes.json");
  try {
    if (fs.existsSync(persistPath)) {
      const data = JSON.parse(fs.readFileSync(persistPath, "utf-8"));
      Object.assign(fixes, data);
    }
  } catch (_) {
    // Ignore corrupt file
  }
}

function persist() {
  if (!persistPath) return;
  try {
    fs.writeFileSync(persistPath, JSON.stringify(fixes, null, 2));
  } catch (_) {
    // Best-effort
  }
}

function fixId(smellType, filePath, line) {
  // Deterministic ID from smell + location
  const base = (smellType || "fix") + "-" +
    path.basename(filePath || "unknown", path.extname(filePath || "")) +
    (line ? "-L" + line : "");
  return base.replace(/[^a-zA-Z0-9_-]/g, "_").slice(0, 80);
}

function getFix(id) {
  return fixes[id] || null;
}

function setFix(id, state) {
  fixes[id] = { ...fixes[id], ...state, updatedAt: new Date().toISOString() };
  persist();
  return fixes[id];
}

function listFixes() {
  return Object.entries(fixes).map(([id, f]) => ({ id, ...f }));
}

// ---------------------------------------------------------------------------
// VCS adapters
// ---------------------------------------------------------------------------

function shellRun(cmd, opts) {
  try {
    return execSync(cmd, {
      encoding: "utf-8",
      timeout: 120000,
      stdio: ["pipe", "pipe", "pipe"],
      ...opts,
    }).trim();
  } catch (err) {
    const stderr = err.stderr ? err.stderr.toString().trim() : "";
    const stdout = err.stdout ? err.stdout.toString().trim() : "";
    throw new Error(stderr || stdout || err.message);
  }
}

// -- SVN adapter --

const svn = {
  name: "svn",

  /**
   * Ensure a working copy exists at localDir.
   * If it already exists, run svn update. Otherwise, svn checkout.
   */
  ensureCheckout(repoUrl, localDir) {
    if (fs.existsSync(path.join(localDir, ".svn"))) {
      shellRun("svn update", { cwd: localDir });
      return { action: "updated", dir: localDir };
    }
    // Create parent if needed
    const parent = path.dirname(localDir);
    if (!fs.existsSync(parent)) {
      fs.mkdirSync(parent, { recursive: true });
    }
    shellRun("svn checkout " + quote(repoUrl) + " " + quote(localDir));
    return { action: "checked_out", dir: localDir };
  },

  /**
   * Create a branch on the SVN server and switch the working copy to it.
   * branchUrl = svnBranchBase + "/" + branchName
   */
  createBranch(localDir, trunkUrl, branchUrl, branchName) {
    // Server-side copy (atomic, cheap)
    shellRun(
      "svn copy " + quote(trunkUrl) + " " + quote(branchUrl) +
      " -m " + quote("Create fix branch: " + branchName)
    );
    // Switch working copy to the branch
    shellRun("svn switch " + quote(branchUrl), { cwd: localDir });
    return { branch: branchName, url: branchUrl };
  },

  /**
   * Commit all changes in the working copy.
   */
  commit(localDir, message) {
    shellRun("svn commit -m " + quote(message), { cwd: localDir });
    return { committed: true };
  },

  /**
   * Check if there are uncommitted changes.
   */
  hasChanges(localDir) {
    const status = shellRun("svn status", { cwd: localDir });
    return status.length > 0;
  },

  /**
   * Get the current branch/URL info.
   */
  info(localDir) {
    const info = shellRun("svn info --show-item url", { cwd: localDir });
    return { url: info };
  },

  /**
   * Generate a diff/patch for review.
   */
  generatePatch(localDir) {
    return shellRun("svn diff", { cwd: localDir });
  },

  /**
   * Check for new commits on the branch since the fix started.
   */
  hasNewCommits(localDir, sinceRevision) {
    try {
      const log = shellRun(
        "svn log -r " + (parseInt(sinceRevision, 10) + 1) + ":HEAD --limit 1 -q",
        { cwd: localDir }
      );
      // svn log returns separator lines, actual commits have "r" prefix
      return /^r\d+/m.test(log);
    } catch (_) {
      return false;
    }
  },

  /**
   * Get current revision number.
   */
  revision(localDir) {
    return shellRun("svn info --show-item revision", { cwd: localDir });
  },
};

// -- Git adapter --

const git = {
  name: "git",

  ensureCheckout(repoUrl, localDir) {
    if (fs.existsSync(path.join(localDir, ".git"))) {
      shellRun("git pull --ff-only", { cwd: localDir });
      return { action: "pulled", dir: localDir };
    }
    const parent = path.dirname(localDir);
    if (!fs.existsSync(parent)) {
      fs.mkdirSync(parent, { recursive: true });
    }
    shellRun("git clone " + quote(repoUrl) + " " + quote(localDir));
    return { action: "cloned", dir: localDir };
  },

  createBranch(localDir, _trunkUrl, _branchUrl, branchName) {
    shellRun("git checkout -b " + quote(branchName), { cwd: localDir });
    return { branch: branchName };
  },

  commit(localDir, message) {
    shellRun("git add -A", { cwd: localDir });
    shellRun("git commit -m " + quote(message), { cwd: localDir });
    return { committed: true };
  },

  hasChanges(localDir) {
    const status = shellRun("git status --porcelain", { cwd: localDir });
    return status.length > 0;
  },

  info(localDir) {
    const branch = shellRun("git branch --show-current", { cwd: localDir });
    const remote = shellRun("git remote get-url origin", { cwd: localDir });
    return { branch, remote };
  },

  generatePatch(localDir) {
    return shellRun("git diff HEAD~1", { cwd: localDir });
  },

  hasNewCommits(localDir, sinceRef) {
    try {
      const count = shellRun(
        "git rev-list --count " + quote(sinceRef) + "..HEAD",
        { cwd: localDir }
      );
      return parseInt(count, 10) > 0;
    } catch (_) {
      return false;
    }
  },

  revision(localDir) {
    return shellRun("git rev-parse HEAD", { cwd: localDir });
  },

  push(localDir, branchName) {
    shellRun("git push -u origin " + quote(branchName), { cwd: localDir });
    return { pushed: true };
  },

  createPR(localDir, title, body, targetBranch) {
    const result = shellRun(
      "gh pr create --title " + quote(title) +
      " --body " + quote(body) +
      " --base " + quote(targetBranch || "main"),
      { cwd: localDir }
    );
    return { prUrl: result };
  },
};

function getVCS(type) {
  if (type === "git") return git;
  return svn;
}

/**
 * Build the shell commands a developer would need to run manually
 * for a fix, in case the automatic workflow can't execute them.
 * Returns an array of { cmd, description } objects.
 */
function buildCommands(config, branchName, localDir) {
  const vcsType = config.vcsType || "svn";
  const repoUrl = config.repoUrl || "";
  const commands = [];

  if (vcsType === "svn") {
    const svnBranchBase = (config.svnBranchBase || "").replace(/\/+$/, "");
    const branchUrl = svnBranchBase + "/" + branchName;

    // Step 1: ensure working copy
    if (!fs.existsSync(path.join(localDir, ".svn"))) {
      commands.push({
        cmd: "svn checkout " + repoUrl + " " + localDir,
        description: "Check out the repository",
      });
    } else {
      commands.push({
        cmd: "svn update",
        description: "Update working copy to latest revision",
        cwd: localDir,
      });
    }

    // Step 2: create branch on server
    commands.push({
      cmd: "svn copy " + repoUrl + " " + branchUrl +
        ' -m "Create fix branch: ' + branchName + '"',
      description: "Create fix branch (server-side copy)",
    });

    // Step 3: switch working copy to branch
    commands.push({
      cmd: "svn switch " + branchUrl,
      description: "Switch working copy to the fix branch",
      cwd: localDir,
    });
  } else {
    // Git
    if (!fs.existsSync(path.join(localDir, ".git"))) {
      commands.push({
        cmd: "git clone " + repoUrl + " " + localDir,
        description: "Clone the repository",
      });
    } else {
      commands.push({
        cmd: "git pull --ff-only",
        description: "Pull latest changes",
        cwd: localDir,
      });
    }

    commands.push({
      cmd: "git checkout -b " + branchName,
      description: "Create and switch to fix branch",
      cwd: localDir,
    });
  }

  return commands;
}

// ---------------------------------------------------------------------------
// Fix lifecycle operations
// ---------------------------------------------------------------------------

function startFix(params, config) {
  const {
    smellType, filePath, line, project, smell,
    editor,
  } = params;

  const id = fixId(smellType || smell, filePath, line);
  const vcsType = config.vcsType || "svn";
  const vcs = getVCS(vcsType);
  const devRoot = config.developerRoot || "";
  const repoUrl = config.repoUrl || "";
  const branchPrefix = config.fixBranchPrefix || "fix/smell-";
  const branchName = branchPrefix + id;

  if (!devRoot) {
    return { error: "developerRoot not configured. Set it in config.yaml." };
  }

  // Determine local checkout directory
  const repoName = repoUrl.split("/").filter(Boolean).pop() || "project";
  const localDir = path.join(devRoot, repoName);

  // Always build the manual commands so the developer can see/run them
  const commands = buildCommands(config, branchName, localDir);

  try {
    // Step 1: Ensure checkout
    setFix(id, {
      status: "checkout",
      smellType, filePath, line, project, smell,
      editor: editor || "claude",
      localDir, branchName, vcsType,
      startedAt: new Date().toISOString(),
    });

    const checkout = vcs.ensureCheckout(repoUrl, localDir);
    setFix(id, { status: "branching", checkoutAction: checkout.action });

    // Step 2: Create fix branch
    if (vcsType === "svn") {
      const svnBranchBase = config.svnBranchBase || "";
      if (!svnBranchBase) {
        setFix(id, { status: "failed", error: "svnBranchBase not configured" });
        return { error: "svnBranchBase not configured. Set it in config.yaml.", id, commands };
      }
      const trunkUrl = repoUrl;
      const branchUrl = svnBranchBase.replace(/\/+$/, "") + "/" + branchName;
      vcs.createBranch(localDir, trunkUrl, branchUrl, branchName);
    } else {
      vcs.createBranch(localDir, null, null, branchName);
    }

    // Record the starting revision for commit detection
    const startRevision = vcs.revision(localDir);
    setFix(id, {
      status: "fixing",
      startRevision,
    });

    return {
      status: "ok",
      id,
      localDir,
      branchName,
      commands,
      state: fixes[id],
    };

  } catch (err) {
    setFix(id, { status: "failed", error: err.message });
    return { error: err.message, id, commands };
  }
}

function getFixStatus(id, config) {
  const fix = getFix(id);
  if (!fix) return { error: "Fix not found: " + id };

  // If in "fixing" state, check for new commits (auto-detect)
  if (fix.status === "fixing" && fix.localDir && fix.startRevision) {
    const vcs = getVCS(fix.vcsType || config.vcsType || "svn");
    try {
      if (vcs.hasNewCommits(fix.localDir, fix.startRevision)) {
        setFix(id, { status: "review", commitDetected: true });
      }
    } catch (_) {
      // Can't check, leave status as-is
    }
  }

  return { status: "ok", id, state: fixes[id] };
}

function submitFix(id, config) {
  const fix = getFix(id);
  if (!fix) return { error: "Fix not found: " + id };
  if (fix.status !== "review" && fix.status !== "fixing") {
    return { error: "Fix is not in a submittable state: " + fix.status, state: fix };
  }

  const vcsType = fix.vcsType || config.vcsType || "svn";
  const vcs = getVCS(vcsType);
  const localDir = fix.localDir;
  const testCmd = config.testCommand || "";

  try {
    // If there are uncommitted changes, commit them first
    if (vcs.hasChanges(localDir)) {
      const msg = "Fix: " + (fix.smellType || fix.smell || "architectural smell") +
        " in " + path.basename(fix.filePath || "");
      vcs.commit(localDir, msg);
    }

    // Step 4a: Build (if configured)
    const buildCmd = config.buildCommand || "";
    const timeoutMs = (parseInt(config.testTimeoutSec, 10) || 300) * 1000;

    if (buildCmd) {
      setFix(id, { status: "building" });
      try {
        const buildOutput = shellRun(buildCmd, { cwd: localDir, timeout: timeoutMs });
        setFix(id, { buildResult: "passed", buildOutput: buildOutput.slice(-4000) });
      } catch (buildErr) {
        const errMsg = buildErr.message.slice(-4000);
        setFix(id, {
          status: "build_failed",
          buildResult: "failed",
          buildOutput: errMsg,
        });
        return {
          status: "build_failed",
          error: "Build failed",
          id,
          buildOutput: errMsg,
          state: fixes[id],
        };
      }
    }

    // Step 4b: Run tests (if configured)
    if (testCmd) {
      setFix(id, { status: "testing" });
      try {
        const testOutput = shellRun(testCmd, { cwd: localDir, timeout: timeoutMs });
        setFix(id, { testResult: "passed", testOutput: testOutput.slice(-4000) });
      } catch (testErr) {
        const errMsg = testErr.message.slice(-4000);
        setFix(id, {
          status: "test_failed",
          testResult: "failed",
          testOutput: errMsg,
        });
        return {
          status: "test_failed",
          error: "Tests failed",
          id,
          testOutput: errMsg,
          state: fixes[id],
        };
      }
    }

    // If neither build nor test configured, mark as skipped
    if (!buildCmd && !testCmd) {
      setFix(id, { testResult: "skipped", buildResult: "skipped" });
    }

    // Step 5: Submit for review
    setFix(id, { status: "submitting" });

    if (vcsType === "git") {
      // Git: push + create PR
      vcs.push(localDir, fix.branchName);
      const prTitle = "Fix: " + (fix.smellType || fix.smell || "smell") +
        " in " + path.basename(fix.filePath || "");

      const current = getFix(id);
      const buildStatus = current.buildResult === "passed"
        ? "passed (" + buildCmd + ")"
        : current.buildResult === "skipped" ? "skipped (no buildCommand)" : "N/A";
      const testStatus = current.testResult === "passed"
        ? "passed (" + testCmd + ")"
        : current.testResult === "skipped" ? "skipped (no testCommand)" : "N/A";

      const prBody = "Automated fix for architectural smell.\n\n" +
        "**Smell:** " + (fix.smell || fix.smellType || "N/A") + "\n" +
        "**File:** " + (fix.filePath || "N/A") + "\n" +
        "**Line:** " + (fix.line || "N/A") + "\n" +
        "**Project:** " + (fix.project || "N/A") + "\n\n" +
        "**Build:** " + buildStatus + "\n" +
        "**Tests:** " + testStatus;
      const prResult = vcs.createPR(
        localDir, prTitle, prBody,
        config.prTargetBranch || "main"
      );
      setFix(id, { status: "done", prUrl: prResult.prUrl });
      return { status: "ok", id, prUrl: prResult.prUrl, state: fixes[id] };
    }

    // SVN: generate patch for review
    const patch = vcs.generatePatch(localDir);
    const patchFile = path.join(localDir, "fix-" + id + ".patch");
    if (patch) {
      fs.writeFileSync(patchFile, patch);
    }
    setFix(id, { status: "done", patchFile: patch ? patchFile : null });
    return {
      status: "ok",
      id,
      patchFile: patch ? patchFile : null,
      patchSize: patch ? patch.length : 0,
      state: fixes[id],
    };

  } catch (err) {
    setFix(id, { status: "failed", error: err.message });
    return { error: err.message, id };
  }
}

// ---------------------------------------------------------------------------
// Shell quoting helper
// ---------------------------------------------------------------------------

function quote(s) {
  if (!s) return '""';
  if (os.platform() === "win32") {
    return '"' + s.replace(/"/g, '\\"') + '"';
  }
  return "'" + s.replace(/'/g, "'\\''") + "'";
}

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

module.exports = {
  initPersistence,
  fixId,
  getFix,
  setFix,
  listFixes,
  startFix,
  getFixStatus,
  submitFix,
  getVCS,
  buildCommands,
};
