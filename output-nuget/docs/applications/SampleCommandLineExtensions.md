# SampleCommandLineExtensions

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/TestExtensions/SampleCommandLineExtensions/SampleCommandLineExtensions.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    SampleCommandLineExtensions["<strong>SampleCommandLineExtensions</strong>"]
    NuGet_CommandLine["NuGet.CommandLine"]
    SampleCommandLineExtensions --> NuGet_CommandLine
    NuGet_CommandLine_Test["NuGet.CommandLine.Test"]
    NuGet_CommandLine_Test -.-> SampleCommandLineExtensions
```

## Project References
- NuGet.CommandLine

## Consumed By
- NuGet.CommandLine.Test


---

*[Back to Index](../index.md)*
