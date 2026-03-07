# Demo Dataset Bootstrapper

## Overview

The `bootstrap-demo-datasets.py` script downloads curated open-source projects for static analysis demonstrations. These projects showcase real-world code patterns, architectural complexity, and common code quality issues.

## Available Datasets

### C# Datasets

1. **eShop (Microsoft)** - Reference .NET eCommerce application
   - Microservices architecture
   - ASP.NET Core, Entity Framework
   - ~50MB
   - Great for: Security analysis, async patterns, microservices complexity

2. **Orchard Core CMS** - Modular CMS framework
   - Large, complex codebase
   - Plugin system, multi-tenancy
   - ~100MB
   - Great for: Architectural analysis, god classes, circular dependencies

### Java Datasets

1. **Spring PetClinic** - Classic Spring Boot sample
   - Simple, well-structured application
   - Spring Boot 3.x, JPA, Thymeleaf
   - ~5MB
   - Great for: Spring patterns, code quality basics

2. **Ta4j** - Technical Analysis for Trading
   - Financial indicators library
   - Backtesting framework
   - ~10MB
   - Great for: Algorithm complexity, numerical code, strategy patterns

3. **Cassandre Trading Bot** - Spring Boot trading framework
   - Crypto & stock trading
   - Real-time data handling
   - ~30MB
   - Great for: Trading patterns, security in finance, Spring Boot best practices

## Quick Start

### List Available Datasets
```bash
python bootstrap-demo-datasets.py --list
```

### Download All Datasets
```bash
python bootstrap-demo-datasets.py --all
```

### Download C# Datasets Only
```bash
# All C# datasets
python bootstrap-demo-datasets.py --csharp

# Specific C# dataset
python bootstrap-demo-datasets.py --csharp eshop
```

### Download Java Datasets Only
```bash
# All Java datasets
python bootstrap-demo-datasets.py --java

# Specific Java datasets
python bootstrap-demo-datasets.py --java ta4j cassandre
```

### Download to Custom Directory
```bash
python bootstrap-demo-datasets.py --all --output ~/demo-projects
```

## Usage Examples

### Example 1: Quick Start with eShop
```bash
# Download eShop
python bootstrap-demo-datasets.py --csharp eshop

# Run analysis
python run.py --repos ~/eshop --out output-eshop

# View results
open output-eshop/docs/viewer.html
```

### Example 2: Compare C# vs Java Trading Projects
```bash
# Download trading-related projects
python bootstrap-demo-datasets.py --csharp stocksharp --java ta4j cassandre

# Analyze StockSharp (C#)
python run.py --repos ~/stocksharp --out output-stocksharp

# Analyze Ta4j (Java)
python run.py --repos ~/ta4j --out output-ta4j

# Analyze Cassandre (Java)
python run.py --repos ~/cassandre --out output-cassandre

# Compare results in viewer
```

### Example 3: Full Demo Setup
```bash
# Download everything
python bootstrap-demo-datasets.py --all --output ~/demo-datasets

# Analyze each one
python run.py --repos ~/demo-datasets/eshop --out output-eshop
python run.py --repos ~/demo-datasets/spring-petclinic --out output-petclinic
python run.py --repos ~/demo-datasets/ta4j --out output-ta4j

# Start companion for IDE integration
./companion-cli.sh start

# Start MCP server for AI analysis
python -m static_analysis_mcp.server
```

## What Gets Downloaded

Each dataset is cloned as a shallow git repository (--depth 1) to minimize download size.

**Default location:** Your home directory (`~`)

**Directory structure:**
```
~/
├── eshop/                    # Microsoft eShop (C#)
├── orchardcore/              # Orchard Core CMS (C#)
├── spring-petclinic/         # Spring PetClinic (Java)
├── stocksharp/               # StockSharp (C#)
├── ta4j/                     # Ta4j Technical Analysis (Java)
└── cassandre/                # Cassandre Trading Bot (Java)
```

## Requirements

- **Git** - For cloning repositories
- **Python 3.8+** - To run the bootstrapper
- **Disk Space** - ~350MB for all datasets

**Check requirements:**
```bash
git --version        # Should show git version
python3 --version    # Should show Python 3.8+
df -h .              # Check available disk space
```

## Why These Datasets?

### C# Projects

**eShop:**
- Official Microsoft reference application
- Real-world microservices patterns
- Common security issues (SQL injection, XSS)
- Async/await patterns
- Modern .NET Core features

**Orchard Core:**
- Large, complex codebase (~500K+ lines)
- Modular architecture
- Many contributors (diverse code styles)
- Real-world CMS complexity
- Circular dependency patterns

### Java Projects

