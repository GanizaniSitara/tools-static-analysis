# OrchardCore.Localization.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Localization |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Localization.Core/OrchardCore.Localization.Core.csproj` |
| Project References | 2 |
| NuGet Dependencies | 1 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Localization_Core["<strong>OrchardCore.Localization.Core</strong>"]
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Localization_Core --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Localization_Abstractions["OrchardCore.Localization.Abstractions"]
    OrchardCore_Localization_Core --> OrchardCore_Localization_Abstractions
    OrchardCore_Setup["OrchardCore.Setup"]
    OrchardCore_Setup -.-> OrchardCore_Localization_Core
    OrchardCore_DataLocalization["OrchardCore.DataLocalization"]
    OrchardCore_DataLocalization -.-> OrchardCore_Localization_Core
    OrchardCore_Localization["OrchardCore.Localization"]
    OrchardCore_Localization -.-> OrchardCore_Localization_Core
```

## Project References
- OrchardCore.Infrastructure.Abstractions
- OrchardCore.Localization.Abstractions

## Consumed By
- OrchardCore.Setup
- OrchardCore.DataLocalization
- OrchardCore.Localization

## External NuGet Packages
| Package | Version |
|---------|---------||
| ZString |  |


---

*[Back to Index](../../index.md)*
