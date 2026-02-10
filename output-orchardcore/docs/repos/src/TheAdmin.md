# TheAdmin

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Themes/TheAdmin/TheAdmin.csproj` |
| Project References | 6 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    TheAdmin["<strong>TheAdmin</strong>"]
    OrchardCore_Theme_Targets["OrchardCore.Theme.Targets"]
    TheAdmin --> OrchardCore_Theme_Targets
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    TheAdmin --> OrchardCore_DisplayManagement
    OrchardCore_ResourceManagement["OrchardCore.ResourceManagement"]
    TheAdmin --> OrchardCore_ResourceManagement
    OrchardCore_Admin["OrchardCore.Admin"]
    TheAdmin --> OrchardCore_Admin
    OrchardCore_Themes["OrchardCore.Themes"]
    TheAdmin --> OrchardCore_Themes
    OrchardCore_Users_Core["OrchardCore.Users.Core"]
    TheAdmin --> OrchardCore_Users_Core
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> TheAdmin
```

## Project References
- OrchardCore.Theme.Targets
- OrchardCore.DisplayManagement
- OrchardCore.ResourceManagement
- OrchardCore.Admin
- OrchardCore.Themes
- OrchardCore.Users.Core

## Consumed By
- OrchardCore.Application.Cms.Core.Targets


---

*[Back to Index](../../index.md)*
