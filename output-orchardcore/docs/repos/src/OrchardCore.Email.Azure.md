# OrchardCore.Email.Azure

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.Email.Azure/OrchardCore.Email.Azure.csproj` |
| Project References | 5 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Email_Azure["<strong>OrchardCore.Email.Azure</strong>"]
    OrchardCore_Admin_Abstractions["OrchardCore.Admin.Abstractions"]
    OrchardCore_Email_Azure --> OrchardCore_Admin_Abstractions
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_Email_Azure --> OrchardCore_DisplayManagement
    OrchardCore_Email_Core["OrchardCore.Email.Core"]
    OrchardCore_Email_Azure --> OrchardCore_Email_Core
    OrchardCore_Navigation_Core["OrchardCore.Navigation.Core"]
    OrchardCore_Email_Azure --> OrchardCore_Navigation_Core
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_Email_Azure --> OrchardCore_Module_Targets
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Email_Azure
```

## Project References
- OrchardCore.Admin.Abstractions
- OrchardCore.DisplayManagement
- OrchardCore.Email.Core
- OrchardCore.Navigation.Core
- OrchardCore.Module.Targets

## Consumed By
- OrchardCore.Application.Cms.Core.Targets

## External NuGet Packages
| Package | Version |
|---------|---------||
| Azure.Communication.Email |  |


---

*[Back to Index](../../index.md)*
