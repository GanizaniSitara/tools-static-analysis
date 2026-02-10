# OrchardCore.Search.Elasticsearch

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.Search.Elasticsearch/OrchardCore.Search.Elasticsearch.csproj` |
| Project References | 8 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Search_Elasticsearch["<strong>OrchardCore.Search.Elasticsearch</strong>"]
    OrchardCore_Admin_Abstractions["OrchardCore.Admin.Abstractions"]
    OrchardCore_Search_Elasticsearch --> OrchardCore_Admin_Abstractions
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_Search_Elasticsearch --> OrchardCore_Module_Targets
    OrchardCore_ContentManagement_GraphQL["OrchardCore.ContentManagement.GraphQL"]
    OrchardCore_Search_Elasticsearch --> OrchardCore_ContentManagement_GraphQL
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_Search_Elasticsearch --> OrchardCore_DisplayManagement
    OrchardCore_Navigation_Core["OrchardCore.Navigation.Core"]
    OrchardCore_Search_Elasticsearch --> OrchardCore_Navigation_Core
    OrchardCore_Queries_Core["OrchardCore.Queries.Core"]
    OrchardCore_Search_Elasticsearch --> OrchardCore_Queries_Core
    OrchardCore_ResourceManagement["OrchardCore.ResourceManagement"]
    OrchardCore_Search_Elasticsearch --> OrchardCore_ResourceManagement
    OrchardCore_Search_Elasticsearch_Core["OrchardCore.Search.Elasticsearch.Core"]
    OrchardCore_Search_Elasticsearch --> OrchardCore_Search_Elasticsearch_Core
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Search_Elasticsearch
```

## Project References
- OrchardCore.Admin.Abstractions
- OrchardCore.Module.Targets
- OrchardCore.ContentManagement.GraphQL
- OrchardCore.DisplayManagement
- OrchardCore.Navigation.Core
- OrchardCore.Queries.Core
- OrchardCore.ResourceManagement
- OrchardCore.Search.Elasticsearch.Core

## Consumed By
- OrchardCore.Application.Cms.Core.Targets

## External NuGet Packages
| Package | Version |
|---------|---------||
| Elastic.Clients.Elasticsearch |  |


---

*[Back to Index](../../index.md)*
