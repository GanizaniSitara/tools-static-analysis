# BaseThemeSample2

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | test |
| Path | `OrchardCore.Tests.Modules/BaseThemeSample2/BaseThemeSample2.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    BaseThemeSample2["<strong>BaseThemeSample2</strong>"]
    OrchardCore_Theme_Targets["OrchardCore.Theme.Targets"]
    BaseThemeSample2 --> OrchardCore_Theme_Targets
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    BaseThemeSample2 --> OrchardCore_DisplayManagement
    OrchardCore_Tests["OrchardCore.Tests"]
    OrchardCore_Tests -.-> BaseThemeSample2
```

## Project References
- OrchardCore.Theme.Targets
- OrchardCore.DisplayManagement

## Consumed By
- OrchardCore.Tests


---

*[Back to Index](../../index.md)*
