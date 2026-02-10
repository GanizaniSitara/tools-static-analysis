# OrchardCore.Apis.GraphQL

## Overview

| Property | Value |
|----------|-------|
| Category | WebApp |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.Apis.GraphQL/OrchardCore.Apis.GraphQL.csproj` |
| Project References | 6 |
| NuGet Dependencies | 5 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Apis_GraphQL["<strong>OrchardCore.Apis.GraphQL</strong>"]
    OrchardCore_Admin_Abstractions["OrchardCore.Admin.Abstractions"]
    OrchardCore_Apis_GraphQL --> OrchardCore_Admin_Abstractions
    OrchardCore_Apis_GraphQL_Abstractions["OrchardCore.Apis.GraphQL.Abstractions"]
    OrchardCore_Apis_GraphQL --> OrchardCore_Apis_GraphQL_Abstractions
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_Apis_GraphQL --> OrchardCore_DisplayManagement
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_Apis_GraphQL --> OrchardCore_Module_Targets
    OrchardCore_Navigation_Core["OrchardCore.Navigation.Core"]
    OrchardCore_Apis_GraphQL --> OrchardCore_Navigation_Core
    OrchardCore_ResourceManagement["OrchardCore.ResourceManagement"]
    OrchardCore_Apis_GraphQL --> OrchardCore_ResourceManagement
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Apis_GraphQL
```

## Project References
- OrchardCore.Admin.Abstractions
- OrchardCore.Apis.GraphQL.Abstractions
- OrchardCore.DisplayManagement
- OrchardCore.Module.Targets
- OrchardCore.Navigation.Core
- OrchardCore.ResourceManagement

## Consumed By
- OrchardCore.Application.Cms.Core.Targets

## External NuGet Packages
| Package | Version |
|---------|---------||
| GraphQL |  |
| GraphQL.DataLoader |  |
| GraphQL.MicrosoftDI |  |
| GraphQL.SystemTextJson |  |
| YesSql.Abstractions |  |


---

*[Back to Index](../../index.md)*
