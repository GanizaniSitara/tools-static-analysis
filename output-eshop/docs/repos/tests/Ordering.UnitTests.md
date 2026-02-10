# Ordering.UnitTests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | tests |
| Path | `Ordering.UnitTests/Ordering.UnitTests.csproj` |
| Project References | 3 |
| NuGet Dependencies | 2 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Ordering_UnitTests["<strong>Ordering.UnitTests</strong>"]
    Ordering_API["Ordering.API"]
    Ordering_UnitTests --> Ordering_API
    Ordering_Domain["Ordering.Domain"]
    Ordering_UnitTests --> Ordering_Domain
    Ordering_Infrastructure["Ordering.Infrastructure"]
    Ordering_UnitTests --> Ordering_Infrastructure
```

## Project References
- Ordering.API
- Ordering.Domain
- Ordering.Infrastructure

## External NuGet Packages
| Package | Version |
|---------|---------||
| NSubstitute |  |
| NSubstitute.Analyzers.CSharp |  |


---

*[Back to Index](../../index.md)*
