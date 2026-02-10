# OrchardCore.Media.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Media.Core/OrchardCore.Media.Core.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 4 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Media_Core["<strong>OrchardCore.Media.Core</strong>"]
    OrchardCore_FileStorage_Abstractions["OrchardCore.FileStorage.Abstractions"]
    OrchardCore_Media_Core --> OrchardCore_FileStorage_Abstractions
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Media_Core --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Media_Abstractions["OrchardCore.Media.Abstractions"]
    OrchardCore_Media_Core --> OrchardCore_Media_Abstractions
    OrchardCore_Media_Azure["OrchardCore.Media.Azure"]
    OrchardCore_Media_Azure -.-> OrchardCore_Media_Core
    OrchardCore_Media_AmazonS3["OrchardCore.Media.AmazonS3"]
    OrchardCore_Media_AmazonS3 -.-> OrchardCore_Media_Core
    OrchardCore_Media["OrchardCore.Media"]
    OrchardCore_Media -.-> OrchardCore_Media_Core
    OrchardCore_Seo["OrchardCore.Seo"]
    OrchardCore_Seo -.-> OrchardCore_Media_Core
```

## Project References
- OrchardCore.FileStorage.Abstractions
- OrchardCore.Infrastructure.Abstractions
- OrchardCore.Media.Abstractions

## Consumed By
- OrchardCore.Media.Azure
- OrchardCore.Media.AmazonS3
- OrchardCore.Media
- OrchardCore.Seo


---

*[Back to Index](../../index.md)*
