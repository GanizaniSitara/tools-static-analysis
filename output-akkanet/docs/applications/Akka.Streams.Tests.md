# Akka.Streams.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/core/Akka.Streams.Tests/Akka.Streams.Tests.csproj` |
| Project References | 4 |
| NuGet Dependencies | 6 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Streams_Tests["<strong>Akka.Streams.Tests</strong>"]
    Akka_Remote["Akka.Remote"]
    Akka_Streams_Tests --> Akka_Remote
    Akka_Streams["Akka.Streams"]
    Akka_Streams_Tests --> Akka_Streams
    Akka_Streams_TestKit["Akka.Streams.TestKit"]
    Akka_Streams_Tests --> Akka_Streams_TestKit
    Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    Akka_Streams_Tests --> Akka_Tests_Shared_Internals
    Akka_Streams_Tests_Performance["Akka.Streams.Tests.Performance"]
    Akka_Streams_Tests_Performance -.-> Akka_Streams_Tests
```

## Project References
- Akka.Remote
- Akka.Streams
- Akka.Streams.TestKit
- Akka.Tests.Shared.Internals

## Consumed By
- Akka.Streams.Tests.Performance

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.NET.Test.Sdk | 17.9.0 |
| xunit | 2.8.1 |
| xunit.runner.visualstudio | 2.8.1 |
| FluentAssertions | 5.10.3 |
| System.Net.Sockets | 4.3.0 |
| System.Runtime.Extensions | 4.3.1 |


---

*[Back to Index](../index.md)*
