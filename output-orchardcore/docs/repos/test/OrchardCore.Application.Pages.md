# OrchardCore.Application.Pages

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | test |
| Path | `OrchardCore.Tests.Pages/OrchardCore.Application.Pages/OrchardCore.Application.Pages.csproj` |
| Project References | 3 |
| NuGet Dependencies | 1 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Application_Pages["<strong>OrchardCore.Application.Pages</strong>"]
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Pages --> OrchardCore_Application_Cms_Core_Targets
    Module_Pages["Module.Pages"]
    OrchardCore_Application_Pages --> Module_Pages
    Theme_Pages["Theme.Pages"]
    OrchardCore_Application_Pages --> Theme_Pages
```

## Project References
- OrchardCore.Application.Cms.Core.Targets
- Module.Pages
- Theme.Pages

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.AspNetCore.Mvc.Razor.RuntimeCompilation |  |


---

*[Back to Index](../../index.md)*
