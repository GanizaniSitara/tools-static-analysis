# Theme.Pages

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | test |
| Path | `OrchardCore.Tests.Pages/OrchardCore.Themes.Pages/Theme.Pages/Theme.Pages.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    Theme_Pages["<strong>Theme.Pages</strong>"]
    OrchardCore_Theme_Targets["OrchardCore.Theme.Targets"]
    Theme_Pages --> OrchardCore_Theme_Targets
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    Theme_Pages --> OrchardCore_DisplayManagement
    OrchardCore_Application_Pages["OrchardCore.Application.Pages"]
    OrchardCore_Application_Pages -.-> Theme_Pages
```

## Project References
- OrchardCore.Theme.Targets
- OrchardCore.DisplayManagement

## Consumed By
- OrchardCore.Application.Pages


---

*[Back to Index](../../index.md)*
