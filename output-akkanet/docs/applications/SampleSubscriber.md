# SampleSubscriber

## Overview

| Property | Value |
|----------|-------|
| Category | Sample |
| Repository | akka.net |
| Path | `src/examples/Cluster/PublishSubscribe/SamplePublishSubscribe/SampleSubscriber.csproj` |
| Project References | 4 |
| NuGet Dependencies | 0 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    SampleSubscriber["<strong>SampleSubscriber</strong>"]
    Akka_Cluster_Tools["Akka.Cluster.Tools"]
    SampleSubscriber --> Akka_Cluster_Tools
    Akka_Cluster["Akka.Cluster"]
    SampleSubscriber --> Akka_Cluster
    Akka_Remote["Akka.Remote"]
    SampleSubscriber --> Akka_Remote
    Akka["Akka"]
    SampleSubscriber --> Akka
```

## Project References
- Akka.Cluster.Tools
- Akka.Cluster
- Akka.Remote
- Akka


---

*[Back to Index](../index.md)*
