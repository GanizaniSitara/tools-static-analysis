# OrchardCore.Setup

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.Setup/OrchardCore.Setup.csproj` |
| Project References | 7 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Setup["<strong>OrchardCore.Setup</strong>"]
    OrchardCore_Data["OrchardCore.Data"]
    OrchardCore_Setup --> OrchardCore_Data
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_Setup --> OrchardCore_DisplayManagement
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Setup --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Localization_Core["OrchardCore.Localization.Core"]
    OrchardCore_Setup --> OrchardCore_Localization_Core
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_Setup --> OrchardCore_Module_Targets
    OrchardCore_Recipes_Abstractions["OrchardCore.Recipes.Abstractions"]
    OrchardCore_Setup --> OrchardCore_Recipes_Abstractions
    OrchardCore_Setup_Core["OrchardCore.Setup.Core"]
    OrchardCore_Setup --> OrchardCore_Setup_Core
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Setup
```

## Project References
- OrchardCore.Data
- OrchardCore.DisplayManagement
- OrchardCore.Infrastructure.Abstractions
- OrchardCore.Localization.Core
- OrchardCore.Module.Targets
- OrchardCore.Recipes.Abstractions
- OrchardCore.Setup.Core

## Consumed By
- OrchardCore.Application.Cms.Core.Targets


---

*[Back to Index](../../index.md)*
