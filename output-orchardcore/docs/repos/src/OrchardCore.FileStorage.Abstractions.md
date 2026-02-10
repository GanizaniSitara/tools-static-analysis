# OrchardCore.FileStorage.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.FileStorage.Abstractions/OrchardCore.FileStorage.Abstractions.csproj` |
| Project References | 0 |
| NuGet Dependencies | 0 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_FileStorage_Abstractions["<strong>OrchardCore.FileStorage.Abstractions</strong>"]
    OrchardCore_FileStorage_AzureBlob["OrchardCore.FileStorage.AzureBlob"]
    OrchardCore_FileStorage_AzureBlob -.-> OrchardCore_FileStorage_Abstractions
    OrchardCore_FileStorage_FileSystem["OrchardCore.FileStorage.FileSystem"]
    OrchardCore_FileStorage_FileSystem -.-> OrchardCore_FileStorage_Abstractions
    OrchardCore_Media_Abstractions["OrchardCore.Media.Abstractions"]
    OrchardCore_Media_Abstractions -.-> OrchardCore_FileStorage_Abstractions
    OrchardCore_Media_Core["OrchardCore.Media.Core"]
    OrchardCore_Media_Core -.-> OrchardCore_FileStorage_Abstractions
    OrchardCore_FileStorage_AmazonS3["OrchardCore.FileStorage.AmazonS3"]
    OrchardCore_FileStorage_AmazonS3 -.-> OrchardCore_FileStorage_Abstractions
```

## Consumed By
- OrchardCore.FileStorage.AzureBlob
- OrchardCore.FileStorage.FileSystem
- OrchardCore.Media.Abstractions
- OrchardCore.Media.Core
- OrchardCore.FileStorage.AmazonS3


---

*[Back to Index](../../index.md)*
