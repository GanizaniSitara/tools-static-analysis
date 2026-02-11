# Akka.Cluster.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/core/Akka.Cluster.Tests/Akka.Cluster.Tests.csproj` |
| Project References | 3 |
| NuGet Dependencies | 6 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Cluster_Tests["<strong>Akka.Cluster.Tests</strong>"]
    Akka_Cluster["Akka.Cluster"]
    Akka_Cluster_Tests --> Akka_Cluster
    Akka_Coordination_Tests["Akka.Coordination.Tests"]
    Akka_Cluster_Tests --> Akka_Coordination_Tests
    Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    Akka_Cluster_Tests --> Akka_Tests_Shared_Internals
    Akka_Cluster_Metrics_Tests["Akka.Cluster.Metrics.Tests"]
    Akka_Cluster_Metrics_Tests -.-> Akka_Cluster_Tests
```

## Project References
- Akka.Cluster
- Akka.Coordination.Tests
- Akka.Tests.Shared.Internals

## Consumed By
- Akka.Cluster.Metrics.Tests

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.NET.Test.Sdk | 17.9.0 |
| xunit | 2.8.1 |
| xunit.runner.visualstudio | 2.8.1 |
| FsCheck.Xunit | 2.16.6 |
| FluentAssertions | 5.10.3 |
| Fsharp.Core | 6.0.5 |


---

*[Back to Index](../index.md)*
