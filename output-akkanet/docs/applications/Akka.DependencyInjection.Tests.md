# Akka.DependencyInjection.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/contrib/dependencyinjection/Akka.DependencyInjection.Tests/Akka.DependencyInjection.Tests.csproj` |
| Project References | 2 |
| NuGet Dependencies | 5 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_DependencyInjection_Tests["<strong>Akka.DependencyInjection.Tests</strong>"]
    Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    Akka_DependencyInjection_Tests --> Akka_Tests_Shared_Internals
    Akka_DependencyInjection["Akka.DependencyInjection"]
    Akka_DependencyInjection_Tests --> Akka_DependencyInjection
```

## Project References
- Akka.Tests.Shared.Internals
- Akka.DependencyInjection

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.Extensions.Hosting | [6.0.*,) |
| Microsoft.NET.Test.Sdk | 17.9.0 |
| xunit | 2.8.1 |
| xunit.runner.visualstudio | 2.8.1 |
| FluentAssertions | 5.10.3 |


---

*[Back to Index](../index.md)*
