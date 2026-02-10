# Module.Pages

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | test |
| Path | `OrchardCore.Tests.Pages/OrchardCore.Modules.Pages/Module.Pages/Module.Pages.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    Module_Pages["<strong>Module.Pages</strong>"]
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    Module_Pages --> OrchardCore_Module_Targets
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    Module_Pages --> OrchardCore_DisplayManagement
    OrchardCore_Application_Pages["OrchardCore.Application.Pages"]
    OrchardCore_Application_Pages -.-> Module_Pages
```

## Project References
- OrchardCore.Module.Targets
- OrchardCore.DisplayManagement

## Consumed By
- OrchardCore.Application.Pages


---

*[Back to Index](../../index.md)*
