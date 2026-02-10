# OrchardCore.Application.Mvc.Targets

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Application.Mvc.Targets/OrchardCore.Application.Mvc.Targets.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Application_Mvc_Targets["<strong>OrchardCore.Application.Mvc.Targets</strong>"]
    OrchardCore_Application_Targets["OrchardCore.Application.Targets"]
    OrchardCore_Application_Mvc_Targets --> OrchardCore_Application_Targets
    OrchardCore_Mvc_Core["OrchardCore.Mvc.Core"]
    OrchardCore_Application_Mvc_Targets --> OrchardCore_Mvc_Core
    OrchardCore_Mvc_Web["OrchardCore.Mvc.Web"]
    OrchardCore_Mvc_Web -.-> OrchardCore_Application_Mvc_Targets
```

## Project References
- OrchardCore.Application.Targets
- OrchardCore.Mvc.Core

## Consumed By
- OrchardCore.Mvc.Web


---

*[Back to Index](../../index.md)*
