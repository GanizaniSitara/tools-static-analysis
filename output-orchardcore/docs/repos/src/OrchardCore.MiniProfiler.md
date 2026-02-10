# OrchardCore.MiniProfiler

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.MiniProfiler/OrchardCore.MiniProfiler.csproj` |
| Project References | 2 |
| NuGet Dependencies | 2 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_MiniProfiler["<strong>OrchardCore.MiniProfiler</strong>"]
    OrchardCore_Admin_Abstractions["OrchardCore.Admin.Abstractions"]
    OrchardCore_MiniProfiler --> OrchardCore_Admin_Abstractions
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_MiniProfiler --> OrchardCore_DisplayManagement
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_MiniProfiler
```

## Project References
- OrchardCore.Admin.Abstractions
- OrchardCore.DisplayManagement

## Consumed By
- OrchardCore.Application.Cms.Core.Targets

## External NuGet Packages
| Package | Version |
|---------|---------||
| MiniProfiler.AspNetCore.Mvc |  |
| YesSql.Abstractions |  |


---

*[Back to Index](../../index.md)*
