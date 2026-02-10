# OrchardCore.DataProtection.Azure

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.DataProtection.Azure/OrchardCore.DataProtection.Azure.csproj` |
| Project References | 2 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_DataProtection_Azure["<strong>OrchardCore.DataProtection.Azure</strong>"]
    OrchardCore_Liquid_Abstractions["OrchardCore.Liquid.Abstractions"]
    OrchardCore_DataProtection_Azure --> OrchardCore_Liquid_Abstractions
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_DataProtection_Azure --> OrchardCore_Module_Targets
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_DataProtection_Azure
```

## Project References
- OrchardCore.Liquid.Abstractions
- OrchardCore.Module.Targets

## Consumed By
- OrchardCore.Application.Cms.Core.Targets

## External NuGet Packages
| Package | Version |
|---------|---------||
| Azure.Extensions.AspNetCore.DataProtection.Blobs |  |


---

*[Back to Index](../../index.md)*
