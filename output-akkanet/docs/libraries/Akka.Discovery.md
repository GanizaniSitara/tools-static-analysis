# Akka.Discovery

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | akka.net |
| Path | `src/core/Akka.Discovery/Akka.Discovery.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Discovery["<strong>Akka.Discovery</strong>"]
    Akka["Akka"]
    Akka_Discovery --> Akka
    Akka_Cluster_Tools["Akka.Cluster.Tools"]
    Akka_Cluster_Tools -.-> Akka_Discovery
    Akka_Discovery_Tests["Akka.Discovery.Tests"]
    Akka_Discovery_Tests -.-> Akka_Discovery
    Akka_API_Tests["Akka.API.Tests"]
    Akka_API_Tests -.-> Akka_Discovery
```

## Project References
- Akka

## Consumed By
- Akka.Cluster.Tools
- Akka.Discovery.Tests
- Akka.API.Tests


---

*[Back to Index](../index.md)*
