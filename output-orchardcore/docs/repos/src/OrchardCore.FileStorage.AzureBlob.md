# OrchardCore.FileStorage.AzureBlob

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.FileStorage.AzureBlob/OrchardCore.FileStorage.AzureBlob.csproj` |
| Project References | 3 |
| NuGet Dependencies | 1 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_FileStorage_AzureBlob["<strong>OrchardCore.FileStorage.AzureBlob</strong>"]
    OrchardCore_Abstractions["OrchardCore.Abstractions"]
    OrchardCore_FileStorage_AzureBlob --> OrchardCore_Abstractions
    OrchardCore_FileStorage_Abstractions["OrchardCore.FileStorage.Abstractions"]
    OrchardCore_FileStorage_AzureBlob --> OrchardCore_FileStorage_Abstractions
    OrchardCore_Liquid_Abstractions["OrchardCore.Liquid.Abstractions"]
    OrchardCore_FileStorage_AzureBlob --> OrchardCore_Liquid_Abstractions
    OrchardCore_Media_Azure["OrchardCore.Media.Azure"]
    OrchardCore_Media_Azure -.-> OrchardCore_FileStorage_AzureBlob
    OrchardCore_Shells_Azure["OrchardCore.Shells.Azure"]
    OrchardCore_Shells_Azure -.-> OrchardCore_FileStorage_AzureBlob
```

## Project References
- OrchardCore.Abstractions
- OrchardCore.FileStorage.Abstractions
- OrchardCore.Liquid.Abstractions

## Consumed By
- OrchardCore.Media.Azure
- OrchardCore.Shells.Azure

## External NuGet Packages
| Package | Version |
|---------|---------||
| Azure.Storage.Blobs |  |


---

*[Back to Index](../../index.md)*
