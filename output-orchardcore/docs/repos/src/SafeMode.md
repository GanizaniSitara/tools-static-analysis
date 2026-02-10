# SafeMode

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Themes/SafeMode/SafeMode.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    SafeMode["<strong>SafeMode</strong>"]
    OrchardCore_Theme_Targets["OrchardCore.Theme.Targets"]
    SafeMode --> OrchardCore_Theme_Targets
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    SafeMode --> OrchardCore_DisplayManagement
    OrchardCore_Application_Cms_Targets["OrchardCore.Application.Cms.Targets"]
    OrchardCore_Application_Cms_Targets -.-> SafeMode
```

## Project References
- OrchardCore.Theme.Targets
- OrchardCore.DisplayManagement

## Consumed By
- OrchardCore.Application.Cms.Targets


---

*[Back to Index](../../index.md)*
