# BaseThemeSample

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | test |
| Path | `OrchardCore.Tests.Modules/BaseThemeSample/BaseThemeSample.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    BaseThemeSample["<strong>BaseThemeSample</strong>"]
    OrchardCore_Theme_Targets["OrchardCore.Theme.Targets"]
    BaseThemeSample --> OrchardCore_Theme_Targets
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    BaseThemeSample --> OrchardCore_DisplayManagement
    OrchardCore_Tests["OrchardCore.Tests"]
    OrchardCore_Tests -.-> BaseThemeSample
```

## Project References
- OrchardCore.Theme.Targets
- OrchardCore.DisplayManagement

## Consumed By
- OrchardCore.Tests


---

*[Back to Index](../../index.md)*
