# Akka.Persistence.TestKit.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/core/Akka.Persistence.TestKit.Tests/Akka.Persistence.TestKit.Tests.csproj` |
| Project References | 3 |
| NuGet Dependencies | 5 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Persistence_TestKit_Tests["<strong>Akka.Persistence.TestKit.Tests</strong>"]
    Akka_Persistence_TestKit["Akka.Persistence.TestKit"]
    Akka_Persistence_TestKit_Tests --> Akka_Persistence_TestKit
    Akka_Persistence_TestKit_Xunit2["Akka.Persistence.TestKit.Xunit2"]
    Akka_Persistence_TestKit_Tests --> Akka_Persistence_TestKit_Xunit2
    Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    Akka_Persistence_TestKit_Tests --> Akka_Tests_Shared_Internals
```

## Project References
- Akka.Persistence.TestKit
- Akka.Persistence.TestKit.Xunit2
- Akka.Tests.Shared.Internals

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.NET.Test.Sdk | 17.9.0 |
| xunit | 2.8.1 |
| xunit.runner.visualstudio | 2.8.1 |
| TeamCity.ServiceMessages | 3.0.13 |
| FluentAssertions | 5.10.3 |


---

*[Back to Index](../index.md)*
