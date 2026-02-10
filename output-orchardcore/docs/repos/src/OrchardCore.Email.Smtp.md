# OrchardCore.Email.Smtp

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.Email.Smtp/OrchardCore.Email.Smtp.csproj` |
| Project References | 8 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Email_Smtp["<strong>OrchardCore.Email.Smtp</strong>"]
    OrchardCore_Abstractions["OrchardCore.Abstractions"]
    OrchardCore_Email_Smtp --> OrchardCore_Abstractions
    OrchardCore_Admin_Abstractions["OrchardCore.Admin.Abstractions"]
    OrchardCore_Email_Smtp --> OrchardCore_Admin_Abstractions
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_Email_Smtp --> OrchardCore_DisplayManagement
    OrchardCore_Email_Abstractions["OrchardCore.Email.Abstractions"]
    OrchardCore_Email_Smtp --> OrchardCore_Email_Abstractions
    OrchardCore_Email_Core["OrchardCore.Email.Core"]
    OrchardCore_Email_Smtp --> OrchardCore_Email_Core
    OrchardCore_Navigation_Core["OrchardCore.Navigation.Core"]
    OrchardCore_Email_Smtp --> OrchardCore_Navigation_Core
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_Email_Smtp --> OrchardCore_Module_Targets
    OrchardCore_ResourceManagement["OrchardCore.ResourceManagement"]
    OrchardCore_Email_Smtp --> OrchardCore_ResourceManagement
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Email_Smtp
```

## Project References
- OrchardCore.Abstractions
- OrchardCore.Admin.Abstractions
- OrchardCore.DisplayManagement
- OrchardCore.Email.Abstractions
- OrchardCore.Email.Core
- OrchardCore.Navigation.Core
- OrchardCore.Module.Targets
- OrchardCore.ResourceManagement

## Consumed By
- OrchardCore.Application.Cms.Core.Targets

## External NuGet Packages
| Package | Version |
|---------|---------||
| MailKit |  |


---

*[Back to Index](../../index.md)*
