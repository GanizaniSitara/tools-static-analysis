# OrchardCore.Contents

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.Contents/OrchardCore.Contents.csproj` |
| Project References | 24 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Contents["<strong>OrchardCore.Contents</strong>"]
    OrchardCore_Admin_Abstractions["OrchardCore.Admin.Abstractions"]
    OrchardCore_Contents --> OrchardCore_Admin_Abstractions
    OrchardCore_AdminMenu_Abstractions["OrchardCore.AdminMenu.Abstractions"]
    OrchardCore_Contents --> OrchardCore_AdminMenu_Abstractions
    OrchardCore_AuditTrail_Abstractions["OrchardCore.AuditTrail.Abstractions"]
    OrchardCore_Contents --> OrchardCore_AuditTrail_Abstractions
    OrchardCore_ContentManagement_GraphQL["OrchardCore.ContentManagement.GraphQL"]
    OrchardCore_Contents --> OrchardCore_ContentManagement_GraphQL
    OrchardCore_Contents_Core["OrchardCore.Contents.Core"]
    OrchardCore_Contents --> OrchardCore_Contents_Core
    OrchardCore_Contents_TagHelpers["OrchardCore.Contents.TagHelpers"]
    OrchardCore_Contents --> OrchardCore_Contents_TagHelpers
    OrchardCore_ContentManagement["OrchardCore.ContentManagement"]
    OrchardCore_Contents --> OrchardCore_ContentManagement
    OrchardCore_ContentManagement_Display["OrchardCore.ContentManagement.Display"]
    OrchardCore_Contents --> OrchardCore_ContentManagement_Display
    OrchardCore_ContentTypes_Abstractions["OrchardCore.ContentTypes.Abstractions"]
    OrchardCore_Contents --> OrchardCore_ContentTypes_Abstractions
    OrchardCore_Deployment_Abstractions["OrchardCore.Deployment.Abstractions"]
    OrchardCore_Contents --> OrchardCore_Deployment_Abstractions
    OrchardCore_Deployment_Core["OrchardCore.Deployment.Core"]
    OrchardCore_Contents --> OrchardCore_Deployment_Core
    OrchardCore_DisplayManagement_Liquid["OrchardCore.DisplayManagement.Liquid"]
    OrchardCore_Contents --> OrchardCore_DisplayManagement_Liquid
    OrchardCore_Feeds_Abstractions["OrchardCore.Feeds.Abstractions"]
    OrchardCore_Contents --> OrchardCore_Feeds_Abstractions
    OrchardCore_Indexing_Abstractions["OrchardCore.Indexing.Abstractions"]
    OrchardCore_Contents --> OrchardCore_Indexing_Abstractions
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_Contents --> OrchardCore_Module_Targets
    OrchardCore_Liquid_Abstractions["OrchardCore.Liquid.Abstractions"]
    OrchardCore_Contents --> OrchardCore_Liquid_Abstractions
    OrchardCore_Localization_Abstractions["OrchardCore.Localization.Abstractions"]
    OrchardCore_Contents --> OrchardCore_Localization_Abstractions
    OrchardCore_Navigation_Core["OrchardCore.Navigation.Core"]
    OrchardCore_Contents --> OrchardCore_Navigation_Core
    OrchardCore_Recipes_Abstractions["OrchardCore.Recipes.Abstractions"]
    OrchardCore_Contents --> OrchardCore_Recipes_Abstractions
    OrchardCore_ResourceManagement["OrchardCore.ResourceManagement"]
    OrchardCore_Contents --> OrchardCore_ResourceManagement
    OrchardCore_Settings_Core["OrchardCore.Settings.Core"]
    OrchardCore_Contents --> OrchardCore_Settings_Core
    OrchardCore_Sitemaps_Abstractions["OrchardCore.Sitemaps.Abstractions"]
    OrchardCore_Contents --> OrchardCore_Sitemaps_Abstractions
    OrchardCore_Users_Abstractions["OrchardCore.Users.Abstractions"]
    OrchardCore_Contents --> OrchardCore_Users_Abstractions
    OrchardCore_Workflows_Abstractions["OrchardCore.Workflows.Abstractions"]
    OrchardCore_Contents --> OrchardCore_Workflows_Abstractions
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Contents
```

## Project References
- OrchardCore.Admin.Abstractions
- OrchardCore.AdminMenu.Abstractions
- OrchardCore.AuditTrail.Abstractions
- OrchardCore.ContentManagement.GraphQL
- OrchardCore.Contents.Core
- OrchardCore.Contents.TagHelpers
- OrchardCore.ContentManagement
- OrchardCore.ContentManagement.Display
- OrchardCore.ContentTypes.Abstractions
- OrchardCore.Deployment.Abstractions
- OrchardCore.Deployment.Core
- OrchardCore.DisplayManagement.Liquid
- OrchardCore.Feeds.Abstractions
- OrchardCore.Indexing.Abstractions
- OrchardCore.Module.Targets
- OrchardCore.Liquid.Abstractions
- OrchardCore.Localization.Abstractions
- OrchardCore.Navigation.Core
- OrchardCore.Recipes.Abstractions
- OrchardCore.ResourceManagement
- OrchardCore.Settings.Core
- OrchardCore.Sitemaps.Abstractions
- OrchardCore.Users.Abstractions
- OrchardCore.Workflows.Abstractions

## Consumed By
- OrchardCore.Application.Cms.Core.Targets


---

*[Back to Index](../../index.md)*
