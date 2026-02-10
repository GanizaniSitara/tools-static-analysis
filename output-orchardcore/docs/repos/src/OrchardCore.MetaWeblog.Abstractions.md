# OrchardCore.MetaWeblog.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.MetaWeblog.Abstractions/OrchardCore.MetaWeblog.Abstractions.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 6 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_MetaWeblog_Abstractions["<strong>OrchardCore.MetaWeblog.Abstractions</strong>"]
    OrchardCore_XmlRpc_Abstractions["OrchardCore.XmlRpc.Abstractions"]
    OrchardCore_MetaWeblog_Abstractions --> OrchardCore_XmlRpc_Abstractions
    OrchardCore_ContentManagement_Abstractions["OrchardCore.ContentManagement.Abstractions"]
    OrchardCore_MetaWeblog_Abstractions --> OrchardCore_ContentManagement_Abstractions
    OrchardCore_Autoroute["OrchardCore.Autoroute"]
    OrchardCore_Autoroute -.-> OrchardCore_MetaWeblog_Abstractions
    OrchardCore_Lists["OrchardCore.Lists"]
    OrchardCore_Lists -.-> OrchardCore_MetaWeblog_Abstractions
    OrchardCore_Media["OrchardCore.Media"]
    OrchardCore_Media -.-> OrchardCore_MetaWeblog_Abstractions
    OrchardCore_Html["OrchardCore.Html"]
    OrchardCore_Html -.-> OrchardCore_MetaWeblog_Abstractions
    OrchardCore_Title["OrchardCore.Title"]
    OrchardCore_Title -.-> OrchardCore_MetaWeblog_Abstractions
    OrchardCore_Markdown["OrchardCore.Markdown"]
    OrchardCore_Markdown -.-> OrchardCore_MetaWeblog_Abstractions
```

## Project References
- OrchardCore.XmlRpc.Abstractions
- OrchardCore.ContentManagement.Abstractions

## Consumed By
- OrchardCore.Autoroute
- OrchardCore.Lists
- OrchardCore.Media
- OrchardCore.Html
- OrchardCore.Title
- OrchardCore.Markdown


---

*[Back to Index](../../index.md)*
