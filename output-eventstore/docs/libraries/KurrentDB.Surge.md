# KurrentDB.Surge

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `KurrentDB.Surge/KurrentDB.Surge.csproj` |
| Project References | 1 |
| NuGet Dependencies | 5 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_Surge["<strong>KurrentDB.Surge</strong>"]
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_Surge --> KurrentDB_Core
    KurrentDB_SchemaRegistry["KurrentDB.SchemaRegistry"]
    KurrentDB_SchemaRegistry -.-> KurrentDB_Surge
    KurrentDB_Connectors["KurrentDB.Connectors"]
    KurrentDB_Connectors -.-> KurrentDB_Surge
```

## Project References
- KurrentDB.Core

## Consumed By
- KurrentDB.SchemaRegistry
- KurrentDB.Connectors

## External NuGet Packages
| Package | Version |
|---------|---------||
| Kurrent.Surge.Core |  |
| Eventuous.Application |  |
| Eventuous.Extensions.AspNetCore |  |
| Eventuous.Extensions.DependencyInjection |  |
| System.Linq.Async |  |


---

*[Back to Index](../index.md)*
