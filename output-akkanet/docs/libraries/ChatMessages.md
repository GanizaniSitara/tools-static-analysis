# ChatMessages

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | akka.net |
| Path | `src/examples/Chat/ChatMessages/ChatMessages.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    ChatMessages["<strong>ChatMessages</strong>"]
    Akka["Akka"]
    ChatMessages --> Akka
    ChatClient["ChatClient"]
    ChatClient -.-> ChatMessages
    ChatServer["ChatServer"]
    ChatServer -.-> ChatMessages
```

## Project References
- Akka

## Consumed By
- ChatClient
- ChatServer


---

*[Back to Index](../index.md)*
