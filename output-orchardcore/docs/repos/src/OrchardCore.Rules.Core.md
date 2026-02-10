# OrchardCore.Rules.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Rules.Core/OrchardCore.Rules.Core.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Rules_Core["<strong>OrchardCore.Rules.Core</strong>"]
    OrchardCore_Abstractions["OrchardCore.Abstractions"]
    OrchardCore_Rules_Core --> OrchardCore_Abstractions
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_Rules_Core --> OrchardCore_DisplayManagement
    OrchardCore_Rules_Abstractions["OrchardCore.Rules.Abstractions"]
    OrchardCore_Rules_Core --> OrchardCore_Rules_Abstractions
    OrchardCore_Rules["OrchardCore.Rules"]
    OrchardCore_Rules -.-> OrchardCore_Rules_Core
```

## Project References
- OrchardCore.Abstractions
- OrchardCore.DisplayManagement
- OrchardCore.Rules.Abstractions

## Consumed By
- OrchardCore.Rules


---

*[Back to Index](../../index.md)*
