# Akka.Streams

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | akka.net |
| Path | `src/core/Akka.Streams/Akka.Streams.csproj` |
| Project References | 1 |
| NuGet Dependencies | 5 |
| Consumers | 10 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Streams["<strong>Akka.Streams</strong>"]
    Akka["Akka"]
    Akka_Streams --> Akka
    Akka_Benchmarks["Akka.Benchmarks"]
    Akka_Benchmarks -.-> Akka_Streams
    StreamsExamples["StreamsExamples"]
    StreamsExamples -.-> Akka_Streams
    Akka_Docs_Tests["Akka.Docs.Tests"]
    Akka_Docs_Tests -.-> Akka_Streams
    Akka_Streams_Tests["Akka.Streams.Tests"]
    Akka_Streams_Tests -.-> Akka_Streams
    Akka_Streams_TestKit["Akka.Streams.TestKit"]
    Akka_Streams_TestKit -.-> Akka_Streams
    Akka_Streams_Tests_TCK["Akka.Streams.Tests.TCK"]
    Akka_Streams_Tests_TCK -.-> Akka_Streams
    Akka_API_Tests["Akka.API.Tests"]
    Akka_API_Tests -.-> Akka_Streams
    Akka_Persistence_Query["Akka.Persistence.Query"]
    Akka_Persistence_Query -.-> Akka_Streams
    Akka_Docs_Tutorials["Akka.Docs.Tutorials"]
    Akka_Docs_Tutorials -.-> Akka_Streams
    Akka_Streams_Tests_Performance["Akka.Streams.Tests.Performance"]
    Akka_Streams_Tests_Performance -.-> Akka_Streams
```

## Project References
- Akka

## Consumed By
- Akka.Benchmarks
- StreamsExamples
- Akka.Docs.Tests
- Akka.Streams.Tests
- Akka.Streams.TestKit
- Akka.Streams.Tests.TCK
- Akka.API.Tests
- Akka.Persistence.Query
- Akka.Docs.Tutorials
- Akka.Streams.Tests.Performance

## External NuGet Packages
| Package | Version |
|---------|---------||
| System.Reflection.TypeExtensions | 4.7.0 |
| Microsoft.Bcl.AsyncInterfaces | [6.0.*,) |
| Google.Protobuf | 3.26.1 |
| Reactive.Streams | 1.0.4 |
| Grpc.Tools | 2.60.0 |


---

*[Back to Index](../index.md)*
