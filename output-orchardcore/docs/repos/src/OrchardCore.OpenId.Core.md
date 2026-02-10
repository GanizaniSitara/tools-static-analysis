# OrchardCore.OpenId.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.OpenId.Core/OrchardCore.OpenId.Core.csproj` |
| Project References | 2 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_OpenId_Core["<strong>OrchardCore.OpenId.Core</strong>"]
    OrchardCore_Data_YesSql["OrchardCore.Data.YesSql"]
    OrchardCore_OpenId_Core --> OrchardCore_Data_YesSql
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_OpenId_Core --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_OpenId["OrchardCore.OpenId"]
    OrchardCore_OpenId -.-> OrchardCore_OpenId_Core
```

## Project References
- OrchardCore.Data.YesSql
- OrchardCore.Infrastructure.Abstractions

## Consumed By
- OrchardCore.OpenId

## External NuGet Packages
| Package | Version |
|---------|---------||
| OpenIddict.Core |  |


---

*[Back to Index](../../index.md)*
