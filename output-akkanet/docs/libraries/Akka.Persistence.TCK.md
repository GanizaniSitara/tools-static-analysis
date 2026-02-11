# Akka.Persistence.TCK

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | akka.net |
| Path | `src/core/Akka.Persistence.TCK/Akka.Persistence.TCK.csproj` |
| Project References | 4 |
| NuGet Dependencies | 2 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Persistence_TCK["<strong>Akka.Persistence.TCK</strong>"]
    Akka_Persistence_Query["Akka.Persistence.Query"]
    Akka_Persistence_TCK --> Akka_Persistence_Query
    Akka_Persistence["Akka.Persistence"]
    Akka_Persistence_TCK --> Akka_Persistence
    Akka_TestKit_Xunit2["Akka.TestKit.Xunit2"]
    Akka_Persistence_TCK --> Akka_TestKit_Xunit2
    Akka_Streams_TestKit["Akka.Streams.TestKit"]
    Akka_Persistence_TCK --> Akka_Streams_TestKit
    Akka_Persistence_Query_InMemory_Tests["Akka.Persistence.Query.InMemory.Tests"]
    Akka_Persistence_Query_InMemory_Tests -.-> Akka_Persistence_TCK
    Akka_Persistence_Custom_Tests["Akka.Persistence.Custom.Tests"]
    Akka_Persistence_Custom_Tests -.-> Akka_Persistence_TCK
    Akka_Persistence_TCK_Tests["Akka.Persistence.TCK.Tests"]
    Akka_Persistence_TCK_Tests -.-> Akka_Persistence_TCK
```

## Project References
- Akka.Persistence.Query
- Akka.Persistence
- Akka.TestKit.Xunit2
- Akka.Streams.TestKit

## Consumed By
- Akka.Persistence.Query.InMemory.Tests
- Akka.Persistence.Custom.Tests
- Akka.Persistence.TCK.Tests

## External NuGet Packages
| Package | Version |
|---------|---------||
| FluentAssertions | 5.10.3 |
| MathNet.Numerics | 5.0.0 |


---

*[Back to Index](../index.md)*
