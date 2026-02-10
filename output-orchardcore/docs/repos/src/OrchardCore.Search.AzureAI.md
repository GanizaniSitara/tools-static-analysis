# OrchardCore.Search.AzureAI

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.Search.AzureAI/OrchardCore.Search.AzureAI.csproj` |
| Project References | 6 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Search_AzureAI["<strong>OrchardCore.Search.AzureAI</strong>"]
    OrchardCore_Admin_Abstractions["OrchardCore.Admin.Abstractions"]
    OrchardCore_Search_AzureAI --> OrchardCore_Admin_Abstractions
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_Search_AzureAI --> OrchardCore_DisplayManagement
    OrchardCore_Flows_Core["OrchardCore.Flows.Core"]
    OrchardCore_Search_AzureAI --> OrchardCore_Flows_Core
    OrchardCore_Navigation_Core["OrchardCore.Navigation.Core"]
    OrchardCore_Search_AzureAI --> OrchardCore_Navigation_Core
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_Search_AzureAI --> OrchardCore_Module_Targets
    OrchardCore_Search_AzureAI_Core["OrchardCore.Search.AzureAI.Core"]
    OrchardCore_Search_AzureAI --> OrchardCore_Search_AzureAI_Core
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Search_AzureAI
```

## Project References
- OrchardCore.Admin.Abstractions
- OrchardCore.DisplayManagement
- OrchardCore.Flows.Core
- OrchardCore.Navigation.Core
- OrchardCore.Module.Targets
- OrchardCore.Search.AzureAI.Core

## Consumed By
- OrchardCore.Application.Cms.Core.Targets

## External NuGet Packages
| Package | Version |
|---------|---------||
| Azure.Search.Documents |  |


---

*[Back to Index](../../index.md)*
