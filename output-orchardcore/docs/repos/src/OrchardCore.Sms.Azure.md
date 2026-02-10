# OrchardCore.Sms.Azure

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.Sms.Azure/OrchardCore.Sms.Azure.csproj` |
| Project References | 4 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Sms_Azure["<strong>OrchardCore.Sms.Azure</strong>"]
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_Sms_Azure --> OrchardCore_DisplayManagement
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_Sms_Azure --> OrchardCore_Module_Targets
    OrchardCore_ResourceManagement["OrchardCore.ResourceManagement"]
    OrchardCore_Sms_Azure --> OrchardCore_ResourceManagement
    OrchardCore_Sms_Core["OrchardCore.Sms.Core"]
    OrchardCore_Sms_Azure --> OrchardCore_Sms_Core
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Sms_Azure
```

## Project References
- OrchardCore.DisplayManagement
- OrchardCore.Module.Targets
- OrchardCore.ResourceManagement
- OrchardCore.Sms.Core

## Consumed By
- OrchardCore.Application.Cms.Core.Targets

## External NuGet Packages
| Package | Version |
|---------|---------||
| Azure.Communication.Sms |  |


---

*[Back to Index](../../index.md)*
