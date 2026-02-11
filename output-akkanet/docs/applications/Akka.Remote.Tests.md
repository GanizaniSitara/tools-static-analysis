# Akka.Remote.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/core/Akka.Remote.Tests/Akka.Remote.Tests.csproj` |
| Project References | 3 |
| NuGet Dependencies | 6 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Remote_Tests["<strong>Akka.Remote.Tests</strong>"]
    Akka_Serialization_Hyperion["Akka.Serialization.Hyperion"]
    Akka_Remote_Tests --> Akka_Serialization_Hyperion
    Akka_Remote["Akka.Remote"]
    Akka_Remote_Tests --> Akka_Remote
    Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    Akka_Remote_Tests --> Akka_Tests_Shared_Internals
```

## Project References
- Akka.Serialization.Hyperion
- Akka.Remote
- Akka.Tests.Shared.Internals

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.NET.Test.Sdk | 17.9.0 |
| xunit | 2.8.1 |
| xunit.runner.visualstudio | 2.8.1 |
| FluentAssertions | 5.10.3 |
| FsCheck | 2.16.6 |
| FsCheck.Xunit | 2.16.6 |


---

*[Back to Index](../index.md)*
