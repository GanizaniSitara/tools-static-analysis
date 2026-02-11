# Akka.Persistence.Query.InMemory

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | akka.net |
| Path | `src/contrib/persistence/Akka.Persistence.Query.InMemory/Akka.Persistence.Query.InMemory.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Persistence_Query_InMemory["<strong>Akka.Persistence.Query.InMemory</strong>"]
    Akka_Persistence_Query["Akka.Persistence.Query"]
    Akka_Persistence_Query_InMemory --> Akka_Persistence_Query
    Akka_Persistence_Query_InMemory_Tests["Akka.Persistence.Query.InMemory.Tests"]
    Akka_Persistence_Query_InMemory_Tests -.-> Akka_Persistence_Query_InMemory
    Akka_API_Tests["Akka.API.Tests"]
    Akka_API_Tests -.-> Akka_Persistence_Query_InMemory
```

## Project References
- Akka.Persistence.Query

## Consumed By
- Akka.Persistence.Query.InMemory.Tests
- Akka.API.Tests


---

*[Back to Index](../index.md)*
