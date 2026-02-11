# System1

## Overview

| Property | Value |
|----------|-------|
| Category | Application |
| Repository | akka.net |
| Path | `src/examples/RemoteDeploy/System1/System1.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    System1["<strong>System1</strong>"]
    Akka_Remote["Akka.Remote"]
    System1 --> Akka_Remote
    Akka["Akka"]
    System1 --> Akka
    Shared["Shared"]
    System1 --> Shared
```

## Project References
- Akka.Remote
- Akka
- Shared


---

*[Back to Index](../index.md)*
