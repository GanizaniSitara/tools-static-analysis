# KurrentDB.SourceGenerators

## Overview

| Property | Value |
|----------|-------|
| Category | Tool |
| Repository | src |
| Path | `KurrentDB.SourceGenerators/KurrentDB.SourceGenerators.csproj` |
| Project References | 0 |
| NuGet Dependencies | 2 |
| Consumers | 4 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_SourceGenerators["<strong>KurrentDB.SourceGenerators</strong>"]
    KurrentDB_Projections_Core["KurrentDB.Projections.Core"]
    KurrentDB_Projections_Core -.-> KurrentDB_SourceGenerators
    KurrentDB_SourceGenerators_Tests["KurrentDB.SourceGenerators.Tests"]
    KurrentDB_SourceGenerators_Tests -.-> KurrentDB_SourceGenerators
    KurrentDB_Core_XUnit_Tests["KurrentDB.Core.XUnit.Tests"]
    KurrentDB_Core_XUnit_Tests -.-> KurrentDB_SourceGenerators
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_Core -.-> KurrentDB_SourceGenerators
```

## Consumed By
- KurrentDB.Projections.Core
- KurrentDB.SourceGenerators.Tests
- KurrentDB.Core.XUnit.Tests
- KurrentDB.Core

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.CodeAnalysis.Analyzers |  |
| Microsoft.CodeAnalysis.CSharp |  |


---

*[Back to Index](../index.md)*
