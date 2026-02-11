# NuGet.Versioning

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Core/NuGet.Versioning/NuGet.Versioning.csproj` |
| Project References | 0 |
| NuGet Dependencies | 0 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Versioning["<strong>NuGet.Versioning</strong>"]
    NuGet_Versioning_Test["NuGet.Versioning.Test"]
    NuGet_Versioning_Test -.-> NuGet_Versioning
    TestablePlugin["TestablePlugin"]
    TestablePlugin -.-> NuGet_Versioning
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_Versioning
    NuGet_Packaging["NuGet.Packaging"]
    NuGet_Packaging -.-> NuGet_Versioning
    NuGet_LibraryModel["NuGet.LibraryModel"]
    NuGet_LibraryModel -.-> NuGet_Versioning
```

## Consumed By
- NuGet.Versioning.Test
- TestablePlugin
- NuGet.VisualStudio.Client
- NuGet.Packaging
- NuGet.LibraryModel


---

*[Back to Index](../index.md)*
