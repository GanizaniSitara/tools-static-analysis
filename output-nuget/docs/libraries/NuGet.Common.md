# NuGet.Common

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Core/NuGet.Common/NuGet.Common.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 4 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Common["<strong>NuGet.Common</strong>"]
    NuGet_Frameworks["NuGet.Frameworks"]
    NuGet_Common --> NuGet_Frameworks
    NuGet_Common_Test["NuGet.Common.Test"]
    NuGet_Common_Test -.-> NuGet_Common
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_Common
    NuGet_LibraryModel["NuGet.LibraryModel"]
    NuGet_LibraryModel -.-> NuGet_Common
    NuGet_Configuration["NuGet.Configuration"]
    NuGet_Configuration -.-> NuGet_Common
```

## Project References
- NuGet.Frameworks

## Consumed By
- NuGet.Common.Test
- NuGet.VisualStudio.Client
- NuGet.LibraryModel
- NuGet.Configuration

## External NuGet Packages
| Package | Version |
|---------|---------||
| System.Collections.Immutable |  |


---

*[Back to Index](../index.md)*
