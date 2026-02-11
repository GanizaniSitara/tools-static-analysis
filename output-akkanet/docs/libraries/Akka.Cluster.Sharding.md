# Akka.Cluster.Sharding

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | akka.net |
| Path | `src/contrib/cluster/Akka.Cluster.Sharding/Akka.Cluster.Sharding.csproj` |
| Project References | 5 |
| NuGet Dependencies | 0 |
| Consumers | 7 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Cluster_Sharding["<strong>Akka.Cluster.Sharding</strong>"]
    Akka_Coordination["Akka.Coordination"]
    Akka_Cluster_Sharding --> Akka_Coordination
    Akka_Persistence["Akka.Persistence"]
    Akka_Cluster_Sharding --> Akka_Persistence
    Akka_Cluster_Tools["Akka.Cluster.Tools"]
    Akka_Cluster_Sharding --> Akka_Cluster_Tools
    Akka_DistributedData_LightningDB["Akka.DistributedData.LightningDB"]
    Akka_Cluster_Sharding --> Akka_DistributedData_LightningDB
    Akka_DistributedData["Akka.DistributedData"]
    Akka_Cluster_Sharding --> Akka_DistributedData
    Akka_Cluster_Benchmarks["Akka.Cluster.Benchmarks"]
    Akka_Cluster_Benchmarks -.-> Akka_Cluster_Sharding
    Akka_Cluster_Sharding_Tests["Akka.Cluster.Sharding.Tests"]
    Akka_Cluster_Sharding_Tests -.-> Akka_Cluster_Sharding
    Akka_Cluster_Sharding_Tests_MultiNode["Akka.Cluster.Sharding.Tests.MultiNode"]
    Akka_Cluster_Sharding_Tests_MultiNode -.-> Akka_Cluster_Sharding
    Akka_DistributedData_Tests["Akka.DistributedData.Tests"]
    Akka_DistributedData_Tests -.-> Akka_Cluster_Sharding
    ClusterSharding_Node["ClusterSharding.Node"]
    ClusterSharding_Node -.-> Akka_Cluster_Sharding
    ShoppingCart["ShoppingCart"]
    ShoppingCart -.-> Akka_Cluster_Sharding
    Akka_API_Tests["Akka.API.Tests"]
    Akka_API_Tests -.-> Akka_Cluster_Sharding
```

## Project References
- Akka.Coordination
- Akka.Persistence
- Akka.Cluster.Tools
- Akka.DistributedData.LightningDB
- Akka.DistributedData

## Consumed By
- Akka.Cluster.Benchmarks
- Akka.Cluster.Sharding.Tests
- Akka.Cluster.Sharding.Tests.MultiNode
- Akka.DistributedData.Tests
- ClusterSharding.Node
- ShoppingCart
- Akka.API.Tests


---

*[Back to Index](../index.md)*
