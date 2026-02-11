# Akka.Persistence.Query

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | akka.net |
| Path | `src/core/Akka.Persistence.Query/Akka.Persistence.Query.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 4 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Persistence_Query["<strong>Akka.Persistence.Query</strong>"]
    Akka_Persistence["Akka.Persistence"]
    Akka_Persistence_Query --> Akka_Persistence
    Akka_Streams["Akka.Streams"]
    Akka_Persistence_Query --> Akka_Streams
    Akka_Persistence_Query_InMemory["Akka.Persistence.Query.InMemory"]
    Akka_Persistence_Query_InMemory -.-> Akka_Persistence_Query
    Akka_Persistence_Query_Tests["Akka.Persistence.Query.Tests"]
    Akka_Persistence_Query_Tests -.-> Akka_Persistence_Query
    Akka_API_Tests["Akka.API.Tests"]
    Akka_API_Tests -.-> Akka_Persistence_Query
    Akka_Persistence_TCK["Akka.Persistence.TCK"]
    Akka_Persistence_TCK -.-> Akka_Persistence_Query
```

## Project References
- Akka.Persistence
- Akka.Streams

## Consumed By
- Akka.Persistence.Query.InMemory
- Akka.Persistence.Query.Tests
- Akka.API.Tests
- Akka.Persistence.TCK


---

*[Back to Index](../index.md)*
