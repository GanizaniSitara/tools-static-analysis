# OrchardCore.Queries.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Queries.Abstractions/OrchardCore.Queries.Abstractions.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Queries_Abstractions["<strong>OrchardCore.Queries.Abstractions</strong>"]
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Queries_Abstractions --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Search_Elasticsearch_Core["OrchardCore.Search.Elasticsearch.Core"]
    OrchardCore_Search_Elasticsearch_Core -.-> OrchardCore_Queries_Abstractions
    OrchardCore_Search_Lucene_Abstractions["OrchardCore.Search.Lucene.Abstractions"]
    OrchardCore_Search_Lucene_Abstractions -.-> OrchardCore_Queries_Abstractions
    OrchardCore_Search_Lucene_Core["OrchardCore.Search.Lucene.Core"]
    OrchardCore_Search_Lucene_Core -.-> OrchardCore_Queries_Abstractions
    OrchardCore_Search_Elasticsearch_Abstractions["OrchardCore.Search.Elasticsearch.Abstractions"]
    OrchardCore_Search_Elasticsearch_Abstractions -.-> OrchardCore_Queries_Abstractions
    OrchardCore_Queries_Core["OrchardCore.Queries.Core"]
    OrchardCore_Queries_Core -.-> OrchardCore_Queries_Abstractions
```

## Project References
- OrchardCore.Infrastructure.Abstractions

## Consumed By
- OrchardCore.Search.Elasticsearch.Core
- OrchardCore.Search.Lucene.Abstractions
- OrchardCore.Search.Lucene.Core
- OrchardCore.Search.Elasticsearch.Abstractions
- OrchardCore.Queries.Core


---

*[Back to Index](../../index.md)*
