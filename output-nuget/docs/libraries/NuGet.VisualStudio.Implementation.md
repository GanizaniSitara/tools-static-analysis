# NuGet.VisualStudio.Implementation

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Clients/NuGet.VisualStudio.Implementation/NuGet.VisualStudio.Implementation.csproj` |
| Project References | 4 |
| NuGet Dependencies | 13 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_VisualStudio_Implementation["<strong>NuGet.VisualStudio.Implementation</strong>"]
    NuGet_PackageManagement_VisualStudio["NuGet.PackageManagement.VisualStudio"]
    NuGet_VisualStudio_Implementation --> NuGet_PackageManagement_VisualStudio
    NuGet_VisualStudio_Contracts["NuGet.VisualStudio.Contracts"]
    NuGet_VisualStudio_Implementation --> NuGet_VisualStudio_Contracts
    NuGet_VisualStudio["NuGet.VisualStudio"]
    NuGet_VisualStudio_Implementation --> NuGet_VisualStudio
    NuGet_VisualStudio_Common["NuGet.VisualStudio.Common"]
    NuGet_VisualStudio_Implementation --> NuGet_VisualStudio_Common
    NuGet_VisualStudio_Implementation_Test["NuGet.VisualStudio.Implementation.Test"]
    NuGet_VisualStudio_Implementation_Test -.-> NuGet_VisualStudio_Implementation
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_VisualStudio_Implementation
    NuGet_Tools["NuGet.Tools"]
    NuGet_Tools -.-> NuGet_VisualStudio_Implementation
```

## Project References
- NuGet.PackageManagement.VisualStudio
- NuGet.VisualStudio.Contracts
- NuGet.VisualStudio
- NuGet.VisualStudio.Common

## Consumed By
- NuGet.VisualStudio.Implementation.Test
- NuGet.VisualStudio.Client
- NuGet.Tools

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.Build |  |
| Microsoft.Build.Framework |  |
| Microsoft.Build.Tasks.Core |  |
| Microsoft.Build.Utilities.Core |  |
| Microsoft.CodeAnalysis |  |
| Microsoft.CodeAnalysis.Common |  |
| Microsoft.CodeAnalysis.Features |  |
| Microsoft.CodeAnalysis.Workspaces.Common |  |
| Microsoft.VisualStudio.LanguageServices |  |
| Microsoft.VisualStudio.ProjectSystem.Managed.VS |  |
| Microsoft.VisualStudio.ProjectSystem.VS |  |
| Microsoft.VisualStudio.Sdk |  |
| Microsoft.VSSDK.BuildTools |  |


---

*[Back to Index](../index.md)*
