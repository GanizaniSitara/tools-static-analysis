# Demo Dataset Bootstrapper

## Overview

`bootstrap-demo-datasets.py` downloads curated open-source projects that are useful for static-analysis demos and validation runs.

Use it when you want a known C# or Java codebase without having to find repositories manually.

## Quick start

List the available datasets:

```text
python bootstrap-demo-datasets.py --list
```

Download everything:

```text
python bootstrap-demo-datasets.py --all
```

Download only C# datasets:

```text
python bootstrap-demo-datasets.py --csharp
python bootstrap-demo-datasets.py --csharp eshop orchardcore
```

Download only Java datasets:

```text
python bootstrap-demo-datasets.py --java
python bootstrap-demo-datasets.py --java spring-petclinic ta4j cassandre
```

Download into a custom directory:

```text
python bootstrap-demo-datasets.py --all --output C:/demo-projects
```

## Included datasets

C# datasets:
- `eshop`: Microsoft's reference .NET e-commerce application
- `orchardcore`: large modular ASP.NET Core CMS

Java datasets:
- `spring-petclinic`: classic Spring Boot sample application
- `ta4j`: technical-analysis library with financial indicators
- `cassandre`: Spring Boot trading-bot framework

Run `python bootstrap-demo-datasets.py --list` to see the current full catalog and metadata.

## Example workflow

Download one sample repo and run the pipeline:

```text
python bootstrap-demo-datasets.py --csharp eshop
python run.py C:/demo-projects/eshop output-eshop
```

Compare a C# project and a Java project:

```text
python bootstrap-demo-datasets.py --csharp orchardcore --java ta4j
python run.py C:/demo-projects/orchardcore output-orchardcore
python run.py C:/demo-projects/ta4j output-ta4j
```

After the pipeline finishes, open the generated `viewer.html` file from the corresponding output directory in your browser.

## Requirements

- Python 3.8+
- Git available on `PATH`
- Enough disk space for the selected repositories

The script performs shallow clones to reduce download size.

## Troubleshooting

If Git is not installed:
- install Git, then rerun the command

If a target directory already exists:
- the script will ask whether to update that repository

If you are short on disk space:
- download only the datasets you need instead of using `--all`

If cloning fails:
- verify that GitHub is reachable from your environment
- rerun with a smaller subset to isolate the failing repository

## Typical outputs

The bootstrapper downloads each repository into the output directory you choose. For example:

```text
C:/demo-projects/
  eshop/
  orchardcore/
  spring-petclinic/
  ta4j/
  cassandre/
```

Each downloaded repository can then be passed directly to `run.py`.
