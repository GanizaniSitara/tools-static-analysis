# OrchardCore.Setup.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Setup.Abstractions/OrchardCore.Setup.Abstractions.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Setup_Abstractions["<strong>OrchardCore.Setup.Abstractions</strong>"]
    OrchardCore_Abstractions["OrchardCore.Abstractions"]
    OrchardCore_Setup_Abstractions --> OrchardCore_Abstractions
    OrchardCore_Recipes_Abstractions["OrchardCore.Recipes.Abstractions"]
    OrchardCore_Setup_Abstractions --> OrchardCore_Recipes_Abstractions
    OrchardCore_Settings["OrchardCore.Settings"]
    OrchardCore_Settings -.-> OrchardCore_Setup_Abstractions
    OrchardCore_Users["OrchardCore.Users"]
    OrchardCore_Users -.-> OrchardCore_Setup_Abstractions
    OrchardCore_AutoSetup["OrchardCore.AutoSetup"]
    OrchardCore_AutoSetup -.-> OrchardCore_Setup_Abstractions
    OrchardCore_Tenants["OrchardCore.Tenants"]
    OrchardCore_Tenants -.-> OrchardCore_Setup_Abstractions
    OrchardCore_Setup_Core["OrchardCore.Setup.Core"]
    OrchardCore_Setup_Core -.-> OrchardCore_Setup_Abstractions
```

## Project References
- OrchardCore.Abstractions
- OrchardCore.Recipes.Abstractions

## Consumed By
- OrchardCore.Settings
- OrchardCore.Users
- OrchardCore.AutoSetup
- OrchardCore.Tenants
- OrchardCore.Setup.Core


---

*[Back to Index](../../index.md)*
