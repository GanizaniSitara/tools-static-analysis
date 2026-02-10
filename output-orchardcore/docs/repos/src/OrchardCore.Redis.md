# OrchardCore.Redis

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.Redis/OrchardCore.Redis.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Redis["<strong>OrchardCore.Redis</strong>"]
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Redis --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_Redis --> OrchardCore_Module_Targets
    OrchardCore_Redis_Abstractions["OrchardCore.Redis.Abstractions"]
    OrchardCore_Redis --> OrchardCore_Redis_Abstractions
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Redis
```

## Project References
- OrchardCore.Infrastructure.Abstractions
- OrchardCore.Module.Targets
- OrchardCore.Redis.Abstractions

## Consumed By
- OrchardCore.Application.Cms.Core.Targets


---

*[Back to Index](../../index.md)*
