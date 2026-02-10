# OrchardCore.ContentTypes.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.ContentTypes.Abstractions/OrchardCore.ContentTypes.Abstractions.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 32 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_ContentTypes_Abstractions["<strong>OrchardCore.ContentTypes.Abstractions</strong>"]
    OrchardCore_ContentManagement_Abstractions["OrchardCore.ContentManagement.Abstractions"]
    OrchardCore_ContentTypes_Abstractions --> OrchardCore_ContentManagement_Abstractions
    OrchardCore_ContentManagement_Display["OrchardCore.ContentManagement.Display"]
    OrchardCore_ContentTypes_Abstractions --> OrchardCore_ContentManagement_Display
    OrchardCore_AdminMenu["OrchardCore.AdminMenu"]
    OrchardCore_AdminMenu -.-> OrchardCore_ContentTypes_Abstractions
    OrchardCore_ContentPreview["OrchardCore.ContentPreview"]
    OrchardCore_ContentPreview -.-> OrchardCore_ContentTypes_Abstractions
    OrchardCore_Taxonomies["OrchardCore.Taxonomies"]
    OrchardCore_Taxonomies -.-> OrchardCore_ContentTypes_Abstractions
    OrchardCore_Flows["OrchardCore.Flows"]
    OrchardCore_Flows -.-> OrchardCore_ContentTypes_Abstractions
    OrchardCore_ContentFields["OrchardCore.ContentFields"]
    OrchardCore_ContentFields -.-> OrchardCore_ContentTypes_Abstractions
    OrchardCore_AdminDashboard["OrchardCore.AdminDashboard"]
    OrchardCore_AdminDashboard -.-> OrchardCore_ContentTypes_Abstractions
    OrchardCore_Autoroute["OrchardCore.Autoroute"]
    OrchardCore_Autoroute -.-> OrchardCore_ContentTypes_Abstractions
    OrchardCore_Menu["OrchardCore.Menu"]
    OrchardCore_Menu -.-> OrchardCore_ContentTypes_Abstractions
    OrchardCore_Alias["OrchardCore.Alias"]
    OrchardCore_Alias -.-> OrchardCore_ContentTypes_Abstractions
    OrchardCore_Liquid["OrchardCore.Liquid"]
    OrchardCore_Liquid -.-> OrchardCore_ContentTypes_Abstractions
    OrchardCore_Lists["OrchardCore.Lists"]
    OrchardCore_Lists -.-> OrchardCore_ContentTypes_Abstractions
    OrchardCore_Contents["OrchardCore.Contents"]
    OrchardCore_Contents -.-> OrchardCore_ContentTypes_Abstractions
    OrchardCore_Facebook["OrchardCore.Facebook"]
    OrchardCore_Facebook -.-> OrchardCore_ContentTypes_Abstractions
    OrchardCore_Search_Lucene["OrchardCore.Search.Lucene"]
    OrchardCore_Search_Lucene -.-> OrchardCore_ContentTypes_Abstractions
    OrchardCore_Media["OrchardCore.Media"]
    OrchardCore_Media -.-> OrchardCore_ContentTypes_Abstractions
    more_consumers["... +17 more"]
    more_consumers -.-> OrchardCore_ContentTypes_Abstractions
```

## Project References
- OrchardCore.ContentManagement.Abstractions
- OrchardCore.ContentManagement.Display

## Consumed By
- OrchardCore.AdminMenu
- OrchardCore.ContentPreview
- OrchardCore.Taxonomies
- OrchardCore.Flows
- OrchardCore.ContentFields
- OrchardCore.AdminDashboard
- OrchardCore.Autoroute
- OrchardCore.Menu
- OrchardCore.Alias
- OrchardCore.Liquid
- OrchardCore.Lists
- OrchardCore.Contents
- OrchardCore.Facebook
- OrchardCore.Search.Lucene
- OrchardCore.Media
- OrchardCore.Sitemaps
- OrchardCore.Seo
- OrchardCore.Html
- OrchardCore.Title
- OrchardCore.Markdown
- OrchardCore.Search
- OrchardCore.CustomSettings
- OrchardCore.Widgets
- OrchardCore.Templates
- OrchardCore.Spatial
- OrchardCore.Indexing
- OrchardCore.ContentLocalization
- OrchardCore.ContentTypes
- OrchardCore.Placements
- OrchardCore.Search.Elasticsearch.Core
- OrchardCore.ContentManagement.GraphQL
- OrchardCore.ContentManagement


---

*[Back to Index](../../index.md)*
