# Akka.DependencyInjection

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | akka.net |
| Path | `src/contrib/dependencyinjection/Akka.DependencyInjection/Akka.DependencyInjection.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    Akka_DependencyInjection["<strong>Akka.DependencyInjection</strong>"]
    Akka["Akka"]
    Akka_DependencyInjection --> Akka
    Akka_DependencyInjection_Tests["Akka.DependencyInjection.Tests"]
    Akka_DependencyInjection_Tests -.-> Akka_DependencyInjection
    Akka_AspNetCore["Akka.AspNetCore"]
    Akka_AspNetCore -.-> Akka_DependencyInjection
    Samples_Akka_AspNetCore["Samples.Akka.AspNetCore"]
    Samples_Akka_AspNetCore -.-> Akka_DependencyInjection
    AkkaWindowsService["AkkaWindowsService"]
    AkkaWindowsService -.-> Akka_DependencyInjection
    AkkaHeadlesssService["AkkaHeadlesssService"]
    AkkaHeadlesssService -.-> Akka_DependencyInjection
```

## Project References
- Akka

## Consumed By
- Akka.DependencyInjection.Tests
- Akka.AspNetCore
- Samples.Akka.AspNetCore
- AkkaWindowsService
- AkkaHeadlesssService

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.Extensions.DependencyInjection.Abstractions | [6.0.*,) |


---

*[Back to Index](../index.md)*
