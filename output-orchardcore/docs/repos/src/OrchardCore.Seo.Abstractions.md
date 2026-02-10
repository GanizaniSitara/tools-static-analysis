# OrchardCore.Seo.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Seo.Abstractions/OrchardCore.Seo.Abstractions.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Seo_Abstractions["<strong>OrchardCore.Seo.Abstractions</strong>"]
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Seo_Abstractions --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Sitemaps["OrchardCore.Sitemaps"]
    OrchardCore_Sitemaps -.-> OrchardCore_Seo_Abstractions
    OrchardCore_Seo["OrchardCore.Seo"]
    OrchardCore_Seo -.-> OrchardCore_Seo_Abstractions
```

## Project References
- OrchardCore.Infrastructure.Abstractions

## Consumed By
- OrchardCore.Sitemaps
- OrchardCore.Seo


---

*[Back to Index](../../index.md)*
