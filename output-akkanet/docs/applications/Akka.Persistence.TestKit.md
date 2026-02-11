# Akka.Persistence.TestKit

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/core/Akka.Persistence.TestKit/Akka.Persistence.TestKit.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Persistence_TestKit["<strong>Akka.Persistence.TestKit</strong>"]
    Akka_TestKit_Xunit2["Akka.TestKit.Xunit2"]
    Akka_Persistence_TestKit --> Akka_TestKit_Xunit2
    Akka_Persistence["Akka.Persistence"]
    Akka_Persistence_TestKit --> Akka_Persistence
    Akka_TestKit["Akka.TestKit"]
    Akka_Persistence_TestKit --> Akka_TestKit
    Akka_Persistence_TestKit_Tests["Akka.Persistence.TestKit.Tests"]
    Akka_Persistence_TestKit_Tests -.-> Akka_Persistence_TestKit
    Akka_Persistence_TestKit_Xunit2["Akka.Persistence.TestKit.Xunit2"]
    Akka_Persistence_TestKit_Xunit2 -.-> Akka_Persistence_TestKit
```

## Project References
- Akka.TestKit.Xunit2
- Akka.Persistence
- Akka.TestKit

## Consumed By
- Akka.Persistence.TestKit.Tests
- Akka.Persistence.TestKit.Xunit2


---

*[Back to Index](../index.md)*
