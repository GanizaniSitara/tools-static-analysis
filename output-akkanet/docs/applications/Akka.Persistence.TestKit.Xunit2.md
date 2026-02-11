# Akka.Persistence.TestKit.Xunit2

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/core/Akka.Persistence.TestKit.Xunit2/Akka.Persistence.TestKit.Xunit2.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Persistence_TestKit_Xunit2["<strong>Akka.Persistence.TestKit.Xunit2</strong>"]
    Akka_TestKit_Xunit2["Akka.TestKit.Xunit2"]
    Akka_Persistence_TestKit_Xunit2 --> Akka_TestKit_Xunit2
    Akka_Persistence_TestKit["Akka.Persistence.TestKit"]
    Akka_Persistence_TestKit_Xunit2 --> Akka_Persistence_TestKit
    Akka_TestKit["Akka.TestKit"]
    Akka_Persistence_TestKit_Xunit2 --> Akka_TestKit
    Akka_Persistence_Tests["Akka.Persistence.Tests"]
    Akka_Persistence_Tests -.-> Akka_Persistence_TestKit_Xunit2
    Akka_Persistence_TestKit_Tests["Akka.Persistence.TestKit.Tests"]
    Akka_Persistence_TestKit_Tests -.-> Akka_Persistence_TestKit_Xunit2
```

## Project References
- Akka.TestKit.Xunit2
- Akka.Persistence.TestKit
- Akka.TestKit

## Consumed By
- Akka.Persistence.Tests
- Akka.Persistence.TestKit.Tests


---

*[Back to Index](../index.md)*
