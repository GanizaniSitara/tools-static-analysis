# OrchardCore.Search.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Search.Abstractions/OrchardCore.Search.Abstractions.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Search_Abstractions["<strong>OrchardCore.Search.Abstractions</strong>"]
    OrchardCore_ContentManagement["OrchardCore.ContentManagement"]
    OrchardCore_Search_Abstractions --> OrchardCore_ContentManagement
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_Search_Abstractions --> OrchardCore_DisplayManagement
    OrchardCore_Indexing_Abstractions["OrchardCore.Indexing.Abstractions"]
    OrchardCore_Search_Abstractions --> OrchardCore_Indexing_Abstractions
    OrchardCore_Search_Lucene["OrchardCore.Search.Lucene"]
    OrchardCore_Search_Lucene -.-> OrchardCore_Search_Abstractions
    OrchardCore_Search["OrchardCore.Search"]
    OrchardCore_Search -.-> OrchardCore_Search_Abstractions
    OrchardCore_Indexing_Core["OrchardCore.Indexing.Core"]
    OrchardCore_Indexing_Core -.-> OrchardCore_Search_Abstractions
    OrchardCore_Search_Elasticsearch_Core["OrchardCore.Search.Elasticsearch.Core"]
    OrchardCore_Search_Elasticsearch_Core -.-> OrchardCore_Search_Abstractions
    OrchardCore_Search_AzureAI_Core["OrchardCore.Search.AzureAI.Core"]
    OrchardCore_Search_AzureAI_Core -.-> OrchardCore_Search_Abstractions
```

## Project References
- OrchardCore.ContentManagement
- OrchardCore.DisplayManagement
- OrchardCore.Indexing.Abstractions

## Consumed By
- OrchardCore.Search.Lucene
- OrchardCore.Search
- OrchardCore.Indexing.Core
- OrchardCore.Search.Elasticsearch.Core
- OrchardCore.Search.AzureAI.Core


---

*[Back to Index](../../index.md)*
