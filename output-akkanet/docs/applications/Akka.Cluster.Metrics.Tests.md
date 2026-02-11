# Akka.Cluster.Metrics.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/contrib/cluster/Akka.Cluster.Metrics.Tests/Akka.Cluster.Metrics.Tests.csproj` |
| Project References | 2 |
| NuGet Dependencies | 4 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Cluster_Metrics_Tests["<strong>Akka.Cluster.Metrics.Tests</strong>"]
    Akka_Cluster_Metrics["Akka.Cluster.Metrics"]
    Akka_Cluster_Metrics_Tests --> Akka_Cluster_Metrics
    Akka_Cluster_Tests["Akka.Cluster.Tests"]
    Akka_Cluster_Metrics_Tests --> Akka_Cluster_Tests
    Akka_Cluster_Metrics_Tests_MultiNode["Akka.Cluster.Metrics.Tests.MultiNode"]
    Akka_Cluster_Metrics_Tests_MultiNode -.-> Akka_Cluster_Metrics_Tests
```

## Project References
- Akka.Cluster.Metrics
- Akka.Cluster.Tests

## Consumed By
- Akka.Cluster.Metrics.Tests.MultiNode

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.NET.Test.Sdk | 17.9.0 |
| xunit | 2.8.1 |
| xunit.runner.visualstudio | 2.8.1 |
| FluentAssertions | 5.10.3 |


---

*[Back to Index](../index.md)*
