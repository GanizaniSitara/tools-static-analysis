# KurrentDB.SecondaryIndexing.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | src |
| Path | `KurrentDB.SecondaryIndexing.Tests/KurrentDB.SecondaryIndexing.Tests.csproj` |
| Project References | 4 |
| NuGet Dependencies | 4 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_SecondaryIndexing_Tests["<strong>KurrentDB.SecondaryIndexing.Tests</strong>"]
    KurrentDB_SecondaryIndexing["KurrentDB.SecondaryIndexing"]
    KurrentDB_SecondaryIndexing_Tests --> KurrentDB_SecondaryIndexing
    KurrentDB_Core_Testing_XUnit["KurrentDB.Core.Testing.XUnit"]
    KurrentDB_SecondaryIndexing_Tests --> KurrentDB_Core_Testing_XUnit
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_SecondaryIndexing_Tests --> KurrentDB_Core
    KurrentDB_Surge_Testing["KurrentDB.Surge.Testing"]
    KurrentDB_SecondaryIndexing_Tests --> KurrentDB_Surge_Testing
    KurrentDB_SecondaryIndexing_LoadTesting["KurrentDB.SecondaryIndexing.LoadTesting"]
    KurrentDB_SecondaryIndexing_LoadTesting -.-> KurrentDB_SecondaryIndexing_Tests
```

## Project References
- KurrentDB.SecondaryIndexing
- KurrentDB.Core.Testing.XUnit
- KurrentDB.Core
- KurrentDB.Surge.Testing

## Consumed By
- KurrentDB.SecondaryIndexing.LoadTesting

## External NuGet Packages
| Package | Version |
|---------|---------||
| Bogus |  |
| Microsoft.AspNetCore.Mvc.Testing |  |
| NSubstitute |  |
| System.Linq.Async |  |


---

*[Back to Index](../index.md)*
