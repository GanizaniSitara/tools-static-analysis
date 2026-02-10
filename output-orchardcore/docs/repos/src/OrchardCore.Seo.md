# OrchardCore.Seo

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.Seo/OrchardCore.Seo.csproj` |
| Project References | 15 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Seo["<strong>OrchardCore.Seo</strong>"]
    OrchardCore_Admin_Abstractions["OrchardCore.Admin.Abstractions"]
    OrchardCore_Seo --> OrchardCore_Admin_Abstractions
    OrchardCore_Apis_GraphQL_Abstractions["OrchardCore.Apis.GraphQL.Abstractions"]
    OrchardCore_Seo --> OrchardCore_Apis_GraphQL_Abstractions
    OrchardCore_ContentManagement["OrchardCore.ContentManagement"]
    OrchardCore_Seo --> OrchardCore_ContentManagement
    OrchardCore_ContentManagement_Display["OrchardCore.ContentManagement.Display"]
    OrchardCore_Seo --> OrchardCore_ContentManagement_Display
    OrchardCore_ContentManagement_Abstractions["OrchardCore.ContentManagement.Abstractions"]
    OrchardCore_Seo --> OrchardCore_ContentManagement_Abstractions
    OrchardCore_ContentTypes_Abstractions["OrchardCore.ContentTypes.Abstractions"]
    OrchardCore_Seo --> OrchardCore_ContentTypes_Abstractions
    OrchardCore_DisplayManagement["OrchardCore.DisplayManagement"]
    OrchardCore_Seo --> OrchardCore_DisplayManagement
    OrchardCore_Media_Core["OrchardCore.Media.Core"]
    OrchardCore_Seo --> OrchardCore_Media_Core
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_Seo --> OrchardCore_Module_Targets
    OrchardCore_Navigation_Core["OrchardCore.Navigation.Core"]
    OrchardCore_Seo --> OrchardCore_Navigation_Core
    OrchardCore_Recipes_Abstractions["OrchardCore.Recipes.Abstractions"]
    OrchardCore_Seo --> OrchardCore_Recipes_Abstractions
    OrchardCore_ResourceManagement["OrchardCore.ResourceManagement"]
    OrchardCore_Seo --> OrchardCore_ResourceManagement
    OrchardCore_Seo_Abstractions["OrchardCore.Seo.Abstractions"]
    OrchardCore_Seo --> OrchardCore_Seo_Abstractions
    OrchardCore_Shortcodes_Abstractions["OrchardCore.Shortcodes.Abstractions"]
    OrchardCore_Seo --> OrchardCore_Shortcodes_Abstractions
    OrchardCore_Indexing["OrchardCore.Indexing"]
    OrchardCore_Seo --> OrchardCore_Indexing
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Seo
```

## Project References
- OrchardCore.Admin.Abstractions
- OrchardCore.Apis.GraphQL.Abstractions
- OrchardCore.ContentManagement
- OrchardCore.ContentManagement.Display
- OrchardCore.ContentManagement.Abstractions
- OrchardCore.ContentTypes.Abstractions
- OrchardCore.DisplayManagement
- OrchardCore.Media.Core
- OrchardCore.Module.Targets
- OrchardCore.Navigation.Core
- OrchardCore.Recipes.Abstractions
- OrchardCore.ResourceManagement
- OrchardCore.Seo.Abstractions
- OrchardCore.Shortcodes.Abstractions
- OrchardCore.Indexing

## Consumed By
- OrchardCore.Application.Cms.Core.Targets


---

*[Back to Index](../../index.md)*
