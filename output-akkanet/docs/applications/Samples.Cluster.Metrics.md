# Samples.Cluster.Metrics

## Overview

| Property | Value |
|----------|-------|
| Category | Sample |
| Repository | akka.net |
| Path | `src/examples/Cluster/Metrics/Samples.Cluster.Metrics/Samples.Cluster.Metrics.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Samples_Cluster_Metrics["<strong>Samples.Cluster.Metrics</strong>"]
    Akka_Cluster_Metrics["Akka.Cluster.Metrics"]
    Samples_Cluster_Metrics --> Akka_Cluster_Metrics
    Akka_Cluster_Tools["Akka.Cluster.Tools"]
    Samples_Cluster_Metrics --> Akka_Cluster_Tools
    Samples_Cluster_Metrics_Common["Samples.Cluster.Metrics.Common"]
    Samples_Cluster_Metrics --> Samples_Cluster_Metrics_Common
```

## Project References
- Akka.Cluster.Metrics
- Akka.Cluster.Tools
- Samples.Cluster.Metrics.Common


---

*[Back to Index](../index.md)*
