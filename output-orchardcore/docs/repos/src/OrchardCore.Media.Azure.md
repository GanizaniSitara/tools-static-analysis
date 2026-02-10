# OrchardCore.Media.Azure

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.Media.Azure/OrchardCore.Media.Azure.csproj` |
| Project References | 8 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Media_Azure["<strong>OrchardCore.Media.Azure</strong>"]
    OrchardCore_Admin_Abstractions["OrchardCore.Admin.Abstractions"]
    OrchardCore_Media_Azure --> OrchardCore_Admin_Abstractions
    OrchardCore_ContentManagement_Display["OrchardCore.ContentManagement.Display"]
    OrchardCore_Media_Azure --> OrchardCore_ContentManagement_Display
    OrchardCore_FileStorage_AzureBlob["OrchardCore.FileStorage.AzureBlob"]
    OrchardCore_Media_Azure --> OrchardCore_FileStorage_AzureBlob
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Media_Azure --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Media_Core["OrchardCore.Media.Core"]
    OrchardCore_Media_Azure --> OrchardCore_Media_Core
    OrchardCore_Navigation_Core["OrchardCore.Navigation.Core"]
    OrchardCore_Media_Azure --> OrchardCore_Navigation_Core
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_Media_Azure --> OrchardCore_Module_Targets
    OrchardCore_Media["OrchardCore.Media"]
    OrchardCore_Media_Azure --> OrchardCore_Media
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Media_Azure
```

## Project References
- OrchardCore.Admin.Abstractions
- OrchardCore.ContentManagement.Display
- OrchardCore.FileStorage.AzureBlob
- OrchardCore.Infrastructure.Abstractions
- OrchardCore.Media.Core
- OrchardCore.Navigation.Core
- OrchardCore.Module.Targets
- OrchardCore.Media

## Consumed By
- OrchardCore.Application.Cms.Core.Targets

## External NuGet Packages
| Package | Version |
|---------|---------||
| SixLabors.ImageSharp.Web.Providers.Azure |  |


---

*[Back to Index](../../index.md)*
