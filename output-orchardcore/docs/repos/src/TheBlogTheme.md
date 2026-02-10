# TheBlogTheme

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Themes/TheBlogTheme/TheBlogTheme.csproj` |
| Project References | 4 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    TheBlogTheme["<strong>TheBlogTheme</strong>"]
    OrchardCore_Queries["OrchardCore.Queries"]
    TheBlogTheme --> OrchardCore_Queries
    OrchardCore_Theme_Targets["OrchardCore.Theme.Targets"]
    TheBlogTheme --> OrchardCore_Theme_Targets
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    TheBlogTheme --> OrchardCore_DisplayManagement
    OrchardCore_ResourceManagement_Abstractions["OrchardCore.ResourceManagement.Abstractions"]
    TheBlogTheme --> OrchardCore_ResourceManagement_Abstractions
    OrchardCore_Application_Cms_Targets["OrchardCore.Application.Cms.Targets"]
    OrchardCore_Application_Cms_Targets -.-> TheBlogTheme
```

## Project References
- OrchardCore.Queries
- OrchardCore.Theme.Targets
- OrchardCore.DisplayManagement
- OrchardCore.ResourceManagement.Abstractions

## Consumed By
- OrchardCore.Application.Cms.Targets


---

*[Back to Index](../../index.md)*
