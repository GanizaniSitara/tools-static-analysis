# OrchardCore.DynamicCache

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.DynamicCache/OrchardCore.DynamicCache.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_DynamicCache["<strong>OrchardCore.DynamicCache</strong>"]
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_DynamicCache --> OrchardCore_DisplayManagement
    OrchardCore_DynamicCache_Abstractions["OrchardCore.DynamicCache.Abstractions"]
    OrchardCore_DynamicCache --> OrchardCore_DynamicCache_Abstractions
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_DynamicCache --> OrchardCore_Module_Targets
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_DynamicCache
    OrchardCore_Tests["OrchardCore.Tests"]
    OrchardCore_Tests -.-> OrchardCore_DynamicCache
```

## Project References
- OrchardCore.DisplayManagement
- OrchardCore.DynamicCache.Abstractions
- OrchardCore.Module.Targets

## Consumed By
- OrchardCore.Application.Cms.Core.Targets
- OrchardCore.Tests


---

*[Back to Index](../../index.md)*
