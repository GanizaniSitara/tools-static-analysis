# OrchardCore.Application.Cms.Targets

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Application.Cms.Targets/OrchardCore.Application.Cms.Targets.csproj` |
| Project References | 6 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Application_Cms_Targets["<strong>OrchardCore.Application.Cms.Targets</strong>"]
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Targets --> OrchardCore_Application_Cms_Core_Targets
    SafeMode["SafeMode"]
    OrchardCore_Application_Cms_Targets --> SafeMode
    TheAgencyTheme["TheAgencyTheme"]
    OrchardCore_Application_Cms_Targets --> TheAgencyTheme
    TheBlogTheme["TheBlogTheme"]
    OrchardCore_Application_Cms_Targets --> TheBlogTheme
    TheComingSoonTheme["TheComingSoonTheme"]
    OrchardCore_Application_Cms_Targets --> TheComingSoonTheme
    TheTheme["TheTheme"]
    OrchardCore_Application_Cms_Targets --> TheTheme
    OrchardCore_Cms_Web["OrchardCore.Cms.Web"]
    OrchardCore_Cms_Web -.-> OrchardCore_Application_Cms_Targets
```

## Project References
- OrchardCore.Application.Cms.Core.Targets
- SafeMode
- TheAgencyTheme
- TheBlogTheme
- TheComingSoonTheme
- TheTheme

## Consumed By
- OrchardCore.Cms.Web

## External NuGet Packages
| Package | Version |
|---------|---------||
| OrchardCore.Translations.All |  |


---

*[Back to Index](../../index.md)*
