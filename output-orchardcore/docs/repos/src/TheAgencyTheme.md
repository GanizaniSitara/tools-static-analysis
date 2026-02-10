# TheAgencyTheme

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Themes/TheAgencyTheme/TheAgencyTheme.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    TheAgencyTheme["<strong>TheAgencyTheme</strong>"]
    OrchardCore_ResourceManagement_Abstractions["OrchardCore.ResourceManagement.Abstractions"]
    TheAgencyTheme --> OrchardCore_ResourceManagement_Abstractions
    OrchardCore_Theme_Targets["OrchardCore.Theme.Targets"]
    TheAgencyTheme --> OrchardCore_Theme_Targets
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    TheAgencyTheme --> OrchardCore_DisplayManagement
    OrchardCore_Application_Cms_Targets["OrchardCore.Application.Cms.Targets"]
    OrchardCore_Application_Cms_Targets -.-> TheAgencyTheme
```

## Project References
- OrchardCore.ResourceManagement.Abstractions
- OrchardCore.Theme.Targets
- OrchardCore.DisplayManagement

## Consumed By
- OrchardCore.Application.Cms.Targets


---

*[Back to Index](../../index.md)*
