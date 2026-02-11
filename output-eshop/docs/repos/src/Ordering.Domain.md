# Ordering.Domain

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `Ordering.Domain/Ordering.Domain.csproj` |
| Project References | 0 |
| NuGet Dependencies | 2 |
| Consumers | 4 |

## Dependency Diagram

```mermaid
graph TD
    Ordering_Domain["<strong>Ordering.Domain</strong>"]
    Ordering_Infrastructure["Ordering.Infrastructure"]
    Ordering_Infrastructure -.-> Ordering_Domain
    Ordering_API["Ordering.API"]
    Ordering_API -.-> Ordering_Domain
    Ordering_UnitTests["Ordering.UnitTests"]
    Ordering_UnitTests -.-> Ordering_Domain
    Ordering_FunctionalTests["Ordering.FunctionalTests"]
    Ordering_FunctionalTests -.-> Ordering_Domain
```

## Consumed By
- Ordering.Infrastructure
- Ordering.API
- Ordering.UnitTests
- Ordering.FunctionalTests

## External NuGet Packages
| Package | Version |
|---------|---------||
| MediatR |  |
| System.Reflection.TypeExtensions |  |

## Data Access Patterns
### MongoDB.Read
| File | Line | Context |
|------|------|---------||
| `src/Ordering.Domain/SeedWork/ValueObject.cs` | 37 | `.Aggregate((x, y) => x ^ y);` |


---

*[Back to Index](../../index.md)*
