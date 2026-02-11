# KurrentDB.SchemaRegistry

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `SchemaRegistry/KurrentDB.SchemaRegistry/KurrentDB.SchemaRegistry.csproj` |
| Project References | 2 |
| NuGet Dependencies | 6 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_SchemaRegistry["<strong>KurrentDB.SchemaRegistry</strong>"]
    KurrentDB_Surge["KurrentDB.Surge"]
    KurrentDB_SchemaRegistry --> KurrentDB_Surge
    KurrentDB_SchemaRegistry_Protocol["KurrentDB.SchemaRegistry.Protocol"]
    KurrentDB_SchemaRegistry --> KurrentDB_SchemaRegistry_Protocol
    KurrentDB_SchemaRegistry_Tests["KurrentDB.SchemaRegistry.Tests"]
    KurrentDB_SchemaRegistry_Tests -.-> KurrentDB_SchemaRegistry
    KurrentDB_Plugins_SchemaRegistry["KurrentDB.Plugins.SchemaRegistry"]
    KurrentDB_Plugins_SchemaRegistry -.-> KurrentDB_SchemaRegistry
```

## Project References
- KurrentDB.Surge
- KurrentDB.SchemaRegistry.Protocol

## Consumed By
- KurrentDB.SchemaRegistry.Tests
- KurrentDB.Plugins.SchemaRegistry

## External NuGet Packages
| Package | Version |
|---------|---------||
| FluentValidation.DependencyInjectionExtensions |  |
| Grpc.AspNetCore |  |
| Kurrent.Quack |  |
| Kurrent.Surge.DuckDB |  |
| Kurrent.Surge.Core |  |
| NJsonSchema |  |


---

*[Back to Index](../index.md)*
