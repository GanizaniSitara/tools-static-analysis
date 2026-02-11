# Akka.Persistence.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/core/Akka.Persistence.Tests/Akka.Persistence.Tests.csproj` |
| Project References | 5 |
| NuGet Dependencies | 4 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Persistence_Tests["<strong>Akka.Persistence.Tests</strong>"]
    Akka_Serialization_Hyperion["Akka.Serialization.Hyperion"]
    Akka_Persistence_Tests --> Akka_Serialization_Hyperion
    Akka_Persistence_TestKit_Xunit2["Akka.Persistence.TestKit.Xunit2"]
    Akka_Persistence_Tests --> Akka_Persistence_TestKit_Xunit2
    Akka_Persistence["Akka.Persistence"]
    Akka_Persistence_Tests --> Akka_Persistence
    Akka_Remote["Akka.Remote"]
    Akka_Persistence_Tests --> Akka_Remote
    Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    Akka_Persistence_Tests --> Akka_Tests_Shared_Internals
```

## Project References
- Akka.Serialization.Hyperion
- Akka.Persistence.TestKit.Xunit2
- Akka.Persistence
- Akka.Remote
- Akka.Tests.Shared.Internals

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.NET.Test.Sdk | 17.9.0 |
| xunit | 2.8.1 |
| xunit.runner.visualstudio | 2.8.1 |
| FluentAssertions | 5.10.3 |


---

*[Back to Index](../index.md)*
