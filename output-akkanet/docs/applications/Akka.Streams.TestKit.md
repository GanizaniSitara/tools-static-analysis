# Akka.Streams.TestKit

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/core/Akka.Streams.TestKit/Akka.Streams.TestKit.csproj` |
| Project References | 2 |
| NuGet Dependencies | 1 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Streams_TestKit["<strong>Akka.Streams.TestKit</strong>"]
    Akka_Streams["Akka.Streams"]
    Akka_Streams_TestKit --> Akka_Streams
    Akka_TestKit["Akka.TestKit"]
    Akka_Streams_TestKit --> Akka_TestKit
    Akka_Streams_Tests["Akka.Streams.Tests"]
    Akka_Streams_Tests -.-> Akka_Streams_TestKit
    Akka_Streams_Tests_TCK["Akka.Streams.Tests.TCK"]
    Akka_Streams_Tests_TCK -.-> Akka_Streams_TestKit
    Akka_Persistence_TCK["Akka.Persistence.TCK"]
    Akka_Persistence_TCK -.-> Akka_Streams_TestKit
    Akka_Streams_TestKit_Tests["Akka.Streams.TestKit.Tests"]
    Akka_Streams_TestKit_Tests -.-> Akka_Streams_TestKit
    Akka_Streams_Tests_Performance["Akka.Streams.Tests.Performance"]
    Akka_Streams_Tests_Performance -.-> Akka_Streams_TestKit
```

## Project References
- Akka.Streams
- Akka.TestKit

## Consumed By
- Akka.Streams.Tests
- Akka.Streams.Tests.TCK
- Akka.Persistence.TCK
- Akka.Streams.TestKit.Tests
- Akka.Streams.Tests.Performance

## External NuGet Packages
| Package | Version |
|---------|---------||
| Polyfill | 1.28.0 |


---

*[Back to Index](../index.md)*
