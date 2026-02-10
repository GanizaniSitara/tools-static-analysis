# OrchardCore.AuditTrail

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.AuditTrail/OrchardCore.AuditTrail.csproj` |
| Project References | 7 |
| NuGet Dependencies | 2 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_AuditTrail["<strong>OrchardCore.AuditTrail</strong>"]
    OrchardCore_Admin_Abstractions["OrchardCore.Admin.Abstractions"]
    OrchardCore_AuditTrail --> OrchardCore_Admin_Abstractions
    OrchardCore_AuditTrail_Abstractions["OrchardCore.AuditTrail.Abstractions"]
    OrchardCore_AuditTrail --> OrchardCore_AuditTrail_Abstractions
    OrchardCore_Data_YesSql_Abstractions["OrchardCore.Data.YesSql.Abstractions"]
    OrchardCore_AuditTrail --> OrchardCore_Data_YesSql_Abstractions
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_AuditTrail --> OrchardCore_Module_Targets
    OrchardCore_Navigation_Core["OrchardCore.Navigation.Core"]
    OrchardCore_AuditTrail --> OrchardCore_Navigation_Core
    OrchardCore_ResourceManagement["OrchardCore.ResourceManagement"]
    OrchardCore_AuditTrail --> OrchardCore_ResourceManagement
    OrchardCore_Settings_Core["OrchardCore.Settings.Core"]
    OrchardCore_AuditTrail --> OrchardCore_Settings_Core
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_AuditTrail
```

## Project References
- OrchardCore.Admin.Abstractions
- OrchardCore.AuditTrail.Abstractions
- OrchardCore.Data.YesSql.Abstractions
- OrchardCore.Module.Targets
- OrchardCore.Navigation.Core
- OrchardCore.ResourceManagement
- OrchardCore.Settings.Core

## Consumed By
- OrchardCore.Application.Cms.Core.Targets

## External NuGet Packages
| Package | Version |
|---------|---------||
| YesSql.Core |  |
| YesSql.Filters.Query |  |


---

*[Back to Index](../../index.md)*
