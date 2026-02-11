# System2

## Overview

| Property | Value |
|----------|-------|
| Category | Application |
| Repository | akka.net |
| Path | `src/examples/RemoteDeploy/System2/System2.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    System2["<strong>System2</strong>"]
    Akka_Remote["Akka.Remote"]
    System2 --> Akka_Remote
    Akka["Akka"]
    System2 --> Akka
    Shared["Shared"]
    System2 --> Shared
```

## Project References
- Akka.Remote
- Akka
- Shared


---

*[Back to Index](../index.md)*
