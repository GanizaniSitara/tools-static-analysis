# KurrentDB.SecondaryIndexing.LoadTesting

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | src |
| Path | `KurrentDB.SecondaryIndexing.LoadTesting/KurrentDB.SecondaryIndexing.LoadTesting.csproj` |
| Project References | 3 |
| NuGet Dependencies | 2 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_SecondaryIndexing_LoadTesting["<strong>KurrentDB.SecondaryIndexing.LoadTesting</strong>"]
    KurrentDB_Connectors_TestServer["KurrentDB.Connectors.TestServer"]
    KurrentDB_SecondaryIndexing_LoadTesting --> KurrentDB_Connectors_TestServer
    KurrentDB_SecondaryIndexing_Tests["KurrentDB.SecondaryIndexing.Tests"]
    KurrentDB_SecondaryIndexing_LoadTesting --> KurrentDB_SecondaryIndexing_Tests
    KurrentDB_SecondaryIndexing["KurrentDB.SecondaryIndexing"]
    KurrentDB_SecondaryIndexing_LoadTesting --> KurrentDB_SecondaryIndexing
```

## Project References
- KurrentDB.Connectors.TestServer
- KurrentDB.SecondaryIndexing.Tests
- KurrentDB.SecondaryIndexing

## External NuGet Packages
| Package | Version |
|---------|---------||
| Dapper |  |
| KurrentDB.Client |  |


---

*[Back to Index](../index.md)*
