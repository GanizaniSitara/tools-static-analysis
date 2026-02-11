# AkkaWindowsService

## Overview

| Property | Value |
|----------|-------|
| Category | Service |
| Repository | akka.net |
| Path | `src/examples/WindowsService/AkkaWindowsService/AkkaWindowsService.csproj` |
| Project References | 2 |
| NuGet Dependencies | 2 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    AkkaWindowsService["<strong>AkkaWindowsService</strong>"]
    Akka_DependencyInjection["Akka.DependencyInjection"]
    AkkaWindowsService --> Akka_DependencyInjection
    Akka["Akka"]
    AkkaWindowsService --> Akka
```

## Project References
- Akka.DependencyInjection
- Akka

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.Extensions.Hosting.WindowsServices | [6.0.*,) |
| Microsoft.Extensions.Http | [6.0.*,) |


---

*[Back to Index](../index.md)*
