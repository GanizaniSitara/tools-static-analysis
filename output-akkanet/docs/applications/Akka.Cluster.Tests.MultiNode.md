# Akka.Cluster.Tests.MultiNode

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/core/Akka.Cluster.Tests.MultiNode/Akka.Cluster.Tests.MultiNode.csproj` |
| Project References | 3 |
| NuGet Dependencies | 5 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Cluster_Tests_MultiNode["<strong>Akka.Cluster.Tests.MultiNode</strong>"]
    Akka_Cluster_TestKit["Akka.Cluster.TestKit"]
    Akka_Cluster_Tests_MultiNode --> Akka_Cluster_TestKit
    Akka_Coordination_Tests["Akka.Coordination.Tests"]
    Akka_Cluster_Tests_MultiNode --> Akka_Coordination_Tests
    Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    Akka_Cluster_Tests_MultiNode --> Akka_Tests_Shared_Internals
```

## Project References
- Akka.Cluster.TestKit
- Akka.Coordination.Tests
- Akka.Tests.Shared.Internals

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
