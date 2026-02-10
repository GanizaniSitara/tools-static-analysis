# OrchardCore.Autoroute.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Autoroute.Core/OrchardCore.Autoroute.Core.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Autoroute_Core["<strong>OrchardCore.Autoroute.Core</strong>"]
    OrchardCore_ContentManagement_Abstractions["OrchardCore.ContentManagement.Abstractions"]
    OrchardCore_Autoroute_Core --> OrchardCore_ContentManagement_Abstractions
    OrchardCore_Data_Abstractions["OrchardCore.Data.Abstractions"]
    OrchardCore_Autoroute_Core --> OrchardCore_Data_Abstractions
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Autoroute_Core --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Autoroute["OrchardCore.Autoroute"]
    OrchardCore_Autoroute -.-> OrchardCore_Autoroute_Core
    OrchardCore_Templates["OrchardCore.Templates"]
    OrchardCore_Templates -.-> OrchardCore_Autoroute_Core
```

## Project References
- OrchardCore.ContentManagement.Abstractions
- OrchardCore.Data.Abstractions
- OrchardCore.Infrastructure.Abstractions

## Consumed By
- OrchardCore.Autoroute
- OrchardCore.Templates


---

*[Back to Index](../../index.md)*
