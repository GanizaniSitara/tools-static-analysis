# KurrentDB.Core.TUnit.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | src |
| Path | `KurrentDB.Core.TUnit.Tests/KurrentDB.Core.TUnit.Tests.csproj` |
| Project References | 2 |
| NuGet Dependencies | 3 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_Core_TUnit_Tests["<strong>KurrentDB.Core.TUnit.Tests</strong>"]
    KurrentDB_Testing_ClusterVNodeApp["KurrentDB.Testing.ClusterVNodeApp"]
    KurrentDB_Core_TUnit_Tests --> KurrentDB_Testing_ClusterVNodeApp
    KurrentDB_Testing["KurrentDB.Testing"]
    KurrentDB_Core_TUnit_Tests --> KurrentDB_Testing
    KurrentDB_Ammeter["KurrentDB.Ammeter"]
    KurrentDB_Ammeter -.-> KurrentDB_Core_TUnit_Tests
```

## Project References
- KurrentDB.Testing.ClusterVNodeApp
- KurrentDB.Testing

## Consumed By
- KurrentDB.Ammeter

## External NuGet Packages
| Package | Version |
|---------|---------||
| Grpc.Net.Client |  |
| Grpc.StatusProto |  |
| Microsoft.Extensions.Diagnostics.Testing |  |


---

*[Back to Index](../index.md)*
