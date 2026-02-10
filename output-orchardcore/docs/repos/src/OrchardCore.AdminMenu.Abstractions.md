# OrchardCore.AdminMenu.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.AdminMenu.Abstractions/OrchardCore.AdminMenu.Abstractions.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_AdminMenu_Abstractions["<strong>OrchardCore.AdminMenu.Abstractions</strong>"]
    OrchardCore_Navigation_Core["OrchardCore.Navigation.Core"]
    OrchardCore_AdminMenu_Abstractions --> OrchardCore_Navigation_Core
    OrchardCore_AdminMenu["OrchardCore.AdminMenu"]
    OrchardCore_AdminMenu -.-> OrchardCore_AdminMenu_Abstractions
    OrchardCore_Lists["OrchardCore.Lists"]
    OrchardCore_Lists -.-> OrchardCore_AdminMenu_Abstractions
    OrchardCore_Contents["OrchardCore.Contents"]
    OrchardCore_Contents -.-> OrchardCore_AdminMenu_Abstractions
```

## Project References
- OrchardCore.Navigation.Core

## Consumed By
- OrchardCore.AdminMenu
- OrchardCore.Lists
- OrchardCore.Contents


---

*[Back to Index](../../index.md)*
