# DerivedThemeSample2

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | test |
| Path | `OrchardCore.Tests.Modules/DerivedThemeSample2/DerivedThemeSample2.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    DerivedThemeSample2["<strong>DerivedThemeSample2</strong>"]
    OrchardCore_Theme_Targets["OrchardCore.Theme.Targets"]
    DerivedThemeSample2 --> OrchardCore_Theme_Targets
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    DerivedThemeSample2 --> OrchardCore_DisplayManagement
    OrchardCore_Tests["OrchardCore.Tests"]
    OrchardCore_Tests -.-> DerivedThemeSample2
```

## Project References
- OrchardCore.Theme.Targets
- OrchardCore.DisplayManagement

## Consumed By
- OrchardCore.Tests


---

*[Back to Index](../../index.md)*
