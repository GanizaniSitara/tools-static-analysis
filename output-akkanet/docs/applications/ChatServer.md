# ChatServer

## Overview

| Property | Value |
|----------|-------|
| Category | Application |
| Repository | akka.net |
| Path | `src/examples/Chat/ChatServer/ChatServer.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    ChatServer["<strong>ChatServer</strong>"]
    Akka_Remote["Akka.Remote"]
    ChatServer --> Akka_Remote
    ChatMessages["ChatMessages"]
    ChatServer --> ChatMessages
```

## Project References
- Akka.Remote
- ChatMessages


---

*[Back to Index](../index.md)*
