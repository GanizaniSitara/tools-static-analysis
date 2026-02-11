# KurrentDB.SchemaRegistry.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | src |
| Path | `SchemaRegistry/KurrentDB.SchemaRegistry.Tests/KurrentDB.SchemaRegistry.Tests.csproj` |
| Project References | 5 |
| NuGet Dependencies | 3 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_SchemaRegistry_Tests["<strong>KurrentDB.SchemaRegistry.Tests</strong>"]
    KurrentDB_Surge_Testing_Messages["KurrentDB.Surge.Testing.Messages"]
    KurrentDB_SchemaRegistry_Tests --> KurrentDB_Surge_Testing_Messages
    KurrentDB_Testing_ClusterVNodeApp["KurrentDB.Testing.ClusterVNodeApp"]
    KurrentDB_SchemaRegistry_Tests --> KurrentDB_Testing_ClusterVNodeApp
    KurrentDB_Testing["KurrentDB.Testing"]
    KurrentDB_SchemaRegistry_Tests --> KurrentDB_Testing
    KurrentDB["KurrentDB"]
    KurrentDB_SchemaRegistry_Tests --> KurrentDB
    KurrentDB_SchemaRegistry["KurrentDB.SchemaRegistry"]
    KurrentDB_SchemaRegistry_Tests --> KurrentDB_SchemaRegistry
```

## Project References
- KurrentDB.Surge.Testing.Messages
- KurrentDB.Testing.ClusterVNodeApp
- KurrentDB.Testing
- KurrentDB
- KurrentDB.SchemaRegistry

## External NuGet Packages
| Package | Version |
|---------|---------||
| Kurrent.Surge |  |
| Kurrent.Surge.DuckDB |  |
| Shouldly |  |


---

*[Back to Index](../index.md)*
