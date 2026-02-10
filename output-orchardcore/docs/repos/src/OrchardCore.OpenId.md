# OrchardCore.OpenId

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.OpenId/OrchardCore.OpenId.csproj` |
| Project References | 12 |
| NuGet Dependencies | 7 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_OpenId["<strong>OrchardCore.OpenId</strong>"]
    OrchardCore_Admin_Abstractions["OrchardCore.Admin.Abstractions"]
    OrchardCore_OpenId --> OrchardCore_Admin_Abstractions
    OrchardCore_ContentManagement_Abstractions["OrchardCore.ContentManagement.Abstractions"]
    OrchardCore_OpenId --> OrchardCore_ContentManagement_Abstractions
    OrchardCore_Data_Abstractions["OrchardCore.Data.Abstractions"]
    OrchardCore_OpenId --> OrchardCore_Data_Abstractions
    OrchardCore_Deployment_Abstractions["OrchardCore.Deployment.Abstractions"]
    OrchardCore_OpenId --> OrchardCore_Deployment_Abstractions
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_OpenId --> OrchardCore_DisplayManagement
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_OpenId --> OrchardCore_Module_Targets
    OrchardCore_Navigation_Core["OrchardCore.Navigation.Core"]
    OrchardCore_OpenId --> OrchardCore_Navigation_Core
    OrchardCore_OpenId_Core["OrchardCore.OpenId.Core"]
    OrchardCore_OpenId --> OrchardCore_OpenId_Core
    OrchardCore_Recipes_Abstractions["OrchardCore.Recipes.Abstractions"]
    OrchardCore_OpenId --> OrchardCore_Recipes_Abstractions
    OrchardCore_ResourceManagement["OrchardCore.ResourceManagement"]
    OrchardCore_OpenId --> OrchardCore_ResourceManagement
    OrchardCore_Roles_Core["OrchardCore.Roles.Core"]
    OrchardCore_OpenId --> OrchardCore_Roles_Core
    OrchardCore_Users_Abstractions["OrchardCore.Users.Abstractions"]
    OrchardCore_OpenId --> OrchardCore_Users_Abstractions
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_OpenId
```

## Project References
- OrchardCore.Admin.Abstractions
- OrchardCore.ContentManagement.Abstractions
- OrchardCore.Data.Abstractions
- OrchardCore.Deployment.Abstractions
- OrchardCore.DisplayManagement
- OrchardCore.Module.Targets
- OrchardCore.Navigation.Core
- OrchardCore.OpenId.Core
- OrchardCore.Recipes.Abstractions
- OrchardCore.ResourceManagement
- OrchardCore.Roles.Core
- OrchardCore.Users.Abstractions

## Consumed By
- OrchardCore.Application.Cms.Core.Targets

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.AspNetCore.Authentication.OpenIdConnect |  |
| Microsoft.IdentityModel.Protocols.OpenIdConnect |  |
| OpenIddict.Server.AspNetCore |  |
| OpenIddict.Server.DataProtection |  |
| OpenIddict.Validation.AspNetCore |  |
| OpenIddict.Validation.DataProtection |  |
| OpenIddict.Validation.SystemNetHttp |  |


---

*[Back to Index](../../index.md)*
