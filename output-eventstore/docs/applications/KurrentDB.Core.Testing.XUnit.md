# KurrentDB.Core.Testing.XUnit

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | src |
| Path | `KurrentDB.Core.Testing.XUnit/KurrentDB.Core.Testing.XUnit.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_Core_Testing_XUnit["<strong>KurrentDB.Core.Testing.XUnit</strong>"]
    KurrentDB_Core_Testing["KurrentDB.Core.Testing"]
    KurrentDB_Core_Testing_XUnit --> KurrentDB_Core_Testing
    KurrentDB_Core_XUnit_Tests["KurrentDB.Core.XUnit.Tests"]
    KurrentDB_Core_XUnit_Tests -.-> KurrentDB_Core_Testing_XUnit
    KurrentDB_SecondaryIndexing_Tests["KurrentDB.SecondaryIndexing.Tests"]
    KurrentDB_SecondaryIndexing_Tests -.-> KurrentDB_Core_Testing_XUnit
```

## Project References
- KurrentDB.Core.Testing

## Consumed By
- KurrentDB.Core.XUnit.Tests
- KurrentDB.SecondaryIndexing.Tests

## External NuGet Packages
| Package | Version |
|---------|---------||
| xunit.v3.extensibility.core |  |


---

*[Back to Index](../index.md)*