**Spring PetClinic:**
- Official Spring sample application
- Simple, clean architecture
- Well-tested baseline
- Classic MVC pattern
- Good for learning/comparison

**Ta4j (Financial Technical Analysis):**
- Stock market indicators (RSI, MACD, etc.)
- Complex numerical algorithms
- Strategy pattern implementations
- Time series data handling
- Perfect for analyzing algorithm complexity

**Cassandre Trading Bot:**
- Spring Boot + WebSocket real-time data
- Cryptocurrency & stock trading
- Database integration for orders/trades
- Security-critical financial logic
- Exception handling in trading scenarios

## Analysis Focus

### Security Analysis
Best datasets:
- **eShop** - SQL injection, XSS, authentication issues
- **Cassandre** - Financial security, API key handling

### Architectural Analysis
Best datasets:
- **Orchard Core** - Large modular system, circular dependencies
- **eShop** - Microservices complexity

### Algorithm Complexity
Best datasets:
- **Ta4j** - Financial indicators, backtesting algorithms
- **StockSharp** - Trading algorithms, event processing

### Code Quality
Best datasets:
- **All** - Each has unique quality issues to discover

## Troubleshooting

### "Git not found"
```bash
# Ubuntu/Debian
sudo apt install git

# macOS
brew install git

# Verify
git --version
```

### "Permission denied"
```bash
# Make script executable
chmod +x bootstrap-demo-datasets.py
```

### "Repository already exists"
The script will ask if you want to update the existing repository.
```
[WARN] eShop already exists at /home/user/eshop
  Update existing repository? (y/n): y
```

### Low disk space
The script checks for 500MB free space. If you're low:
```bash
# Check space
df -h .

# Download only what you need
python bootstrap-demo-datasets.py --csharp eshop --java ta4j
```

### Clone failed
Check internet connection and GitHub access:
```bash
# Test GitHub connectivity
git ls-remote https://github.com/dotnet/eShop.git HEAD

# Use HTTPS instead of SSH if needed (script uses HTTPS by default)
```

## Command Reference

```bash
# List all available datasets
python bootstrap-demo-datasets.py --list

# Download everything
python bootstrap-demo-datasets.py --all

# Download only C# projects
python bootstrap-demo-datasets.py --csharp

# Download specific C# project
python bootstrap-demo-datasets.py --csharp eshop

# Download only Java projects
python bootstrap-demo-datasets.py --java

# Download specific Java projects
python bootstrap-demo-datasets.py --java ta4j cassandre

# Download to custom directory
python bootstrap-demo-datasets.py --all --output ~/my-demos

# Show help
python bootstrap-demo-datasets.py --help
```

## After Download

### Run Analysis

```bash
# Basic analysis
python run.py --repos ~/eshop --out output-eshop

# With external tools (semgrep, bandit)
python run.py --repos ~/eshop --out output-eshop --tools all

# Analysis with specific level
python run.py --repos ~/ta4j --out output-ta4j --level high
```

### View Results

```bash
# Start companion server
./companion-cli.sh start

# Open viewer
open output-eshop/docs/viewer.html

# Or start MCP server for AI-powered analysis
python -m static_analysis_mcp.server
```

## Dataset Sizes

| Dataset | Language | Size | Download Time (10Mbps) |
|---------|----------|------|------------------------|
| Spring PetClinic | Java | ~5MB | <1 min |
| Ta4j | Java | ~10MB | ~1 min |
| Cassandre | Java | ~30MB | ~3 min |
| eShop | C# | ~50MB | ~5 min |
| Orchard Core | C# | ~100MB | ~10 min |
| StockSharp | C# | ~150MB | ~15 min |
| **Total** | - | **~345MB** | **~35 min** |

## Next Steps

1. **Download datasets:**
   ```bash
   python bootstrap-demo-datasets.py --all
   ```

2. **Run analysis:**
   ```bash
   python run.py --repos ~/eshop --out output-eshop
   python run.py --repos ~/ta4j --out output-ta4j
   ```

3. **Start companion:**
   ```bash
   ./companion-cli.sh start
   ```

4. **View results:**
   ```bash
   open output-eshop/docs/viewer.html
   open output-ta4j/docs/viewer.html
   ```

5. **Use MCP server:**
   ```bash
   python -m static_analysis_mcp.server
   ```

## Summary

The bootstrapper makes it easy to download curated demo projects for:
- Testing the static analysis pipeline
- Demonstrating different code quality issues
- Comparing C# vs Java patterns
- Training on real-world codebases
- Showcasing security vulnerabilities

All projects are open-source, actively maintained, and represent real-world complexity.

---

**Ready to analyze real code!**
