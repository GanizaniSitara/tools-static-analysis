# OrchardCore.Sitemaps.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Sitemaps.Abstractions/OrchardCore.Sitemaps.Abstractions.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 4 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Sitemaps_Abstractions["<strong>OrchardCore.Sitemaps.Abstractions</strong>"]
    OrchardCore_ContentManagement_Abstractions["OrchardCore.ContentManagement.Abstractions"]
    OrchardCore_Sitemaps_Abstractions --> OrchardCore_ContentManagement_Abstractions
    OrchardCore_DisplayManagement_Abstractions["OrchardCore.DisplayManagement.Abstractions"]
    OrchardCore_Sitemaps_Abstractions --> OrchardCore_DisplayManagement_Abstractions
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Sitemaps_Abstractions --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Autoroute["OrchardCore.Autoroute"]
    OrchardCore_Autoroute -.-> OrchardCore_Sitemaps_Abstractions
    OrchardCore_Contents["OrchardCore.Contents"]
    OrchardCore_Contents -.-> OrchardCore_Sitemaps_Abstractions
    OrchardCore_Sitemaps["OrchardCore.Sitemaps"]
    OrchardCore_Sitemaps -.-> OrchardCore_Sitemaps_Abstractions
    OrchardCore_ContentLocalization["OrchardCore.ContentLocalization"]
    OrchardCore_ContentLocalization -.-> OrchardCore_Sitemaps_Abstractions
```

## Project References
- OrchardCore.ContentManagement.Abstractions
- OrchardCore.DisplayManagement.Abstractions
- OrchardCore.Infrastructure.Abstractions

## Consumed By
- OrchardCore.Autoroute
- OrchardCore.Contents
- OrchardCore.Sitemaps
- OrchardCore.ContentLocalization


---

*[Back to Index](../../index.md)*
