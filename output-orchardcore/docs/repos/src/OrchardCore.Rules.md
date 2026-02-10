# OrchardCore.Rules

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.Rules/OrchardCore.Rules.csproj` |
| Project References | 5 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Rules["<strong>OrchardCore.Rules</strong>"]
    OrchardCore_ContentManagement_Display["OrchardCore.ContentManagement.Display"]
    OrchardCore_Rules --> OrchardCore_ContentManagement_Display
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_Rules --> OrchardCore_DisplayManagement
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_Rules --> OrchardCore_Module_Targets
    OrchardCore_ResourceManagement["OrchardCore.ResourceManagement"]
    OrchardCore_Rules --> OrchardCore_ResourceManagement
    OrchardCore_Rules_Core["OrchardCore.Rules.Core"]
    OrchardCore_Rules --> OrchardCore_Rules_Core
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Rules
```

## Project References
- OrchardCore.ContentManagement.Display
- OrchardCore.DisplayManagement
- OrchardCore.Module.Targets
- OrchardCore.ResourceManagement
- OrchardCore.Rules.Core

## Consumed By
- OrchardCore.Application.Cms.Core.Targets

## External NuGet Packages
| Package | Version |
|---------|---------||
| Jint |  |


---

*[Back to Index](../../index.md)*
