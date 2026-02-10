# OrchardCore.Recipes.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Recipes.Core/OrchardCore.Recipes.Core.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Recipes_Core["<strong>OrchardCore.Recipes.Core</strong>"]
    OrchardCore_Data_Abstractions["OrchardCore.Data.Abstractions"]
    OrchardCore_Recipes_Core --> OrchardCore_Data_Abstractions
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Recipes_Core --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Recipes_Abstractions["OrchardCore.Recipes.Abstractions"]
    OrchardCore_Recipes_Core --> OrchardCore_Recipes_Abstractions
    OrchardCore_Recipes["OrchardCore.Recipes"]
    OrchardCore_Recipes -.-> OrchardCore_Recipes_Core
```

## Project References
- OrchardCore.Data.Abstractions
- OrchardCore.Infrastructure.Abstractions
- OrchardCore.Recipes.Abstractions

## Consumed By
- OrchardCore.Recipes


---

*[Back to Index](../../index.md)*
