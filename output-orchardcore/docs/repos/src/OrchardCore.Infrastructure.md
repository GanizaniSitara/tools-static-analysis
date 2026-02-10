# OrchardCore.Infrastructure

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Infrastructure/OrchardCore.Infrastructure.csproj` |
| Project References | 3 |
| NuGet Dependencies | 2 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Infrastructure["<strong>OrchardCore.Infrastructure</strong>"]
    OrchardCore["OrchardCore"]
    OrchardCore_Infrastructure --> OrchardCore
    OrchardCore_Data_YesSql["OrchardCore.Data.YesSql"]
    OrchardCore_Infrastructure --> OrchardCore_Data_YesSql
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Infrastructure --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Notifications_Core["OrchardCore.Notifications.Core"]
    OrchardCore_Notifications_Core -.-> OrchardCore_Infrastructure
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Infrastructure
```

## Project References
- OrchardCore
- OrchardCore.Data.YesSql
- OrchardCore.Infrastructure.Abstractions

## Consumed By
- OrchardCore.Notifications.Core
- OrchardCore.Application.Cms.Core.Targets

## External NuGet Packages
| Package | Version |
|---------|---------||
| HtmlSanitizer |  |
| MimeKit |  |


---

*[Back to Index](../../index.md)*
