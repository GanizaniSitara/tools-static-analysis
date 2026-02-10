# OrchardCore.Resources

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.Resources/OrchardCore.Resources.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Resources["<strong>OrchardCore.Resources</strong>"]
    OrchardCore_DisplayManagement_Liquid["OrchardCore.DisplayManagement.Liquid"]
    OrchardCore_Resources --> OrchardCore_DisplayManagement_Liquid
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_Resources --> OrchardCore_Module_Targets
    OrchardCore_ResourceManagement_Core["OrchardCore.ResourceManagement.Core"]
    OrchardCore_Resources --> OrchardCore_ResourceManagement_Core
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Resources
```

## Project References
- OrchardCore.DisplayManagement.Liquid
- OrchardCore.Module.Targets
- OrchardCore.ResourceManagement.Core

## Consumed By
- OrchardCore.Application.Cms.Core.Targets


---

*[Back to Index](../../index.md)*
