# OrchardCore.UrlRewriting.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.UrlRewriting.Abstractions/OrchardCore.UrlRewriting.Abstractions.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_UrlRewriting_Abstractions["<strong>OrchardCore.UrlRewriting.Abstractions</strong>"]
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_UrlRewriting_Abstractions --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_UrlRewriting_Core["OrchardCore.UrlRewriting.Core"]
    OrchardCore_UrlRewriting_Core -.-> OrchardCore_UrlRewriting_Abstractions
```

## Project References
- OrchardCore.Infrastructure.Abstractions

## Consumed By
- OrchardCore.UrlRewriting.Core


---

*[Back to Index](../../index.md)*
