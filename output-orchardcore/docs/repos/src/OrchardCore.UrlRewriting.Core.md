# OrchardCore.UrlRewriting.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.UrlRewriting.Core/OrchardCore.UrlRewriting.Core.csproj` |
| Project References | 4 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_UrlRewriting_Core["<strong>OrchardCore.UrlRewriting.Core</strong>"]
    OrchardCore_Admin_Abstractions["OrchardCore.Admin.Abstractions"]
    OrchardCore_UrlRewriting_Core --> OrchardCore_Admin_Abstractions
    OrchardCore_Data_Abstractions["OrchardCore.Data.Abstractions"]
    OrchardCore_UrlRewriting_Core --> OrchardCore_Data_Abstractions
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_UrlRewriting_Core --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_UrlRewriting_Abstractions["OrchardCore.UrlRewriting.Abstractions"]
    OrchardCore_UrlRewriting_Core --> OrchardCore_UrlRewriting_Abstractions
    OrchardCore_UrlRewriting["OrchardCore.UrlRewriting"]
    OrchardCore_UrlRewriting -.-> OrchardCore_UrlRewriting_Core
```

## Project References
- OrchardCore.Admin.Abstractions
- OrchardCore.Data.Abstractions
- OrchardCore.Infrastructure.Abstractions
- OrchardCore.UrlRewriting.Abstractions

## Consumed By
- OrchardCore.UrlRewriting


---

*[Back to Index](../../index.md)*
