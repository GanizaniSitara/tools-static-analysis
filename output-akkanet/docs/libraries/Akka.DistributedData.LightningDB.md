# Akka.DistributedData.LightningDB

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | akka.net |
| Path | `src/contrib/cluster/Akka.DistributedData.LightningDB/Akka.DistributedData.LightningDB.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 4 |

## Dependency Diagram

```mermaid
graph TD
    Akka_DistributedData_LightningDB["<strong>Akka.DistributedData.LightningDB</strong>"]
    Akka_DistributedData["Akka.DistributedData"]
    Akka_DistributedData_LightningDB --> Akka_DistributedData
    Akka_DistributedData_Tests_MultiNode["Akka.DistributedData.Tests.MultiNode"]
    Akka_DistributedData_Tests_MultiNode -.-> Akka_DistributedData_LightningDB
    Akka_Cluster_Sharding_Tests_MultiNode["Akka.Cluster.Sharding.Tests.MultiNode"]
    Akka_Cluster_Sharding_Tests_MultiNode -.-> Akka_DistributedData_LightningDB
    Akka_DistributedData_Tests["Akka.DistributedData.Tests"]
    Akka_DistributedData_Tests -.-> Akka_DistributedData_LightningDB
    Akka_Cluster_Sharding["Akka.Cluster.Sharding"]
    Akka_Cluster_Sharding -.-> Akka_DistributedData_LightningDB
```

## Project References
- Akka.DistributedData

## Consumed By
- Akka.DistributedData.Tests.MultiNode
- Akka.Cluster.Sharding.Tests.MultiNode
- Akka.DistributedData.Tests
- Akka.Cluster.Sharding

## External NuGet Packages
| Package | Version |
|---------|---------||
| LightningDB | 0.16.0 |


---

*[Back to Index](../index.md)*
