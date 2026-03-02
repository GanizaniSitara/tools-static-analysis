# AI Tool Integration Configuration

This directory uses YAML configuration for AI tool integration settings.

## Quick Start

1. **Copy the example config:**
   ```bash
   cp config.example.yaml config.yaml
   ```

2. **Edit `config.yaml` with your settings:**
   ```bash
   nano config.yaml  # or your preferred editor
   ```

3. **Run the pipeline:**
   ```bash
   python run.py /path/to/repos output-dir
   ```

## Configuration File

- **`config.example.yaml`** - Template with all options documented (committed to git)
- **`config.yaml`** - Your local configuration (gitignored, safe for local settings)

## Key Settings

### `claudeCodePath` (string)
Path to Claude Code executable.

**Examples:**
- `claude` - Use from PATH (default)
- `/home/user/.local/bin/claude` - Absolute path
- `~/.local/bin/claude` - Home-relative path

### `githubCopilotEnabled` (boolean)
Enable GitHub Copilot CLI integration.

**Requires:** An active GitHub Copilot subscription (Pro, Pro+, Business, or Enterprise).

### `copilotMode` (string)
Which Copilot CLI to use.

- `standalone` - New standalone CLI (`npm i -g @github/copilot`) - recommended
- `gh-extension` - Legacy `gh copilot` extension (deprecated Oct 2025)

### `copilotCliPath` (string)
Path to the standalone Copilot CLI executable. Only used when `copilotMode: standalone`.

**Install:**
```bash
npm install -g @github/copilot
```

### Fix Workflow Settings

| Setting | Type | Description |
|---------|------|-------------|
| `vcsType` | string | Version control system: `svn` or `git` |
| `repoUrl` | string | Repository URL (SVN trunk or Git clone URL) |
| `svnBranchBase` | string | SVN branch base URL (SVN only) |
| `developerRoot` | string | Local root folder for checkouts |
| `fixBranchPrefix` | string | Branch name prefix for fix branches |
| `prTargetBranch` | string | Target branch for Git PRs (Git only) |
| `buildCommand` | string | Command to build the project before tests |
| `testCommand` | string | Command to run tests after a fix |
| `testTimeoutSec` | int | Build/test timeout in seconds (default: 300) |
| `autoRunTests` | boolean | Automatically run tests on fix submission |

## Configuration Examples

### Minimal (defaults)
```yaml
claudeCodePath: claude
githubCopilotEnabled: true
copilotMode: standalone
copilotCliPath: copilot
```

### With legacy Copilot extension
```yaml
githubCopilotEnabled: true
copilotMode: gh-extension
```

### Full fix workflow (Git/GitHub)
```yaml
vcsType: git
repoUrl: "git@github.com:org/eShop.git"
developerRoot: "/home/user/repos"
prTargetBranch: main
buildCommand: "dotnet build"
testCommand: "dotnet test --no-build"
testTimeoutSec: 600
autoRunTests: true
```

### Full fix workflow (SVN)
```yaml
vcsType: svn
repoUrl: "https://svn.example.com/repos/eShop/trunk"
svnBranchBase: "https://svn.example.com/repos/eShop/branches"
developerRoot: "C:\\repos"
fixBranchPrefix: "fix/smell-"
buildCommand: "dotnet build"
testCommand: "dotnet test --no-build"
testTimeoutSec: 600
autoRunTests: true
```

## Testing Your Configuration

1. **Check config loads correctly:**
   ```bash
   python3 -c "from run import CONFIG; import yaml; print(yaml.dump(CONFIG))"
   ```

2. **Test the viewer:**
   ```bash
   python run.py /path/to/repo output-test
   # Open http://localhost:8000/viewer.html
   # Click any AI tool button to test
   ```

3. **Verify button visibility:**
   - Claude button: always visible
   - Copilot button: visible when `githubCopilotEnabled: true`

## Troubleshooting

### Config not loading
- Ensure `config.yaml` exists (not just `config.example.yaml`)
- Check YAML syntax: `python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"`

### Copilot CLI not working
- Standalone mode: `copilot --version` (install: `npm i -g @github/copilot`)
- Legacy mode: `gh copilot --version` (requires `gh` CLI with copilot extension)

## Security Note

`config.yaml` is gitignored to prevent accidentally committing local paths or credentials. Always use `config.example.yaml` as the template for documentation.
