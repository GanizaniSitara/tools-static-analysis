# Akka.Cluster.Tools.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/contrib/cluster/Akka.Cluster.Tools.Tests/Akka.Cluster.Tools.Tests.csproj` |
| Project References | 3 |
| NuGet Dependencies | 4 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Cluster_Tools_Tests["<strong>Akka.Cluster.Tools.Tests</strong>"]
    Akka_Coordination_Tests["Akka.Coordination.Tests"]
    Akka_Cluster_Tools_Tests --> Akka_Coordination_Tests
    Akka_Cluster_Tools["Akka.Cluster.Tools"]
    Akka_Cluster_Tools_Tests --> Akka_Cluster_Tools
    Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    Akka_Cluster_Tools_Tests --> Akka_Tests_Shared_Internals
```

## Project References
- Akka.Coordination.Tests
- Akka.Cluster.Tools
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
