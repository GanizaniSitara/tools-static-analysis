# Akka.Cluster.Tools.Tests.MultiNode

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/Akka.Cluster.Tools.Tests.MultiNode.csproj` |
| Project References | 4 |
| NuGet Dependencies | 6 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Cluster_Tools_Tests_MultiNode["<strong>Akka.Cluster.Tools.Tests.MultiNode</strong>"]
    Akka_Coordination_Tests["Akka.Coordination.Tests"]
    Akka_Cluster_Tools_Tests_MultiNode --> Akka_Coordination_Tests
    Akka_Cluster_Tools["Akka.Cluster.Tools"]
    Akka_Cluster_Tools_Tests_MultiNode --> Akka_Cluster_Tools
    Akka_Cluster_TestKit["Akka.Cluster.TestKit"]
    Akka_Cluster_Tools_Tests_MultiNode --> Akka_Cluster_TestKit
    Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    Akka_Cluster_Tools_Tests_MultiNode --> Akka_Tests_Shared_Internals
```

## Project References
- Akka.Coordination.Tests
- Akka.Cluster.Tools
- Akka.Cluster.TestKit
- Akka.Tests.Shared.Internals

## External NuGet Packages
| Package | Version |
|---------|---------||
| Akka.Management | 1.5.50 |
| Akka.MultiNode.TestAdapter | 1.5.40 |
| Microsoft.NET.Test.Sdk | 17.9.0 |
| FluentAssertions | 5.10.3 |
| xunit | 2.8.1 |
| xunit.runner.visualstudio | 2.8.1 |


---

*[Back to Index](../index.md)*
