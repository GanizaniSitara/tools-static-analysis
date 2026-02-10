# OrchardCore.Shortcodes.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Shortcodes.Abstractions/OrchardCore.Shortcodes.Abstractions.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 7 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Shortcodes_Abstractions["<strong>OrchardCore.Shortcodes.Abstractions</strong>"]
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Shortcodes_Abstractions --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Shortcodes["OrchardCore.Shortcodes"]
    OrchardCore_Shortcodes -.-> OrchardCore_Shortcodes_Abstractions
    OrchardCore_ContentFields["OrchardCore.ContentFields"]
    OrchardCore_ContentFields -.-> OrchardCore_Shortcodes_Abstractions
    OrchardCore_Liquid["OrchardCore.Liquid"]
    OrchardCore_Liquid -.-> OrchardCore_Shortcodes_Abstractions
    OrchardCore_Media["OrchardCore.Media"]
    OrchardCore_Media -.-> OrchardCore_Shortcodes_Abstractions
    OrchardCore_Seo["OrchardCore.Seo"]
    OrchardCore_Seo -.-> OrchardCore_Shortcodes_Abstractions
    OrchardCore_Html["OrchardCore.Html"]
    OrchardCore_Html -.-> OrchardCore_Shortcodes_Abstractions
    OrchardCore_Markdown["OrchardCore.Markdown"]
    OrchardCore_Markdown -.-> OrchardCore_Shortcodes_Abstractions
```

## Project References
- OrchardCore.Infrastructure.Abstractions

## Consumed By
- OrchardCore.Shortcodes
- OrchardCore.ContentFields
- OrchardCore.Liquid
- OrchardCore.Media
- OrchardCore.Seo
- OrchardCore.Html
- OrchardCore.Markdown

## External NuGet Packages
| Package | Version |
|---------|---------||
| Shortcodes |  |


---

*[Back to Index](../../index.md)*
