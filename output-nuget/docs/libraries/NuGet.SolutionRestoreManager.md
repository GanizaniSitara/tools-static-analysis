# NuGet.SolutionRestoreManager

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Clients/NuGet.SolutionRestoreManager/NuGet.SolutionRestoreManager.csproj` |
| Project References | 3 |
| NuGet Dependencies | 2 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_SolutionRestoreManager["<strong>NuGet.SolutionRestoreManager</strong>"]
    NuGet_PackageManagement["NuGet.PackageManagement"]
    NuGet_SolutionRestoreManager --> NuGet_PackageManagement
    NuGet_PackageManagement_VisualStudio["NuGet.PackageManagement.VisualStudio"]
    NuGet_SolutionRestoreManager --> NuGet_PackageManagement_VisualStudio
    NuGet_VisualStudio_Common["NuGet.VisualStudio.Common"]
    NuGet_SolutionRestoreManager --> NuGet_VisualStudio_Common
    NuGet_SolutionRestoreManager_Test["NuGet.SolutionRestoreManager.Test"]
    NuGet_SolutionRestoreManager_Test -.-> NuGet_SolutionRestoreManager
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_SolutionRestoreManager
```

## Project References
- NuGet.PackageManagement
- NuGet.PackageManagement.VisualStudio
- NuGet.VisualStudio.Common

## Consumed By
- NuGet.SolutionRestoreManager.Test
- NuGet.VisualStudio.Client

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.VisualStudio.Sdk |  |
| Microsoft.VSSDK.BuildTools |  |


---

*[Back to Index](../index.md)*
