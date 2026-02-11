# KurrentDB.Testing.ClusterVNodeApp

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | src |
| Path | `KurrentDB.Testing.ClusterVNodeApp/KurrentDB.Testing.ClusterVNodeApp.csproj` |
| Project References | 2 |
| NuGet Dependencies | 5 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_Testing_ClusterVNodeApp["<strong>KurrentDB.Testing.ClusterVNodeApp</strong>"]
    KurrentDB_Testing["KurrentDB.Testing"]
    KurrentDB_Testing_ClusterVNodeApp --> KurrentDB_Testing
    KurrentDB["KurrentDB"]
    KurrentDB_Testing_ClusterVNodeApp --> KurrentDB
    KurrentDB_Api_V2_Tests["KurrentDB.Api.V2.Tests"]
    KurrentDB_Api_V2_Tests -.-> KurrentDB_Testing_ClusterVNodeApp
    KurrentDB_SchemaRegistry_Tests["KurrentDB.SchemaRegistry.Tests"]
    KurrentDB_SchemaRegistry_Tests -.-> KurrentDB_Testing_ClusterVNodeApp
    KurrentDB_Core_TUnit_Tests["KurrentDB.Core.TUnit.Tests"]
    KurrentDB_Core_TUnit_Tests -.-> KurrentDB_Testing_ClusterVNodeApp
```

## Project References
- KurrentDB.Testing
- KurrentDB

## Consumed By
- KurrentDB.Api.V2.Tests
- KurrentDB.SchemaRegistry.Tests
- KurrentDB.Core.TUnit.Tests

## External NuGet Packages
| Package | Version |
|---------|---------||
| Grpc.Net.Client |  |
| OpenTelemetry.Exporter.OpenTelemetryProtocol |  |
| RestSharp |  |
| Testcontainers |  |
| Grpc.Tools |  |


---

*[Back to Index](../index.md)*
