# Akka.Serialization.TestKit

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/contrib/serializers/Akka.Serialization.TestKit/Akka.Serialization.TestKit.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Serialization_TestKit["<strong>Akka.Serialization.TestKit</strong>"]
    Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    Akka_Serialization_TestKit --> Akka_Tests_Shared_Internals
    Akka_Serialization_Hyperion_Tests["Akka.Serialization.Hyperion.Tests"]
    Akka_Serialization_Hyperion_Tests -.-> Akka_Serialization_TestKit
```

## Project References
- Akka.Tests.Shared.Internals

## Consumed By
- Akka.Serialization.Hyperion.Tests


---

*[Back to Index](../index.md)*
