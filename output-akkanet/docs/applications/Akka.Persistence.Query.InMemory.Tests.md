# Akka.Persistence.Query.InMemory.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/contrib/persistence/Akka.Persistence.Query.InMemory.Tests/Akka.Persistence.Query.InMemory.Tests.csproj` |
| Project References | 2 |
| NuGet Dependencies | 4 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Persistence_Query_InMemory_Tests["<strong>Akka.Persistence.Query.InMemory.Tests</strong>"]
    Akka_Persistence_TCK["Akka.Persistence.TCK"]
    Akka_Persistence_Query_InMemory_Tests --> Akka_Persistence_TCK
    Akka_Persistence_Query_InMemory["Akka.Persistence.Query.InMemory"]
    Akka_Persistence_Query_InMemory_Tests --> Akka_Persistence_Query_InMemory
```

## Project References
- Akka.Persistence.TCK
- Akka.Persistence.Query.InMemory

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.NET.Test.Sdk | 17.9.0 |
| xunit | 2.8.1 |
| xunit.runner.visualstudio | 2.8.1 |
| FluentAssertions | 5.10.3 |


---

*[Back to Index](../index.md)*
