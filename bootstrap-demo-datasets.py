#!/usr/bin/env python3
"""
Bootstrap Demo Datasets

Downloads sample C# and Java projects for static analysis demonstrations.
These are open-source projects that showcase different architectural patterns
and code quality issues.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Any

# ANSI colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'


def print_success(msg: str):
    print(f"{GREEN}✓{RESET} {msg}")


def print_info(msg: str):
    print(f"{BLUE}ℹ{RESET} {msg}")


def print_warning(msg: str):
    print(f"{YELLOW}⚠{RESET} {msg}")


def print_error(msg: str):
    print(f"{RED}✗{RESET} {msg}")


def print_header(msg: str):
    print()
    print("=" * 70)
    print(f"  {BOLD}{msg}{RESET}")
    print("=" * 70)
    print()


# Dataset definitions
DATASETS = {
    "csharp": {
        "eshop": {
            "name": "eShop (Microsoft)",
            "description": "Reference .NET application - eCommerce with microservices",
            "url": "https://github.com/dotnet/eShop.git",
            "branch": "main",
            "language": "C#",
            "size": "~50MB",
            "features": [
                "Microservices architecture",
                "ASP.NET Core",
                "Entity Framework",
                "Docker support",
                "Real-world patterns"
            ],
            "analysis_targets": [
                "Security vulnerabilities (SQL injection, XSS)",
                "Exception handling issues",
                "Async/await patterns",
                "Dependency complexity",
                "Code quality metrics"
            ]
        },
        "orchardcore": {
            "name": "Orchard Core CMS",
            "description": "Modular ASP.NET Core CMS framework",
            "url": "https://github.com/OrchardCMS/OrchardCore.git",
            "branch": "main",
            "language": "C#",
            "size": "~100MB",
            "features": [
                "Modular architecture",
                "CMS platform",
                "Plugin system",
                "Multi-tenancy",
                "Large codebase"
            ],
            "analysis_targets": [
                "Architectural complexity",
                "God classes/methods",
                "Deep nesting",
                "Circular dependencies",
                "Module coupling"
            ]
        }
    },
    "java": {
        "spring-petclinic": {
            "name": "Spring PetClinic",
            "description": "Classic Spring Boot sample application",
            "url": "https://github.com/spring-projects/spring-petclinic.git",
            "branch": "main",
            "language": "Java",
            "size": "~5MB",
            "features": [
                "Spring Boot 3.x",
                "Spring Data JPA",
                "Thymeleaf templates",
                "MySQL/H2 database",
                "Simple architecture"
            ],
            "analysis_targets": [
                "Spring framework patterns",
                "JPA usage",
                "Exception handling",
                "Code quality",
                "Test coverage"
            ]
        },
        "stocksharp": {
            "name": "StockSharp (Trading Platform)",
            "description": "Open-source algorithmic trading platform (C# but we'll use Java alternative)",
            "url": "https://github.com/StockSharp/StockSharp.git",
            "branch": "master",
            "language": "C#",
            "size": "~150MB",
            "features": [
                "Real-time trading",
                "Market data analysis",
                "Complex algorithms",
                "Event-driven architecture",
                "Financial calculations"
            ],
            "analysis_targets": [
                "Complex algorithms",
                "Thread safety issues",
                "Performance patterns",
                "Data flow analysis",
                "Security in trading logic"
            ]
        },
        "ta4j": {
            "name": "Ta4j (Technical Analysis)",
            "description": "Java library for technical analysis in trading",
            "url": "https://github.com/ta4j/ta4j.git",
            "branch": "master",
            "language": "Java",
            "size": "~10MB",
            "features": [
                "Trading indicators",
                "Backtesting framework",
                "Strategy analysis",
                "Time series data",
                "Financial calculations"
            ],
            "analysis_targets": [
                "Algorithm complexity",
                "Numerical precision",
                "Strategy patterns",
                "Code quality",
                "API design"
            ]
        },
        "cassandre": {
            "name": "Cassandre Trading Bot",
            "description": "Spring Boot trading bot framework for crypto/stocks",
            "url": "https://github.com/cassandre-tech/cassandre-trading-bot.git",
            "branch": "development",
            "language": "Java",
            "size": "~30MB",
            "features": [
                "Spring Boot trading bot",
                "Crypto & stock trading",
                "Strategy framework",
                "WebSocket real-time data",
                "Database integration"
            ],
            "analysis_targets": [
                "Trading strategy patterns",
                "Real-time data handling",
                "Exception handling in trading",
                "Security in financial apps",
                "Spring Boot best practices"
            ]
        }
    }
}


def check_git_installed() -> bool:
    """Check if git is installed."""
    try:
        subprocess.run(
            ["git", "--version"],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_disk_space(required_mb: int = 500) -> bool:
    """Check if enough disk space available."""
    try:
        import shutil
        stat = shutil.disk_usage(".")
        available_mb = stat.free / (1024 * 1024)
        return available_mb > required_mb
    except Exception:
        return True  # Assume OK if can't check


def clone_repository(name: str, url: str, branch: str, target_dir: Path) -> bool:
    """Clone a git repository."""
    try:
        if target_dir.exists():
            print_warning(f"{name} already exists at {target_dir}")

            # Ask user if they want to update
            response = input(f"  Update existing repository? (y/n): ").lower().strip()
            if response == 'y':
                print_info(f"Updating {name}...")
                subprocess.run(
                    ["git", "pull"],
                    cwd=target_dir,
                    capture_output=True,
                    check=True
                )
                print_success(f"Updated {name}")
                return True
            else:
                print_info(f"Skipping {name}")
                return True

        print_info(f"Cloning {name} from {url}...")
        print_info(f"Target: {target_dir}")
        print_info(f"Branch: {branch}")

        subprocess.run(
            ["git", "clone", "--depth", "1", "--branch", branch, url, str(target_dir)],
            check=True,
            capture_output=True
        )

        print_success(f"Cloned {name}")
        return True

    except subprocess.CalledProcessError as e:
        print_error(f"Failed to clone {name}: {e.stderr.decode() if e.stderr else str(e)}")
        return False


def show_dataset_info(datasets: Dict[str, Any], language: str):
    """Show information about available datasets."""
    print_header(f"{language.upper()} Demo Datasets")

    for key, data in datasets.items():
        print(f"{BOLD}{data['name']}{RESET}")
        print(f"  Description: {data['description']}")
        print(f"  Language: {data['language']}")
        print(f"  Size: {data['size']}")
        print(f"  URL: {data['url']}")
        print()

        print(f"  {BOLD}Features:{RESET}")
        for feature in data['features']:
            print(f"    • {feature}")
        print()

        print(f"  {BOLD}Analysis Targets:{RESET}")
        for target in data['analysis_targets']:
            print(f"    • {target}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Bootstrap demo datasets for static analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all datasets
  python bootstrap-demo-datasets.py --all

  # Download only C# datasets
  python bootstrap-demo-datasets.py --csharp

  # Download specific datasets
  python bootstrap-demo-datasets.py --csharp eshop --java cassandre

  # List available datasets
  python bootstrap-demo-datasets.py --list

  # Download to custom directory
  python bootstrap-demo-datasets.py --all --output ~/demo-projects
        """
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Download all demo datasets"
    )

    parser.add_argument(
        "--csharp",
        nargs="*",
        metavar="DATASET",
        help="Download C# datasets (eshop, orchardcore, or all if no args)"
    )

    parser.add_argument(
        "--java",
        nargs="*",
        metavar="DATASET",
        help="Download Java datasets (spring-petclinic, ta4j, cassandre, or all if no args)"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List available datasets and exit"
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path.home(),
        help="Output directory (default: %(default)s)"
    )

    args = parser.parse_args()

    # Show help if no arguments
    if len(sys.argv) == 1:
        parser.print_help()
        print()
        print_info("Use --list to see available datasets")
        return 0

    # List datasets and exit
    if args.list:
        show_dataset_info(DATASETS["csharp"], "C#")
        show_dataset_info(DATASETS["java"], "Java")
        return 0

    # Pre-flight checks
    print_header("Pre-flight Checks")

    if not check_git_installed():
        print_error("Git is not installed")
        print_info("Install: sudo apt install git  (Ubuntu/Debian)")
        print_info("Install: brew install git       (macOS)")
        return 1
    print_success("Git is installed")

    if not check_disk_space():
        print_warning("Low disk space (< 500MB available)")
        response = input("Continue anyway? (y/n): ").lower().strip()
        if response != 'y':
            return 1
    print_success("Sufficient disk space")

    # Create output directory
    output_dir = args.output
    output_dir.mkdir(parents=True, exist_ok=True)
    print_success(f"Output directory: {output_dir}")

    # Determine what to download
    to_download = []

    if args.all:
        # Download everything
        for lang_key, lang_datasets in DATASETS.items():
            for dataset_key, dataset_info in lang_datasets.items():
                to_download.append((lang_key, dataset_key, dataset_info))
    else:
        # Download specified datasets
        if args.csharp is not None:
            if len(args.csharp) == 0:
                # All C# datasets
                for dataset_key, dataset_info in DATASETS["csharp"].items():
                    to_download.append(("csharp", dataset_key, dataset_info))
            else:
                # Specific C# datasets
                for dataset_key in args.csharp:
                    if dataset_key in DATASETS["csharp"]:
                        to_download.append(("csharp", dataset_key, DATASETS["csharp"][dataset_key]))
                    else:
                        print_error(f"Unknown C# dataset: {dataset_key}")
                        print_info(f"Available: {', '.join(DATASETS['csharp'].keys())}")

        if args.java is not None:
            if len(args.java) == 0:
                # All Java datasets
                for dataset_key, dataset_info in DATASETS["java"].items():
                    to_download.append(("java", dataset_key, dataset_info))
            else:
                # Specific Java datasets
                for dataset_key in args.java:
                    if dataset_key in DATASETS["java"]:
                        to_download.append(("java", dataset_key, DATASETS["java"][dataset_key]))
                    else:
                        print_error(f"Unknown Java dataset: {dataset_key}")
                        print_info(f"Available: {', '.join(DATASETS['java'].keys())}")

    if not to_download:
        print_warning("No datasets selected")
        print_info("Use --all, --csharp, or --java")
        return 1

    # Download datasets
    print_header(f"Downloading {len(to_download)} Dataset(s)")

    success_count = 0
    failed = []

    for lang_key, dataset_key, dataset_info in to_download:
        print()
        print(f"{BOLD}Dataset: {dataset_info['name']}{RESET}")
        print(f"Language: {dataset_info['language']}")
        print(f"Size: {dataset_info['size']}")
        print()

        target_dir = output_dir / dataset_key

        if clone_repository(
            dataset_info['name'],
            dataset_info['url'],
            dataset_info['branch'],
            target_dir
        ):
            success_count += 1
        else:
            failed.append(dataset_info['name'])

    # Summary
    print_header("Download Summary")
    print(f"Total datasets: {len(to_download)}")
    print(f"Successful: {GREEN}{success_count}{RESET}")
    print(f"Failed: {RED}{len(failed)}{RESET}")

    if failed:
        print()
        print("Failed datasets:")
        for name in failed:
            print(f"  • {name}")

    print()
    print_success(f"Datasets downloaded to: {output_dir}")
    print()

    # Next steps
    print_header("Next Steps")
    print("Run analysis on downloaded datasets:")
    print()

    for lang_key, dataset_key, dataset_info in to_download:
        if dataset_info['name'] not in failed:
            target_dir = output_dir / dataset_key
            print(f"{BOLD}{dataset_info['name']}:{RESET}")
            print(f"  python run.py --repos {target_dir} --out output-{dataset_key}")
            print()

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
