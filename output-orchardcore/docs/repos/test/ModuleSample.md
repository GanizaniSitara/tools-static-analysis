# ModuleSample

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | test |
| Path | `OrchardCore.Tests.Modules/ModuleSample/ModuleSample.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    ModuleSample["<strong>ModuleSample</strong>"]
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    ModuleSample --> OrchardCore_Module_Targets
    OrchardCore_Tests["OrchardCore.Tests"]
    OrchardCore_Tests -.-> ModuleSample
```

## Project References
- OrchardCore.Module.Targets

## Consumed By
- OrchardCore.Tests


---

*[Back to Index](../../index.md)*
