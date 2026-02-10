# OrchardCore.Mvc.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Mvc.Core/OrchardCore.Mvc.Core.csproj` |
| Project References | 2 |
| NuGet Dependencies | 1 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Mvc_Core["<strong>OrchardCore.Mvc.Core</strong>"]
    OrchardCore_Abstractions["OrchardCore.Abstractions"]
    OrchardCore_Mvc_Core --> OrchardCore_Abstractions
    OrchardCore_DisplayManagement_Abstractions["OrchardCore.DisplayManagement.Abstractions"]
    OrchardCore_Mvc_Core --> OrchardCore_DisplayManagement_Abstractions
    OrchardCore_HomeRoute["OrchardCore.HomeRoute"]
    OrchardCore_HomeRoute -.-> OrchardCore_Mvc_Core
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_DisplayManagement -.-> OrchardCore_Mvc_Core
    OrchardCore_Application_Mvc_Targets["OrchardCore.Application.Mvc.Targets"]
    OrchardCore_Application_Mvc_Targets -.-> OrchardCore_Mvc_Core
```

## Project References
- OrchardCore.Abstractions
- OrchardCore.DisplayManagement.Abstractions

## Consumed By
- OrchardCore.HomeRoute
- OrchardCore.DisplayManagement
- OrchardCore.Application.Mvc.Targets

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.AspNetCore.Mvc.Razor.RuntimeCompilation |  |


---

*[Back to Index](../../index.md)*
