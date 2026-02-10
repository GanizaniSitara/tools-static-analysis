# OrchardCore.Setup.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Setup.Core/OrchardCore.Setup.Core.csproj` |
| Project References | 4 |
| NuGet Dependencies | 1 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Setup_Core["<strong>OrchardCore.Setup.Core</strong>"]
    OrchardCore_Abstractions["OrchardCore.Abstractions"]
    OrchardCore_Setup_Core --> OrchardCore_Abstractions
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Setup_Core --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Recipes_Abstractions["OrchardCore.Recipes.Abstractions"]
    OrchardCore_Setup_Core --> OrchardCore_Recipes_Abstractions
    OrchardCore_Setup_Abstractions["OrchardCore.Setup.Abstractions"]
    OrchardCore_Setup_Core --> OrchardCore_Setup_Abstractions
    OrchardCore_Setup["OrchardCore.Setup"]
    OrchardCore_Setup -.-> OrchardCore_Setup_Core
    OrchardCore_Tenants["OrchardCore.Tenants"]
    OrchardCore_Tenants -.-> OrchardCore_Setup_Core
```

## Project References
- OrchardCore.Abstractions
- OrchardCore.Infrastructure.Abstractions
- OrchardCore.Recipes.Abstractions
- OrchardCore.Setup.Abstractions

## Consumed By
- OrchardCore.Setup
- OrchardCore.Tenants

## External NuGet Packages
| Package | Version |
|---------|---------||
| YesSql |  |


---

*[Back to Index](../../index.md)*
