# OrchardCore.HomeRoute

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.HomeRoute/OrchardCore.HomeRoute.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_HomeRoute["<strong>OrchardCore.HomeRoute</strong>"]
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_HomeRoute --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_HomeRoute --> OrchardCore_Module_Targets
    OrchardCore_Mvc_Core["OrchardCore.Mvc.Core"]
    OrchardCore_HomeRoute --> OrchardCore_Mvc_Core
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_HomeRoute
```

## Project References
- OrchardCore.Infrastructure.Abstractions
- OrchardCore.Module.Targets
- OrchardCore.Mvc.Core

## Consumed By
- OrchardCore.Application.Cms.Core.Targets


---

*[Back to Index](../../index.md)*
