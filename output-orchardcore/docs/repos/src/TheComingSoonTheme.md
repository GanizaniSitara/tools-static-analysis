# TheComingSoonTheme

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Themes/TheComingSoonTheme/TheComingSoonTheme.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    TheComingSoonTheme["<strong>TheComingSoonTheme</strong>"]
    OrchardCore_ResourceManagement_Abstractions["OrchardCore.ResourceManagement.Abstractions"]
    TheComingSoonTheme --> OrchardCore_ResourceManagement_Abstractions
    OrchardCore_Theme_Targets["OrchardCore.Theme.Targets"]
    TheComingSoonTheme --> OrchardCore_Theme_Targets
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    TheComingSoonTheme --> OrchardCore_DisplayManagement
    OrchardCore_Application_Cms_Targets["OrchardCore.Application.Cms.Targets"]
    OrchardCore_Application_Cms_Targets -.-> TheComingSoonTheme
```

## Project References
- OrchardCore.ResourceManagement.Abstractions
- OrchardCore.Theme.Targets
- OrchardCore.DisplayManagement

## Consumed By
- OrchardCore.Application.Cms.Targets


---

*[Back to Index](../../index.md)*
