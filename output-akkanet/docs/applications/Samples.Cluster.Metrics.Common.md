# Samples.Cluster.Metrics.Common

## Overview

| Property | Value |
|----------|-------|
| Category | Sample |
| Repository | akka.net |
| Path | `src/examples/Cluster/Metrics/Samples.Cluster.Metrics.Common/Samples.Cluster.Metrics.Common.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    Samples_Cluster_Metrics_Common["<strong>Samples.Cluster.Metrics.Common</strong>"]
    Akka_Cluster_Metrics["Akka.Cluster.Metrics"]
    Samples_Cluster_Metrics_Common --> Akka_Cluster_Metrics
    Samples_Cluster_Metrics["Samples.Cluster.Metrics"]
    Samples_Cluster_Metrics -.-> Samples_Cluster_Metrics_Common
    Samples_Cluster_AdaptiveGroup["Samples.Cluster.AdaptiveGroup"]
    Samples_Cluster_AdaptiveGroup -.-> Samples_Cluster_Metrics_Common
```

## Project References
- Akka.Cluster.Metrics

## Consumed By
- Samples.Cluster.Metrics
- Samples.Cluster.AdaptiveGroup


---

*[Back to Index](../index.md)*
