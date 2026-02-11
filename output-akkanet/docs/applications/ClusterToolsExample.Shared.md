# ClusterToolsExample.Shared

## Overview

| Property | Value |
|----------|-------|
| Category | Sample |
| Repository | akka.net |
| Path | `src/examples/Cluster/ClusterTools/ClusterToolsExample.Shared/ClusterToolsExample.Shared.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    ClusterToolsExample_Shared["<strong>ClusterToolsExample.Shared</strong>"]
    Akka_Cluster_Tools["Akka.Cluster.Tools"]
    ClusterToolsExample_Shared --> Akka_Cluster_Tools
    ClusterToolsExample_Seed["ClusterToolsExample.Seed"]
    ClusterToolsExample_Seed -.-> ClusterToolsExample_Shared
    ClusterToolsExample_Node["ClusterToolsExample.Node"]
    ClusterToolsExample_Node -.-> ClusterToolsExample_Shared
```

## Project References
- Akka.Cluster.Tools

## Consumed By
- ClusterToolsExample.Seed
- ClusterToolsExample.Node


---

*[Back to Index](../index.md)*
