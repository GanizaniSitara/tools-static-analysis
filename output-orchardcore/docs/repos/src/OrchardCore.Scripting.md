# OrchardCore.Scripting

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.Scripting/OrchardCore.Scripting.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Scripting["<strong>OrchardCore.Scripting</strong>"]
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_Scripting --> OrchardCore_Module_Targets
    OrchardCore_Scripting_JavaScript["OrchardCore.Scripting.JavaScript"]
    OrchardCore_Scripting --> OrchardCore_Scripting_JavaScript
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Scripting
```

## Project References
- OrchardCore.Module.Targets
- OrchardCore.Scripting.JavaScript

## Consumed By
- OrchardCore.Application.Cms.Core.Targets


---

*[Back to Index](../../index.md)*
