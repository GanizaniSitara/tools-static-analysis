# Akka.Docs.Tutorials

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/core/Akka.Docs.Tutorials/Akka.Docs.Tutorials.csproj` |
| Project References | 6 |
| NuGet Dependencies | 3 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Docs_Tutorials["<strong>Akka.Docs.Tutorials</strong>"]
    Akka["Akka"]
    Akka_Docs_Tutorials --> Akka
    Akka_Persistence["Akka.Persistence"]
    Akka_Docs_Tutorials --> Akka_Persistence
    Akka_Streams["Akka.Streams"]
    Akka_Docs_Tutorials --> Akka_Streams
    Akka_TestKit["Akka.TestKit"]
    Akka_Docs_Tutorials --> Akka_TestKit
    Akka_Cluster_Tools["Akka.Cluster.Tools"]
    Akka_Docs_Tutorials --> Akka_Cluster_Tools
    Akka_TestKit_Xunit2["Akka.TestKit.Xunit2"]
    Akka_Docs_Tutorials --> Akka_TestKit_Xunit2
```

## Project References
- Akka
- Akka.Persistence
- Akka.Streams
- Akka.TestKit
- Akka.Cluster.Tools
- Akka.TestKit.Xunit2

## External NuGet Packages
| Package | Version |
|---------|---------||
| FluentAssertions | 5.10.3 |
| xunit | 2.8.1 |
| xunit.runner.visualstudio | 2.8.1 |


---

*[Back to Index](../index.md)*
