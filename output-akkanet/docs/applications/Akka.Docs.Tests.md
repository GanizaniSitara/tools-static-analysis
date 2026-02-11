# Akka.Docs.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/core/Akka.Docs.Tests/Akka.Docs.Tests.csproj` |
| Project References | 8 |
| NuGet Dependencies | 4 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Docs_Tests["<strong>Akka.Docs.Tests</strong>"]
    Akka_Cluster_Metrics["Akka.Cluster.Metrics"]
    Akka_Docs_Tests --> Akka_Cluster_Metrics
    Akka_Coordination_Tests["Akka.Coordination.Tests"]
    Akka_Docs_Tests --> Akka_Coordination_Tests
    Akka["Akka"]
    Akka_Docs_Tests --> Akka
    Akka_Persistence["Akka.Persistence"]
    Akka_Docs_Tests --> Akka_Persistence
    Akka_Streams["Akka.Streams"]
    Akka_Docs_Tests --> Akka_Streams
    Akka_TestKit["Akka.TestKit"]
    Akka_Docs_Tests --> Akka_TestKit
    Akka_Cluster_Tools["Akka.Cluster.Tools"]
    Akka_Docs_Tests --> Akka_Cluster_Tools
    Akka_TestKit_Xunit2["Akka.TestKit.Xunit2"]
    Akka_Docs_Tests --> Akka_TestKit_Xunit2
```

## Project References
- Akka.Cluster.Metrics
- Akka.Coordination.Tests
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
| Microsoft.NET.Test.Sdk | 17.9.0 |
| xunit | 2.8.1 |
| xunit.runner.visualstudio | 2.8.1 |


---

*[Back to Index](../index.md)*
