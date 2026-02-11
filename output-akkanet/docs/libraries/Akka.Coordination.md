# Akka.Coordination

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | akka.net |
| Path | `src/core/Akka.Coordination/Akka.Coordination.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Coordination["<strong>Akka.Coordination</strong>"]
    Akka["Akka"]
    Akka_Coordination --> Akka
    Akka_Cluster_Tools["Akka.Cluster.Tools"]
    Akka_Cluster_Tools -.-> Akka_Coordination
    Akka_Cluster_Sharding["Akka.Cluster.Sharding"]
    Akka_Cluster_Sharding -.-> Akka_Coordination
    Akka_Cluster["Akka.Cluster"]
    Akka_Cluster -.-> Akka_Coordination
    Akka_Coordination_Tests["Akka.Coordination.Tests"]
    Akka_Coordination_Tests -.-> Akka_Coordination
    Akka_API_Tests["Akka.API.Tests"]
    Akka_API_Tests -.-> Akka_Coordination
```

## Project References
- Akka

## Consumed By
- Akka.Cluster.Tools
- Akka.Cluster.Sharding
- Akka.Cluster
- Akka.Coordination.Tests
- Akka.API.Tests


---

*[Back to Index](../index.md)*
