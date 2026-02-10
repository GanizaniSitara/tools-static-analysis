# OrchardCore.Rules.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Rules.Abstractions/OrchardCore.Rules.Abstractions.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Rules_Abstractions["<strong>OrchardCore.Rules.Abstractions</strong>"]
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Rules_Abstractions --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Layers["OrchardCore.Layers"]
    OrchardCore_Layers -.-> OrchardCore_Rules_Abstractions
    OrchardCore_Rules_Core["OrchardCore.Rules.Core"]
    OrchardCore_Rules_Core -.-> OrchardCore_Rules_Abstractions
```

## Project References
- OrchardCore.Infrastructure.Abstractions

## Consumed By
- OrchardCore.Layers
- OrchardCore.Rules.Core


---

*[Back to Index](../../index.md)*
