# Examples.OrchardCoreThemes.Alpha

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | test |
| Path | `OrchardCore.Tests.Themes/Examples.OrchardCoreThemes.Alpha/Examples.OrchardCoreThemes.Alpha.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    Examples_OrchardCoreThemes_Alpha["<strong>Examples.OrchardCoreThemes.Alpha</strong>"]
    OrchardCore_Theme_Targets["OrchardCore.Theme.Targets"]
    Examples_OrchardCoreThemes_Alpha --> OrchardCore_Theme_Targets
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    Examples_OrchardCoreThemes_Alpha --> OrchardCore_DisplayManagement
    OrchardCore_Abstractions_Tests["OrchardCore.Abstractions.Tests"]
    OrchardCore_Abstractions_Tests -.-> Examples_OrchardCoreThemes_Alpha
```

## Project References
- OrchardCore.Theme.Targets
- OrchardCore.DisplayManagement

## Consumed By
- OrchardCore.Abstractions.Tests


---

*[Back to Index](../../index.md)*
