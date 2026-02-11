# Shared

## Overview

| Property | Value |
|----------|-------|
| Category | Application |
| Repository | akka.net |
| Path | `src/examples/RemoteDeploy/Shared/Shared.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    Shared["<strong>Shared</strong>"]
    Akka["Akka"]
    Shared --> Akka
    System1["System1"]
    System1 -.-> Shared
    System2["System2"]
    System2 -.-> Shared
```

## Project References
- Akka

## Consumed By
- System1
- System2


---

*[Back to Index](../index.md)*
