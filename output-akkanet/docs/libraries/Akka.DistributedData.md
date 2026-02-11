# Akka.DistributedData

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | akka.net |
| Path | `src/contrib/cluster/Akka.DistributedData/Akka.DistributedData.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 7 |

## Dependency Diagram

```mermaid
graph TD
    Akka_DistributedData["<strong>Akka.DistributedData</strong>"]
    Akka_Cluster["Akka.Cluster"]
    Akka_DistributedData --> Akka_Cluster
    Akka_Benchmarks["Akka.Benchmarks"]
    Akka_Benchmarks -.-> Akka_DistributedData
    Akka_DistributedData_LightningDB["Akka.DistributedData.LightningDB"]
    Akka_DistributedData_LightningDB -.-> Akka_DistributedData
    Akka_DistributedData_Tests_MultiNode["Akka.DistributedData.Tests.MultiNode"]
    Akka_DistributedData_Tests_MultiNode -.-> Akka_DistributedData
    Akka_DistributedData_Tests["Akka.DistributedData.Tests"]
    Akka_DistributedData_Tests -.-> Akka_DistributedData
    Akka_Cluster_Sharding["Akka.Cluster.Sharding"]
    Akka_Cluster_Sharding -.-> Akka_DistributedData
    DDataStressTest["DDataStressTest"]
    DDataStressTest -.-> Akka_DistributedData
    Akka_API_Tests["Akka.API.Tests"]
    Akka_API_Tests -.-> Akka_DistributedData
```

## Project References
- Akka.Cluster

## Consumed By
- Akka.Benchmarks
- Akka.DistributedData.LightningDB
- Akka.DistributedData.Tests.MultiNode
- Akka.DistributedData.Tests
- Akka.Cluster.Sharding
- DDataStressTest
- Akka.API.Tests

## External NuGet Packages
| Package | Version |
|---------|---------||
| Grpc.Tools | 2.60.0 |


---

*[Back to Index](../index.md)*
