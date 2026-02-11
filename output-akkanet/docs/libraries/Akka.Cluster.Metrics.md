# Akka.Cluster.Metrics

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | akka.net |
| Path | `src/contrib/cluster/Akka.Cluster.Metrics/Akka.Cluster.Metrics.csproj` |
| Project References | 1 |
| NuGet Dependencies | 2 |
| Consumers | 7 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Cluster_Metrics["<strong>Akka.Cluster.Metrics</strong>"]
    Akka_Cluster["Akka.Cluster"]
    Akka_Cluster_Metrics --> Akka_Cluster
    Akka_Cluster_Metrics_Tests["Akka.Cluster.Metrics.Tests"]
    Akka_Cluster_Metrics_Tests -.-> Akka_Cluster_Metrics
    Akka_Cluster_Metrics_Tests_MultiNode["Akka.Cluster.Metrics.Tests.MultiNode"]
    Akka_Cluster_Metrics_Tests_MultiNode -.-> Akka_Cluster_Metrics
    Samples_Cluster_Metrics_Common["Samples.Cluster.Metrics.Common"]
    Samples_Cluster_Metrics_Common -.-> Akka_Cluster_Metrics
    Samples_Cluster_Metrics["Samples.Cluster.Metrics"]
    Samples_Cluster_Metrics -.-> Akka_Cluster_Metrics
    Samples_Cluster_AdaptiveGroup["Samples.Cluster.AdaptiveGroup"]
    Samples_Cluster_AdaptiveGroup -.-> Akka_Cluster_Metrics
    Akka_Docs_Tests["Akka.Docs.Tests"]
    Akka_Docs_Tests -.-> Akka_Cluster_Metrics
    Akka_API_Tests["Akka.API.Tests"]
    Akka_API_Tests -.-> Akka_Cluster_Metrics
```

## Project References
- Akka.Cluster

## Consumed By
- Akka.Cluster.Metrics.Tests
- Akka.Cluster.Metrics.Tests.MultiNode
- Samples.Cluster.Metrics.Common
- Samples.Cluster.Metrics
- Samples.Cluster.AdaptiveGroup
- Akka.Docs.Tests
- Akka.API.Tests

## External NuGet Packages
| Package | Version |
|---------|---------||
| System.Diagnostics.Process | 4.3.0 |
| Grpc.Tools | 2.60.0 |


---

*[Back to Index](../index.md)*
