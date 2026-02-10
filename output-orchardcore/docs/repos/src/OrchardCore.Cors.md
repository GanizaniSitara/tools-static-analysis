# OrchardCore.Cors

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.Cors/OrchardCore.Cors.csproj` |
| Project References | 7 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Cors["<strong>OrchardCore.Cors</strong>"]
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_Cors --> OrchardCore_Module_Targets
    OrchardCore_Navigation_Core["OrchardCore.Navigation.Core"]
    OrchardCore_Cors --> OrchardCore_Navigation_Core
    OrchardCore_Admin_Abstractions["OrchardCore.Admin.Abstractions"]
    OrchardCore_Cors --> OrchardCore_Admin_Abstractions
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_Cors --> OrchardCore_DisplayManagement
    OrchardCore_Roles_Abstractions["OrchardCore.Roles.Abstractions"]
    OrchardCore_Cors --> OrchardCore_Roles_Abstractions
    OrchardCore_Users_Core["OrchardCore.Users.Core"]
    OrchardCore_Cors --> OrchardCore_Users_Core
    OrchardCore_ResourceManagement["OrchardCore.ResourceManagement"]
    OrchardCore_Cors --> OrchardCore_ResourceManagement
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Cors
```

## Project References
- OrchardCore.Module.Targets
- OrchardCore.Navigation.Core
- OrchardCore.Admin.Abstractions
- OrchardCore.DisplayManagement
- OrchardCore.Roles.Abstractions
- OrchardCore.Users.Core
- OrchardCore.ResourceManagement

## Consumed By
- OrchardCore.Application.Cms.Core.Targets


---

*[Back to Index](../../index.md)*
