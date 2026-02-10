# OrchardCore.Media.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Media.Abstractions/OrchardCore.Media.Abstractions.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Media_Abstractions["<strong>OrchardCore.Media.Abstractions</strong>"]
    OrchardCore_Abstractions["OrchardCore.Abstractions"]
    OrchardCore_Media_Abstractions --> OrchardCore_Abstractions
    OrchardCore_ContentManagement_Abstractions["OrchardCore.ContentManagement.Abstractions"]
    OrchardCore_Media_Abstractions --> OrchardCore_ContentManagement_Abstractions
    OrchardCore_FileStorage_Abstractions["OrchardCore.FileStorage.Abstractions"]
    OrchardCore_Media_Abstractions --> OrchardCore_FileStorage_Abstractions
    OrchardCore_Media_Indexing_Pdf["OrchardCore.Media.Indexing.Pdf"]
    OrchardCore_Media_Indexing_Pdf -.-> OrchardCore_Media_Abstractions
    OrchardCore_Lists["OrchardCore.Lists"]
    OrchardCore_Lists -.-> OrchardCore_Media_Abstractions
    OrchardCore_Media_AmazonS3["OrchardCore.Media.AmazonS3"]
    OrchardCore_Media_AmazonS3 -.-> OrchardCore_Media_Abstractions
    OrchardCore_Media_Indexing_OpenXML["OrchardCore.Media.Indexing.OpenXML"]
    OrchardCore_Media_Indexing_OpenXML -.-> OrchardCore_Media_Abstractions
    OrchardCore_Media_Core["OrchardCore.Media.Core"]
    OrchardCore_Media_Core -.-> OrchardCore_Media_Abstractions
```

## Project References
- OrchardCore.Abstractions
- OrchardCore.ContentManagement.Abstractions
- OrchardCore.FileStorage.Abstractions

## Consumed By
- OrchardCore.Media.Indexing.Pdf
- OrchardCore.Lists
- OrchardCore.Media.AmazonS3
- OrchardCore.Media.Indexing.OpenXML
- OrchardCore.Media.Core


---

*[Back to Index](../../index.md)*
