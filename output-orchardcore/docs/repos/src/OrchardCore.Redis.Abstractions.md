# OrchardCore.Redis.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Redis.Abstractions/OrchardCore.Redis.Abstractions.csproj` |
| Project References | 1 |
| NuGet Dependencies | 3 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Redis_Abstractions["<strong>OrchardCore.Redis.Abstractions</strong>"]
    OrchardCore_Abstractions["OrchardCore.Abstractions"]
    OrchardCore_Redis_Abstractions --> OrchardCore_Abstractions
    OrchardCore_Redis["OrchardCore.Redis"]
    OrchardCore_Redis -.-> OrchardCore_Redis_Abstractions
```

## Project References
- OrchardCore.Abstractions

## Consumed By
- OrchardCore.Redis

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.AspNetCore.DataProtection.StackExchangeRedis |  |
| Microsoft.Extensions.Caching.StackExchangeRedis |  |
| StackExchange.Redis |  |


---

*[Back to Index](../../index.md)*
