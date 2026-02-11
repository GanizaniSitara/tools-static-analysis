# NuGet.VisualStudio.Interop

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Clients/NuGet.VisualStudio.Interop/NuGet.VisualStudio.Interop.csproj` |
| Project References | 1 |
| NuGet Dependencies | 3 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_VisualStudio_Interop["<strong>NuGet.VisualStudio.Interop</strong>"]
    NuGet_VisualStudio["NuGet.VisualStudio"]
    NuGet_VisualStudio_Interop --> NuGet_VisualStudio
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_VisualStudio_Interop
    NuGet_Tools["NuGet.Tools"]
    NuGet_Tools -.-> NuGet_VisualStudio_Interop
```

## Project References
- NuGet.VisualStudio

## Consumed By
- NuGet.VisualStudio.Client
- NuGet.Tools

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.VisualStudio.Shell.15.0 |  |
| Microsoft.VisualStudio.Shell.Styles |  |
| Newtonsoft.Json |  |


---

*[Back to Index](../index.md)*
