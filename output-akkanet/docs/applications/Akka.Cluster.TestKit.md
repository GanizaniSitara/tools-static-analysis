# Akka.Cluster.TestKit

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/core/Akka.Cluster.TestKit/Akka.Cluster.TestKit.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Cluster_TestKit["<strong>Akka.Cluster.TestKit</strong>"]
    Akka_Remote_TestKit["Akka.Remote.TestKit"]
    Akka_Cluster_TestKit --> Akka_Remote_TestKit
    Akka_Cluster["Akka.Cluster"]
    Akka_Cluster_TestKit --> Akka_Cluster
    Akka_Cluster_Tools_Tests_MultiNode["Akka.Cluster.Tools.Tests.MultiNode"]
    Akka_Cluster_Tools_Tests_MultiNode -.-> Akka_Cluster_TestKit
    Akka_DistributedData_Tests_MultiNode["Akka.DistributedData.Tests.MultiNode"]
    Akka_DistributedData_Tests_MultiNode -.-> Akka_Cluster_TestKit
    Akka_Cluster_Sharding_Tests_MultiNode["Akka.Cluster.Sharding.Tests.MultiNode"]
    Akka_Cluster_Sharding_Tests_MultiNode -.-> Akka_Cluster_TestKit
    Akka_Cluster_Metrics_Tests_MultiNode["Akka.Cluster.Metrics.Tests.MultiNode"]
    Akka_Cluster_Metrics_Tests_MultiNode -.-> Akka_Cluster_TestKit
    Akka_Cluster_Tests_MultiNode["Akka.Cluster.Tests.MultiNode"]
    Akka_Cluster_Tests_MultiNode -.-> Akka_Cluster_TestKit
```

## Project References
- Akka.Remote.TestKit
- Akka.Cluster

## Consumed By
- Akka.Cluster.Tools.Tests.MultiNode
- Akka.DistributedData.Tests.MultiNode
- Akka.Cluster.Sharding.Tests.MultiNode
- Akka.Cluster.Metrics.Tests.MultiNode
- Akka.Cluster.Tests.MultiNode


---

*[Back to Index](../index.md)*
