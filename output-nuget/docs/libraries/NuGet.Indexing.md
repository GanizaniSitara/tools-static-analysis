# NuGet.Indexing

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Clients/NuGet.Indexing/NuGet.Indexing.csproj` |
| Project References | 1 |
| NuGet Dependencies | 2 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Indexing["<strong>NuGet.Indexing</strong>"]
    NuGet_Protocol["NuGet.Protocol"]
    NuGet_Indexing --> NuGet_Protocol
    NuGet_Indexing_Test["NuGet.Indexing.Test"]
    NuGet_Indexing_Test -.-> NuGet_Indexing
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_Indexing
    NuGet_PackageManagement_VisualStudio["NuGet.PackageManagement.VisualStudio"]
    NuGet_PackageManagement_VisualStudio -.-> NuGet_Indexing
```

## Project References
- NuGet.Protocol

## Consumed By
- NuGet.Indexing.Test
- NuGet.VisualStudio.Client
- NuGet.PackageManagement.VisualStudio

## External NuGet Packages
| Package | Version |
|---------|---------||
| Lucene.Net |  |
| SharpZipLib |  |


---

*[Back to Index](../index.md)*
