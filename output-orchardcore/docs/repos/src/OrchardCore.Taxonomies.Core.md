# OrchardCore.Taxonomies.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Taxonomies.Core/OrchardCore.Taxonomies.Core.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Taxonomies_Core["<strong>OrchardCore.Taxonomies.Core</strong>"]
    OrchardCore_ContentManagement_Abstractions["OrchardCore.ContentManagement.Abstractions"]
    OrchardCore_Taxonomies_Core --> OrchardCore_ContentManagement_Abstractions
    OrchardCore_ContentManagement["OrchardCore.ContentManagement"]
    OrchardCore_Taxonomies_Core --> OrchardCore_ContentManagement
    OrchardCore_Navigation_Core["OrchardCore.Navigation.Core"]
    OrchardCore_Taxonomies_Core --> OrchardCore_Navigation_Core
    OrchardCore_Taxonomies["OrchardCore.Taxonomies"]
    OrchardCore_Taxonomies -.-> OrchardCore_Taxonomies_Core
```

## Project References
- OrchardCore.ContentManagement.Abstractions
- OrchardCore.ContentManagement
- OrchardCore.Navigation.Core

## Consumed By
- OrchardCore.Taxonomies


---

*[Back to Index](../../index.md)*
