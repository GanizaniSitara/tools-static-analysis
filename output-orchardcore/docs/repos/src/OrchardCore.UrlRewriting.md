# OrchardCore.UrlRewriting

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.UrlRewriting/OrchardCore.UrlRewriting.csproj` |
| Project References | 5 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_UrlRewriting["<strong>OrchardCore.UrlRewriting</strong>"]
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_UrlRewriting --> OrchardCore_Module_Targets
    OrchardCore_Navigation_Core["OrchardCore.Navigation.Core"]
    OrchardCore_UrlRewriting --> OrchardCore_Navigation_Core
    OrchardCore_Recipes_Abstractions["OrchardCore.Recipes.Abstractions"]
    OrchardCore_UrlRewriting --> OrchardCore_Recipes_Abstractions
    OrchardCore_ResourceManagement["OrchardCore.ResourceManagement"]
    OrchardCore_UrlRewriting --> OrchardCore_ResourceManagement
    OrchardCore_UrlRewriting_Core["OrchardCore.UrlRewriting.Core"]
    OrchardCore_UrlRewriting --> OrchardCore_UrlRewriting_Core
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_UrlRewriting
```

## Project References
- OrchardCore.Module.Targets
- OrchardCore.Navigation.Core
- OrchardCore.Recipes.Abstractions
- OrchardCore.ResourceManagement
- OrchardCore.UrlRewriting.Core

## Consumed By
- OrchardCore.Application.Cms.Core.Targets


---

*[Back to Index](../../index.md)*
