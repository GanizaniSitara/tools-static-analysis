# OrchardCore.Application.Cms.Core.Targets

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Application.Cms.Core.Targets/OrchardCore.Application.Cms.Core.Targets.csproj` |
| Project References | 93 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Application_Cms_Core_Targets["<strong>OrchardCore.Application.Cms.Core.Targets</strong>"]
    OrchardCore_Application_Targets["OrchardCore.Application.Targets"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Application_Targets
    OrchardCore_Admin["OrchardCore.Admin"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Admin
    OrchardCore_AdminDashboard["OrchardCore.AdminDashboard"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_AdminDashboard
    OrchardCore_AdminMenu["OrchardCore.AdminMenu"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_AdminMenu
    OrchardCore_Alias["OrchardCore.Alias"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Alias
    OrchardCore_Apis_GraphQL["OrchardCore.Apis.GraphQL"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Apis_GraphQL
    OrchardCore_ArchiveLater["OrchardCore.ArchiveLater"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_ArchiveLater
    OrchardCore_AuditTrail["OrchardCore.AuditTrail"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_AuditTrail
    OrchardCore_Autoroute["OrchardCore.Autoroute"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Autoroute
    OrchardCore_AutoSetup["OrchardCore.AutoSetup"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_AutoSetup
    OrchardCore_BackgroundTasks["OrchardCore.BackgroundTasks"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_BackgroundTasks
    OrchardCore_ContentFields["OrchardCore.ContentFields"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_ContentFields
    OrchardCore_ContentLocalization["OrchardCore.ContentLocalization"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_ContentLocalization
    OrchardCore_ContentPreview["OrchardCore.ContentPreview"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_ContentPreview
    OrchardCore_Contents["OrchardCore.Contents"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Contents
    OrchardCore_ContentTypes["OrchardCore.ContentTypes"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_ContentTypes
    OrchardCore_Cors["OrchardCore.Cors"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Cors
    OrchardCore_CustomSettings["OrchardCore.CustomSettings"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_CustomSettings
    OrchardCore_DataProtection_Azure["OrchardCore.DataProtection.Azure"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_DataProtection_Azure
    OrchardCore_Deployment["OrchardCore.Deployment"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Deployment
    OrchardCore_Deployment_Remote["OrchardCore.Deployment.Remote"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Deployment_Remote
    OrchardCore_Diagnostics["OrchardCore.Diagnostics"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Diagnostics
    OrchardCore_DynamicCache["OrchardCore.DynamicCache"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_DynamicCache
    OrchardCore_Email["OrchardCore.Email"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Email
    OrchardCore_Email_Azure["OrchardCore.Email.Azure"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Email_Azure
    OrchardCore_Email_Smtp["OrchardCore.Email.Smtp"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Email_Smtp
    OrchardCore_Facebook["OrchardCore.Facebook"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Facebook
    OrchardCore_Features["OrchardCore.Features"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Features
    OrchardCore_Feeds["OrchardCore.Feeds"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Feeds
    OrchardCore_Flows["OrchardCore.Flows"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Flows
    OrchardCore_Forms["OrchardCore.Forms"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Forms
    OrchardCore_GitHub["OrchardCore.GitHub"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_GitHub
    OrchardCore_Google["OrchardCore.Google"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Google
    OrchardCore_HealthChecks["OrchardCore.HealthChecks"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_HealthChecks
    OrchardCore_HomeRoute["OrchardCore.HomeRoute"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_HomeRoute
    OrchardCore_Html["OrchardCore.Html"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Html
    OrchardCore_Https["OrchardCore.Https"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Https
    OrchardCore_Indexing["OrchardCore.Indexing"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Indexing
    OrchardCore_Infrastructure["OrchardCore.Infrastructure"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Infrastructure
    OrchardCore_Layers["OrchardCore.Layers"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Layers
    OrchardCore_Liquid["OrchardCore.Liquid"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Liquid
    OrchardCore_Lists["OrchardCore.Lists"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Lists
    OrchardCore_Localization["OrchardCore.Localization"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Localization
    OrchardCore_DataLocalization["OrchardCore.DataLocalization"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_DataLocalization
    OrchardCore_Markdown["OrchardCore.Markdown"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Markdown
    OrchardCore_Media["OrchardCore.Media"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Media
    OrchardCore_Media_AmazonS3["OrchardCore.Media.AmazonS3"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Media_AmazonS3
    OrchardCore_Media_Azure["OrchardCore.Media.Azure"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Media_Azure
    OrchardCore_Media_Indexing_OpenXML["OrchardCore.Media.Indexing.OpenXML"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Media_Indexing_OpenXML
    OrchardCore_Media_Indexing_Pdf["OrchardCore.Media.Indexing.Pdf"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Media_Indexing_Pdf
    OrchardCore_Microsoft_Authentication["OrchardCore.Microsoft.Authentication"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Microsoft_Authentication
    OrchardCore_MiniProfiler["OrchardCore.MiniProfiler"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_MiniProfiler
    OrchardCore_Menu["OrchardCore.Menu"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Menu
    OrchardCore_Navigation["OrchardCore.Navigation"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Navigation
    OrchardCore_Notifications["OrchardCore.Notifications"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Notifications
    OrchardCore_OpenId["OrchardCore.OpenId"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_OpenId
    OrchardCore_Placements["OrchardCore.Placements"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Placements
    OrchardCore_PublishLater["OrchardCore.PublishLater"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_PublishLater
    OrchardCore_Queries["OrchardCore.Queries"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Queries
    OrchardCore_ReCaptcha["OrchardCore.ReCaptcha"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_ReCaptcha
    OrchardCore_Recipes["OrchardCore.Recipes"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Recipes
    OrchardCore_Redis["OrchardCore.Redis"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Redis
    OrchardCore_Resources["OrchardCore.Resources"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Resources
    OrchardCore_ResponseCompression["OrchardCore.ResponseCompression"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_ResponseCompression
    OrchardCore_UrlRewriting["OrchardCore.UrlRewriting"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_UrlRewriting
    OrchardCore_ReverseProxy["OrchardCore.ReverseProxy"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_ReverseProxy
    OrchardCore_Rules["OrchardCore.Rules"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Rules
    OrchardCore_Roles["OrchardCore.Roles"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Roles
    OrchardCore_Scripting["OrchardCore.Scripting"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Scripting
    OrchardCore_Search["OrchardCore.Search"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Search
    OrchardCore_Search_AzureAI["OrchardCore.Search.AzureAI"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Search_AzureAI
    OrchardCore_Search_Elasticsearch["OrchardCore.Search.Elasticsearch"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Search_Elasticsearch
    OrchardCore_Search_Lucene["OrchardCore.Search.Lucene"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Search_Lucene
    OrchardCore_Security["OrchardCore.Security"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Security
    OrchardCore_Seo["OrchardCore.Seo"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Seo
    OrchardCore_Settings["OrchardCore.Settings"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Settings
    OrchardCore_Setup["OrchardCore.Setup"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Setup
    OrchardCore_Sitemaps["OrchardCore.Sitemaps"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Sitemaps
    OrchardCore_Shortcodes["OrchardCore.Shortcodes"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Shortcodes
    OrchardCore_Sms["OrchardCore.Sms"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Sms
    OrchardCore_Sms_Azure["OrchardCore.Sms.Azure"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Sms_Azure
    OrchardCore_Spatial["OrchardCore.Spatial"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Spatial
    OrchardCore_Taxonomies["OrchardCore.Taxonomies"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Taxonomies
    OrchardCore_Templates["OrchardCore.Templates"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Templates
    OrchardCore_Tenants["OrchardCore.Tenants"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Tenants
    OrchardCore_Themes["OrchardCore.Themes"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Themes
    OrchardCore_Title["OrchardCore.Title"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Title
    OrchardCore_Twitter["OrchardCore.Twitter"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Twitter
    OrchardCore_Users["OrchardCore.Users"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Users
    OrchardCore_Widgets["OrchardCore.Widgets"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Widgets
    OrchardCore_Workflows["OrchardCore.Workflows"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_Workflows
    OrchardCore_XmlRpc["OrchardCore.XmlRpc"]
    OrchardCore_Application_Cms_Core_Targets --> OrchardCore_XmlRpc
    TheAdmin["TheAdmin"]
    OrchardCore_Application_Cms_Core_Targets --> TheAdmin
    OrchardCore_Application_Cms_Targets["OrchardCore.Application.Cms.Targets"]
    OrchardCore_Application_Cms_Targets -.-> OrchardCore_Application_Cms_Core_Targets
    OrchardCore_Application_Pages["OrchardCore.Application.Pages"]
    OrchardCore_Application_Pages -.-> OrchardCore_Application_Cms_Core_Targets
```

