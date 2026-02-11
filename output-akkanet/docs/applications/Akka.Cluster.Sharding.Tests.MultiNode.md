# Akka.Cluster.Sharding.Tests.MultiNode

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/contrib/cluster/Akka.Cluster.Sharding.Tests.MultiNode/Akka.Cluster.Sharding.Tests.MultiNode.csproj` |
| Project References | 5 |
| NuGet Dependencies | 5 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Cluster_Sharding_Tests_MultiNode["<strong>Akka.Cluster.Sharding.Tests.MultiNode</strong>"]
    Akka_Serialization_Hyperion["Akka.Serialization.Hyperion"]
    Akka_Cluster_Sharding_Tests_MultiNode --> Akka_Serialization_Hyperion
    Akka_Cluster_Sharding["Akka.Cluster.Sharding"]
    Akka_Cluster_Sharding_Tests_MultiNode --> Akka_Cluster_Sharding
    Akka_Cluster_TestKit["Akka.Cluster.TestKit"]
    Akka_Cluster_Sharding_Tests_MultiNode --> Akka_Cluster_TestKit
    Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    Akka_Cluster_Sharding_Tests_MultiNode --> Akka_Tests_Shared_Internals
    Akka_DistributedData_LightningDB["Akka.DistributedData.LightningDB"]
    Akka_Cluster_Sharding_Tests_MultiNode --> Akka_DistributedData_LightningDB
```

## Project References
- Akka.Serialization.Hyperion
- Akka.Cluster.Sharding
- Akka.Cluster.TestKit
- Akka.Tests.Shared.Internals
- Akka.DistributedData.LightningDB

## External NuGet Packages
| Package | Version |
|---------|---------||
| Akka.MultiNode.TestAdapter | 1.5.40 |
| Microsoft.NET.Test.Sdk | 17.9.0 |
| FluentAssertions | 5.10.3 |
| xunit | 2.8.1 |
| xunit.runner.visualstudio | 2.8.1 |


---

*[Back to Index](../index.md)*
