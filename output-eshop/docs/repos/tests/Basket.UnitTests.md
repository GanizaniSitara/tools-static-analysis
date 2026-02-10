# Basket.UnitTests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | tests |
| Path | `Basket.UnitTests/Basket.UnitTests.csproj` |
| Project References | 1 |
| NuGet Dependencies | 4 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Basket_UnitTests["<strong>Basket.UnitTests</strong>"]
    Basket_API["Basket.API"]
    Basket_UnitTests --> Basket_API
```

## Project References
- Basket.API

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.AspNetCore.Mvc.Testing |  |
| Microsoft.Extensions.Identity.Stores |  |
| NSubstitute |  |
| NSubstitute.Analyzers.CSharp |  |

## Data Access Patterns
### gRPC
| File | Line | Context |
|------|------|---------||
| `tests/Basket.UnitTests/Helpers/TestServerCallContext.cs` | 1 | `﻿using Grpc.Core;` |


---

*[Back to Index](../../index.md)*
