# DerivedThemeSample

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | test |
| Path | `OrchardCore.Tests.Modules/DerivedThemeSample/DerivedThemeSample.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    DerivedThemeSample["<strong>DerivedThemeSample</strong>"]
    OrchardCore_Theme_Targets["OrchardCore.Theme.Targets"]
    DerivedThemeSample --> OrchardCore_Theme_Targets
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    DerivedThemeSample --> OrchardCore_DisplayManagement
    OrchardCore_Tests["OrchardCore.Tests"]
    OrchardCore_Tests -.-> DerivedThemeSample
```

## Project References
- OrchardCore.Theme.Targets
- OrchardCore.DisplayManagement

## Consumed By
- OrchardCore.Tests


---

*[Back to Index](../../index.md)*
