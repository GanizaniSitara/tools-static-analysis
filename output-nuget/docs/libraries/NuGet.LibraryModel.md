# NuGet.LibraryModel

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Core/NuGet.LibraryModel/NuGet.LibraryModel.csproj` |
| Project References | 2 |
| NuGet Dependencies | 1 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_LibraryModel["<strong>NuGet.LibraryModel</strong>"]
    NuGet_Common["NuGet.Common"]
    NuGet_LibraryModel --> NuGet_Common
    NuGet_Versioning["NuGet.Versioning"]
    NuGet_LibraryModel --> NuGet_Versioning
    NuGet_LibraryModel_Tests["NuGet.LibraryModel.Tests"]
    NuGet_LibraryModel_Tests -.-> NuGet_LibraryModel
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_LibraryModel
    NuGet_DependencyResolver_Core["NuGet.DependencyResolver.Core"]
    NuGet_DependencyResolver_Core -.-> NuGet_LibraryModel
```

## Project References
- NuGet.Common
- NuGet.Versioning

## Consumed By
- NuGet.LibraryModel.Tests
- NuGet.VisualStudio.Client
- NuGet.DependencyResolver.Core

## External NuGet Packages
| Package | Version |
|---------|---------||
| System.Collections.Immutable |  |


---

*[Back to Index](../index.md)*
