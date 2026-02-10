# OrchardCore.DynamicCache.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.DynamicCache.Abstractions/OrchardCore.DynamicCache.Abstractions.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_DynamicCache_Abstractions["<strong>OrchardCore.DynamicCache.Abstractions</strong>"]
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_DynamicCache_Abstractions --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_DynamicCache["OrchardCore.DynamicCache"]
    OrchardCore_DynamicCache -.-> OrchardCore_DynamicCache_Abstractions
    OrchardCore_DisplayManagement_Liquid["OrchardCore.DisplayManagement.Liquid"]
    OrchardCore_DisplayManagement_Liquid -.-> OrchardCore_DynamicCache_Abstractions
```

## Project References
- OrchardCore.Infrastructure.Abstractions

## Consumed By
- OrchardCore.DynamicCache
- OrchardCore.DisplayManagement.Liquid


---

*[Back to Index](../../index.md)*
