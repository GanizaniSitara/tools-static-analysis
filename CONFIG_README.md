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
Path to OpenCode executable in WSL.

### `githubCopilotEnabled` (boolean)
Enable GitHub Copilot CLI integration via WSL.

**Requires:** `gh copilot` extension installed
```bash
gh extension install github/gh-copilot
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

### Micromamba not activating
- Ensure micromamba is installed: `wsl -d Ubuntu-24.04 -- micromamba --version`
- Check environment exists: `wsl -d Ubuntu-24.04 -- micromamba env list`
- Test activation: `wsl -d Ubuntu-24.04 -- bash -c 'eval "$(micromamba shell hook --shell bash)" && micromamba activate myenv && which python'`

## Security Note

`config.yaml` is gitignored to prevent accidentally committing local paths or credentials. Always use `config.example.yaml` as the template for documentation.
