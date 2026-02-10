# OrchardCore.Queries.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Queries.Core/OrchardCore.Queries.Core.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Queries_Core["<strong>OrchardCore.Queries.Core</strong>"]
    OrchardCore_Queries_Abstractions["OrchardCore.Queries.Abstractions"]
    OrchardCore_Queries_Core --> OrchardCore_Queries_Abstractions
    OrchardCore_Queries["OrchardCore.Queries"]
    OrchardCore_Queries -.-> OrchardCore_Queries_Core
    OrchardCore_Search_Elasticsearch["OrchardCore.Search.Elasticsearch"]
    OrchardCore_Search_Elasticsearch -.-> OrchardCore_Queries_Core
    OrchardCore_Search_Lucene["OrchardCore.Search.Lucene"]
    OrchardCore_Search_Lucene -.-> OrchardCore_Queries_Core
```

## Project References
- OrchardCore.Queries.Abstractions

## Consumed By
- OrchardCore.Queries
- OrchardCore.Search.Elasticsearch
- OrchardCore.Search.Lucene

## External NuGet Packages
| Package | Version |
|---------|---------||
| YesSql.Core |  |


---

*[Back to Index](../../index.md)*
