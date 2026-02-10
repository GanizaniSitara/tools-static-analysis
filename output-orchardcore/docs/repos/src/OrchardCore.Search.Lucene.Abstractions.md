# OrchardCore.Search.Lucene.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Search.Lucene.Abstractions/OrchardCore.Search.Lucene.Abstractions.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Search_Lucene_Abstractions["<strong>OrchardCore.Search.Lucene.Abstractions</strong>"]
    OrchardCore_Queries_Abstractions["OrchardCore.Queries.Abstractions"]
    OrchardCore_Search_Lucene_Abstractions --> OrchardCore_Queries_Abstractions
    OrchardCore_Search_Lucene_Core["OrchardCore.Search.Lucene.Core"]
    OrchardCore_Search_Lucene_Core -.-> OrchardCore_Search_Lucene_Abstractions
```

## Project References
- OrchardCore.Queries.Abstractions

## Consumed By
- OrchardCore.Search.Lucene.Core

## External NuGet Packages
| Package | Version |
|---------|---------||
| Lucene.Net |  |


---

*[Back to Index](../../index.md)*
