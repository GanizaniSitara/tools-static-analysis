# Akka.Coordination.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/core/Akka.Coordination.Tests/Akka.Coordination.Tests.csproj` |
| Project References | 2 |
| NuGet Dependencies | 5 |
| Consumers | 6 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Coordination_Tests["<strong>Akka.Coordination.Tests</strong>"]
    Akka_Coordination["Akka.Coordination"]
    Akka_Coordination_Tests --> Akka_Coordination
    Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    Akka_Coordination_Tests --> Akka_Tests_Shared_Internals
    Akka_Cluster_Tools_Tests_MultiNode["Akka.Cluster.Tools.Tests.MultiNode"]
    Akka_Cluster_Tools_Tests_MultiNode -.-> Akka_Coordination_Tests
    Akka_Cluster_Sharding_Tests["Akka.Cluster.Sharding.Tests"]
    Akka_Cluster_Sharding_Tests -.-> Akka_Coordination_Tests
    Akka_Cluster_Tools_Tests["Akka.Cluster.Tools.Tests"]
    Akka_Cluster_Tools_Tests -.-> Akka_Coordination_Tests
    Akka_Docs_Tests["Akka.Docs.Tests"]
    Akka_Docs_Tests -.-> Akka_Coordination_Tests
    Akka_Cluster_Tests_MultiNode["Akka.Cluster.Tests.MultiNode"]
    Akka_Cluster_Tests_MultiNode -.-> Akka_Coordination_Tests
    Akka_Cluster_Tests["Akka.Cluster.Tests"]
    Akka_Cluster_Tests -.-> Akka_Coordination_Tests
```

## Project References
- Akka.Coordination
- Akka.Tests.Shared.Internals

## Consumed By
- Akka.Cluster.Tools.Tests.MultiNode
- Akka.Cluster.Sharding.Tests
- Akka.Cluster.Tools.Tests
- Akka.Docs.Tests
- Akka.Cluster.Tests.MultiNode
- Akka.Cluster.Tests

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.NET.Test.Sdk | 17.9.0 |
| xunit | 2.8.1 |
| xunit.runner.visualstudio | 2.8.1 |
| FluentAssertions | 5.10.3 |
| FsCheck.Xunit | 2.16.6 |


---

*[Back to Index](../index.md)*
