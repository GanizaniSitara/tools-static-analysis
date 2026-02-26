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

### `enableWslTools` (boolean)
Master toggle for WSL integration. When `true`, AI tools run via WSL instead of Windows native.

**Examples:**
- `false` - Use Windows native tools (default)
- `true` - Use WSL for all AI tools

### `claudeCodePath` (string)
Path to Claude Code executable in WSL.

**Examples:**
- `claude` - Use from PATH
- `/home/user/.local/bin/claude` - Absolute path
- `~/.local/bin/claude` - Home-relative path

### `micromambaEnv` (string)
Micromamba/conda environment name to activate before running Claude Code.

**Examples:**
- `""` - No environment activation (default)
- `ai-tools` - Activate the `ai-tools` environment
- `python311` - Activate the `python311` environment

### `openCodePath` (string)
Path to OpenCode executable (in WSL or native Linux).

**Examples:**
- `opencode` - Use from PATH
- `/usr/local/bin/opencode` - Absolute path

### `openCodeNonInteractive` (boolean)
Launch mode for OpenCode.

- `false` - TUI mode (opens interactive terminal UI) - default
- `true` - Non-interactive mode (uses `opencode -p "<prompt>"`)

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

## Configuration Modes

### Mode 1: Windows Only
```yaml
enableWslTools: false
claudeCodePath: claude  # Uses Windows claude.exe
```

### Mode 2: WSL with Default Environment
```yaml
enableWslTools: true
wslDistro: Ubuntu-24.04
claudeCodePath: claude
micromambaEnv: ""  # No conda environment
```

### Mode 3: WSL with Micromamba Environment
```yaml
enableWslTools: true
wslDistro: Ubuntu
claudeCodePath: /home/user/.local/bin/claude
micromambaEnv: ai-tools  # Activates conda environment
```

### Mode 4: WSL with All AI Tools
```yaml
enableWslTools: true
wslDistro: Ubuntu-24.04
claudeCodePath: claude
openCodePath: opencode
openCodeNonInteractive: false
githubCopilotEnabled: true
copilotMode: standalone
copilotCliPath: copilot
```

### Mode 5: Native Linux (companion runs inside WSL directly)
```yaml
enableWslTools: true      # Still needed to show buttons in viewer
claudeCodeUseWsl: false
openCodePath: opencode
githubCopilotEnabled: true
copilotMode: standalone
copilotCliPath: copilot
# The companion auto-detects Linux and runs tools directly (no wsl -d wrapper)
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
   - When `enableWslTools: false` → See 4 buttons (Studio, Code, Claude, View)
   - When `enableWslTools: true` → See 6 buttons (+ OpenCode, Copilot)

## Troubleshooting

### Config not loading
- Ensure `config.yaml` exists (not just `config.example.yaml`)
- Check YAML syntax: `python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"`

### WSL tools not working
- Verify WSL distro name: `wsl -l -v`
- Check tool paths: `wsl -d Ubuntu-24.04 -- which claude`
- Test path conversion: `wsl -d Ubuntu-24.04 -- wslpath -u 'C:\path'`
- Check OpenCode: `wsl -d Ubuntu-24.04 -- opencode --version`
- Check Copilot CLI: `wsl -d Ubuntu-24.04 -- copilot --version`
- For legacy Copilot: `wsl -d Ubuntu-24.04 -- gh copilot --version`

### Micromamba not activating
- Ensure micromamba is installed: `wsl -d Ubuntu-24.04 -- micromamba --version`
- Check environment exists: `wsl -d Ubuntu-24.04 -- micromamba env list`
- Test activation: `wsl -d Ubuntu-24.04 -- bash -c 'eval "$(micromamba shell hook --shell bash)" && micromamba activate myenv && which python'`

## Security Note

`config.yaml` is gitignored to prevent accidentally committing local paths or credentials. Always use `config.example.yaml` as the template for documentation.
