# Akka.Cluster.Metrics.Tests.MultiNode

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/contrib/cluster/Akka.Cluster.Metrics.Tests.MultiNode/Akka.Cluster.Metrics.Tests.MultiNode.csproj` |
| Project References | 3 |
| NuGet Dependencies | 5 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Cluster_Metrics_Tests_MultiNode["<strong>Akka.Cluster.Metrics.Tests.MultiNode</strong>"]
    Akka_Cluster_Metrics_Tests["Akka.Cluster.Metrics.Tests"]
    Akka_Cluster_Metrics_Tests_MultiNode --> Akka_Cluster_Metrics_Tests
    Akka_Cluster_Metrics["Akka.Cluster.Metrics"]
    Akka_Cluster_Metrics_Tests_MultiNode --> Akka_Cluster_Metrics
    Akka_Cluster_TestKit["Akka.Cluster.TestKit"]
    Akka_Cluster_Metrics_Tests_MultiNode --> Akka_Cluster_TestKit
```

## Project References
- Akka.Cluster.Metrics.Tests
- Akka.Cluster.Metrics
- Akka.Cluster.TestKit

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
