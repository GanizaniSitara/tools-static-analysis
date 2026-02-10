# OrchardCore.FileStorage.AmazonS3

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.FileStorage.AmazonS3/OrchardCore.FileStorage.AmazonS3.csproj` |
| Project References | 2 |
| NuGet Dependencies | 2 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_FileStorage_AmazonS3["<strong>OrchardCore.FileStorage.AmazonS3</strong>"]
    OrchardCore_Abstractions["OrchardCore.Abstractions"]
    OrchardCore_FileStorage_AmazonS3 --> OrchardCore_Abstractions
    OrchardCore_FileStorage_Abstractions["OrchardCore.FileStorage.Abstractions"]
    OrchardCore_FileStorage_AmazonS3 --> OrchardCore_FileStorage_Abstractions
    OrchardCore_Media_AmazonS3["OrchardCore.Media.AmazonS3"]
    OrchardCore_Media_AmazonS3 -.-> OrchardCore_FileStorage_AmazonS3
```

## Project References
- OrchardCore.Abstractions
- OrchardCore.FileStorage.Abstractions

## Consumed By
- OrchardCore.Media.AmazonS3

## External NuGet Packages
| Package | Version |
|---------|---------||
| AWSSDK.S3 |  |
| AWSSDK.Extensions.NETCore.Setup |  |


---

*[Back to Index](../../index.md)*
