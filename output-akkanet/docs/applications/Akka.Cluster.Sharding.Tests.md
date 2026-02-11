# Akka.Cluster.Sharding.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/contrib/cluster/Akka.Cluster.Sharding.Tests/Akka.Cluster.Sharding.Tests.csproj` |
| Project References | 4 |
| NuGet Dependencies | 4 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Cluster_Sharding_Tests["<strong>Akka.Cluster.Sharding.Tests</strong>"]
    Akka_Coordination_Tests["Akka.Coordination.Tests"]
    Akka_Cluster_Sharding_Tests --> Akka_Coordination_Tests
    Akka_Cluster_Sharding["Akka.Cluster.Sharding"]
    Akka_Cluster_Sharding_Tests --> Akka_Cluster_Sharding
    Akka_Persistence["Akka.Persistence"]
    Akka_Cluster_Sharding_Tests --> Akka_Persistence
    Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    Akka_Cluster_Sharding_Tests --> Akka_Tests_Shared_Internals
```

## Project References
- Akka.Coordination.Tests
- Akka.Cluster.Sharding
- Akka.Persistence
- Akka.Tests.Shared.Internals

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.NET.Test.Sdk | 17.9.0 |
| xunit | 2.8.1 |
| xunit.runner.visualstudio | 2.8.1 |
| FluentAssertions | 5.10.3 |


---

*[Back to Index](../index.md)*
