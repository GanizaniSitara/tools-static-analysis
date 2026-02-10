# OrchardCore.Feeds

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.Feeds/OrchardCore.Feeds.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Feeds["<strong>OrchardCore.Feeds</strong>"]
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_Feeds --> OrchardCore_DisplayManagement
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_Feeds --> OrchardCore_Module_Targets
    OrchardCore_Feeds_Core["OrchardCore.Feeds.Core"]
    OrchardCore_Feeds --> OrchardCore_Feeds_Core
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Feeds
```

## Project References
- OrchardCore.DisplayManagement
- OrchardCore.Module.Targets
- OrchardCore.Feeds.Core

## Consumed By
- OrchardCore.Application.Cms.Core.Targets


---

*[Back to Index](../../index.md)*
