# OrchardCore.HealthChecks

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.HealthChecks/OrchardCore.HealthChecks.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_HealthChecks["<strong>OrchardCore.HealthChecks</strong>"]
    OrchardCore_HealthChecks_Abstractions["OrchardCore.HealthChecks.Abstractions"]
    OrchardCore_HealthChecks --> OrchardCore_HealthChecks_Abstractions
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_HealthChecks --> OrchardCore_Module_Targets
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_HealthChecks
```

## Project References
- OrchardCore.HealthChecks.Abstractions
- OrchardCore.Module.Targets

## Consumed By
- OrchardCore.Application.Cms.Core.Targets


---

*[Back to Index](../../index.md)*
