# OrchardCore.Search.Lucene.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Search.Lucene.Core/OrchardCore.Search.Lucene.Core.csproj` |
| Project References | 6 |
| NuGet Dependencies | 2 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Search_Lucene_Core["<strong>OrchardCore.Search.Lucene.Core</strong>"]
    OrchardCore_Abstractions["OrchardCore.Abstractions"]
    OrchardCore_Search_Lucene_Core --> OrchardCore_Abstractions
    OrchardCore_Contents_Core["OrchardCore.Contents.Core"]
    OrchardCore_Search_Lucene_Core --> OrchardCore_Contents_Core
    OrchardCore_Indexing_Abstractions["OrchardCore.Indexing.Abstractions"]
    OrchardCore_Search_Lucene_Core --> OrchardCore_Indexing_Abstractions
    OrchardCore_Indexing_Core["OrchardCore.Indexing.Core"]
    OrchardCore_Search_Lucene_Core --> OrchardCore_Indexing_Core
    OrchardCore_Queries_Abstractions["OrchardCore.Queries.Abstractions"]
    OrchardCore_Search_Lucene_Core --> OrchardCore_Queries_Abstractions
    OrchardCore_Search_Lucene_Abstractions["OrchardCore.Search.Lucene.Abstractions"]
    OrchardCore_Search_Lucene_Core --> OrchardCore_Search_Lucene_Abstractions
    OrchardCore_Search_Lucene["OrchardCore.Search.Lucene"]
    OrchardCore_Search_Lucene -.-> OrchardCore_Search_Lucene_Core
```

## Project References
- OrchardCore.Abstractions
- OrchardCore.Contents.Core
- OrchardCore.Indexing.Abstractions
- OrchardCore.Indexing.Core
- OrchardCore.Queries.Abstractions
- OrchardCore.Search.Lucene.Abstractions

## Consumed By
- OrchardCore.Search.Lucene

## External NuGet Packages
| Package | Version |
|---------|---------||
| Lucene.Net.QueryParser |  |
| Lucene.Net.Spatial |  |


---

*[Back to Index](../../index.md)*
