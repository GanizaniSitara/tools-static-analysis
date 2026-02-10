# Examples.OrchardCoreModules.Alpha

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | test |
| Path | `OrchardCore.Tests.Modules/Examples.OrchardCoreModules.Alpha/Examples.OrchardCoreModules.Alpha.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    Examples_OrchardCoreModules_Alpha["<strong>Examples.OrchardCoreModules.Alpha</strong>"]
    OrchardCore_Abstractions["OrchardCore.Abstractions"]
    Examples_OrchardCoreModules_Alpha --> OrchardCore_Abstractions
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    Examples_OrchardCoreModules_Alpha --> OrchardCore_Module_Targets
    OrchardCore_Abstractions_Tests["OrchardCore.Abstractions.Tests"]
    OrchardCore_Abstractions_Tests -.-> Examples_OrchardCoreModules_Alpha
```

## Project References
- OrchardCore.Abstractions
- OrchardCore.Module.Targets

## Consumed By
- OrchardCore.Abstractions.Tests


---

*[Back to Index](../../index.md)*
