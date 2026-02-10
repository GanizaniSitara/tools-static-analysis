# OrchardCore.ReCaptcha.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.ReCaptcha.Core/OrchardCore.ReCaptcha.Core.csproj` |
| Project References | 2 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_ReCaptcha_Core["<strong>OrchardCore.ReCaptcha.Core</strong>"]
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_ReCaptcha_Core --> OrchardCore_DisplayManagement
    OrchardCore_ResourceManagement_Abstractions["OrchardCore.ResourceManagement.Abstractions"]
    OrchardCore_ReCaptcha_Core --> OrchardCore_ResourceManagement_Abstractions
    OrchardCore_ReCaptcha["OrchardCore.ReCaptcha"]
    OrchardCore_ReCaptcha -.-> OrchardCore_ReCaptcha_Core
```

## Project References
- OrchardCore.DisplayManagement
- OrchardCore.ResourceManagement.Abstractions

## Consumed By
- OrchardCore.ReCaptcha

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.Extensions.Http.Resilience |  |


---

*[Back to Index](../../index.md)*