## Project References
- OrchardCore.Application.Targets
- OrchardCore.Admin
- OrchardCore.AdminDashboard
- OrchardCore.AdminMenu
- OrchardCore.Alias
- OrchardCore.Apis.GraphQL
- OrchardCore.ArchiveLater
- OrchardCore.AuditTrail
- OrchardCore.Autoroute
- OrchardCore.AutoSetup
- OrchardCore.BackgroundTasks
- OrchardCore.ContentFields
- OrchardCore.ContentLocalization
- OrchardCore.ContentPreview
- OrchardCore.Contents
- OrchardCore.ContentTypes
- OrchardCore.Cors
- OrchardCore.CustomSettings
- OrchardCore.DataProtection.Azure
- OrchardCore.Deployment
- OrchardCore.Deployment.Remote
- OrchardCore.Diagnostics
- OrchardCore.DynamicCache
- OrchardCore.Email
- OrchardCore.Email.Azure
- OrchardCore.Email.Smtp
- OrchardCore.Facebook
- OrchardCore.Features
- OrchardCore.Feeds
- OrchardCore.Flows
- OrchardCore.Forms
- OrchardCore.GitHub
- OrchardCore.Google
- OrchardCore.HealthChecks
- OrchardCore.HomeRoute
- OrchardCore.Html
- OrchardCore.Https
- OrchardCore.Indexing
- OrchardCore.Infrastructure
- OrchardCore.Layers
- OrchardCore.Liquid
- OrchardCore.Lists
- OrchardCore.Localization
- OrchardCore.DataLocalization
- OrchardCore.Markdown
- OrchardCore.Media
- OrchardCore.Media.AmazonS3
- OrchardCore.Media.Azure
- OrchardCore.Media.Indexing.OpenXML
- OrchardCore.Media.Indexing.Pdf
- OrchardCore.Microsoft.Authentication
- OrchardCore.MiniProfiler
- OrchardCore.Menu
- OrchardCore.Navigation
- OrchardCore.Notifications
- OrchardCore.OpenId
- OrchardCore.Placements
- OrchardCore.PublishLater
- OrchardCore.Queries
- OrchardCore.ReCaptcha
- OrchardCore.Recipes
- OrchardCore.Redis
- OrchardCore.Resources
- OrchardCore.ResponseCompression
- OrchardCore.UrlRewriting
- OrchardCore.ReverseProxy
- OrchardCore.Rules
- OrchardCore.Roles
- OrchardCore.Scripting
- OrchardCore.Search
- OrchardCore.Search.AzureAI
- OrchardCore.Search.Elasticsearch
- OrchardCore.Search.Lucene
- OrchardCore.Security
- OrchardCore.Seo
- OrchardCore.Settings
- OrchardCore.Setup
- OrchardCore.Sitemaps
- OrchardCore.Shortcodes
- OrchardCore.Sms
- OrchardCore.Sms.Azure
- OrchardCore.Spatial
- OrchardCore.Taxonomies
- OrchardCore.Templates
- OrchardCore.Tenants
- OrchardCore.Themes
- OrchardCore.Title
- OrchardCore.Twitter
- OrchardCore.Users
- OrchardCore.Widgets
- OrchardCore.Workflows
- OrchardCore.XmlRpc
- TheAdmin

## Consumed By
- OrchardCore.Application.Cms.Targets
- OrchardCore.Application.Pages


---

*[Back to Index](../../index.md)*
