# KurrentDB.Core.XUnit.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | src |
| Path | `KurrentDB.Core.XUnit.Tests/KurrentDB.Core.XUnit.Tests.csproj` |
| Project References | 3 |
| NuGet Dependencies | 4 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_Core_XUnit_Tests["<strong>KurrentDB.Core.XUnit.Tests</strong>"]
    KurrentDB_Core_Testing_XUnit["KurrentDB.Core.Testing.XUnit"]
    KurrentDB_Core_XUnit_Tests --> KurrentDB_Core_Testing_XUnit
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_Core_XUnit_Tests --> KurrentDB_Core
    KurrentDB_SourceGenerators["KurrentDB.SourceGenerators"]
    KurrentDB_Core_XUnit_Tests --> KurrentDB_SourceGenerators
```

## Project References
- KurrentDB.Core.Testing.XUnit
- KurrentDB.Core
- KurrentDB.SourceGenerators

## External NuGet Packages
| Package | Version |
|---------|---------||
| TestableIO.System.IO.Abstractions |  |
| TestableIO.System.IO.Abstractions.TestingHelpers |  |
| Microsoft.Extensions.Diagnostics.Testing |  |
| System.Linq.Async |  |


---

*[Back to Index](../index.md)*
