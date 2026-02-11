# KurrentDB.Api.V2.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | src |
| Path | `KurrentDB.Api.V2.Tests/KurrentDB.Api.V2.Tests.csproj` |
| Project References | 3 |
| NuGet Dependencies | 4 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_Api_V2_Tests["<strong>KurrentDB.Api.V2.Tests</strong>"]
    KurrentDB_Testing_ClusterVNodeApp["KurrentDB.Testing.ClusterVNodeApp"]
    KurrentDB_Api_V2_Tests --> KurrentDB_Testing_ClusterVNodeApp
    KurrentDB_Testing["KurrentDB.Testing"]
    KurrentDB_Api_V2_Tests --> KurrentDB_Testing
    KurrentDB_Api_V2["KurrentDB.Api.V2"]
    KurrentDB_Api_V2_Tests --> KurrentDB_Api_V2
    KurrentDB_Ammeter["KurrentDB.Ammeter"]
    KurrentDB_Ammeter -.-> KurrentDB_Api_V2_Tests
```

## Project References
- KurrentDB.Testing.ClusterVNodeApp
- KurrentDB.Testing
- KurrentDB.Api.V2

## Consumed By
- KurrentDB.Ammeter

## External NuGet Packages
| Package | Version |
|---------|---------||
| Grpc.Net.Client |  |
| Grpc.StatusProto |  |
| Microsoft.Extensions.Diagnostics.Testing |  |
| System.Linq.Async |  |


---

*[Back to Index](../index.md)*
