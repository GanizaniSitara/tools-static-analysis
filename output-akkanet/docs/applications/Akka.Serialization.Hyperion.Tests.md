# Akka.Serialization.Hyperion.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/contrib/serializers/Akka.Serialization.Hyperion.Tests/Akka.Serialization.Hyperion.Tests.csproj` |
| Project References | 3 |
| NuGet Dependencies | 4 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Serialization_Hyperion_Tests["<strong>Akka.Serialization.Hyperion.Tests</strong>"]
    Akka_Serialization_Hyperion["Akka.Serialization.Hyperion"]
    Akka_Serialization_Hyperion_Tests --> Akka_Serialization_Hyperion
    Akka_Serialization_TestKit["Akka.Serialization.TestKit"]
    Akka_Serialization_Hyperion_Tests --> Akka_Serialization_TestKit
    Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    Akka_Serialization_Hyperion_Tests --> Akka_Tests_Shared_Internals
```

## Project References
- Akka.Serialization.Hyperion
- Akka.Serialization.TestKit
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
