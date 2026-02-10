# OrchardCore.Application.Targets

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Application.Targets/OrchardCore.Application.Targets.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Application_Targets["<strong>OrchardCore.Application.Targets</strong>"]
    OrchardCore["OrchardCore"]
    OrchardCore_Application_Targets --> OrchardCore
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Application_Targets
    OrchardCore_Application_Mvc_Targets["OrchardCore.Application.Mvc.Targets"]
    OrchardCore_Application_Mvc_Targets -.-> OrchardCore_Application_Targets
```

## Project References
- OrchardCore

## Consumed By
- OrchardCore.Application.Cms.Core.Targets
- OrchardCore.Application.Mvc.Targets


---

*[Back to Index](../../index.md)*
