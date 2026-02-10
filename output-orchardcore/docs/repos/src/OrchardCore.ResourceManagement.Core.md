# OrchardCore.ResourceManagement.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.ResourceManagement.Core/OrchardCore.ResourceManagement.Core.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_ResourceManagement_Core["<strong>OrchardCore.ResourceManagement.Core</strong>"]
    OrchardCore_Abstractions["OrchardCore.Abstractions"]
    OrchardCore_ResourceManagement_Core --> OrchardCore_Abstractions
    OrchardCore_ResourceManagement_Abstractions["OrchardCore.ResourceManagement.Abstractions"]
    OrchardCore_ResourceManagement_Core --> OrchardCore_ResourceManagement_Abstractions
    OrchardCore_Resources["OrchardCore.Resources"]
    OrchardCore_Resources -.-> OrchardCore_ResourceManagement_Core
    OrchardCore_ResourceManagement["OrchardCore.ResourceManagement"]
    OrchardCore_ResourceManagement -.-> OrchardCore_ResourceManagement_Core
```

## Project References
- OrchardCore.Abstractions
- OrchardCore.ResourceManagement.Abstractions

## Consumed By
- OrchardCore.Resources
- OrchardCore.ResourceManagement


---

*[Back to Index](../../index.md)*
