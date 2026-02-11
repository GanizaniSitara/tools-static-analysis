# Akka.TestKit.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/core/Akka.TestKit.Tests/Akka.TestKit.Tests.csproj` |
| Project References | 4 |
| NuGet Dependencies | 4 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_TestKit_Tests["<strong>Akka.TestKit.Tests</strong>"]
    Akka["Akka"]
    Akka_TestKit_Tests --> Akka
    Akka_TestKit["Akka.TestKit"]
    Akka_TestKit_Tests --> Akka_TestKit
    Akka_TestKit_Xunit2["Akka.TestKit.Xunit2"]
    Akka_TestKit_Tests --> Akka_TestKit_Xunit2
    Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    Akka_TestKit_Tests --> Akka_Tests_Shared_Internals
```

## Project References
- Akka
- Akka.TestKit
- Akka.TestKit.Xunit2
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
