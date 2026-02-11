# NuGet.Frameworks

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Core/NuGet.Frameworks/NuGet.Frameworks.csproj` |
| Project References | 0 |
| NuGet Dependencies | 0 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Frameworks["<strong>NuGet.Frameworks</strong>"]
    NuGet_Frameworks_Test["NuGet.Frameworks.Test"]
    NuGet_Frameworks_Test -.-> NuGet_Frameworks
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_Frameworks
    NuGet_Common["NuGet.Common"]
    NuGet_Common -.-> NuGet_Frameworks
```

## Consumed By
- NuGet.Frameworks.Test
- NuGet.VisualStudio.Client
- NuGet.Common


---

*[Back to Index](../index.md)*
