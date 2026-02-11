# NuGet.Tools

## Overview

| Property | Value |
|----------|-------|
| Category | Tool |
| Repository | NuGet.Client |
| Path | `src/NuGet.Clients/NuGet.Tools/NuGet.Tools.csproj` |
| Project References | 4 |
| NuGet Dependencies | 2 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Tools["<strong>NuGet.Tools</strong>"]
    NuGet_Console["NuGet.Console"]
    NuGet_Tools --> NuGet_Console
    NuGet_PackageManagement_PowerShellCmdlets["NuGet.PackageManagement.PowerShellCmdlets"]
    NuGet_Tools --> NuGet_PackageManagement_PowerShellCmdlets
    NuGet_VisualStudio_Implementation["NuGet.VisualStudio.Implementation"]
    NuGet_Tools --> NuGet_VisualStudio_Implementation
    NuGet_VisualStudio_Interop["NuGet.VisualStudio.Interop"]
    NuGet_Tools --> NuGet_VisualStudio_Interop
    NuGet_Tools_Test["NuGet.Tools.Test"]
    NuGet_Tools_Test -.-> NuGet_Tools
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_Tools
```

## Project References
- NuGet.Console
- NuGet.PackageManagement.PowerShellCmdlets
- NuGet.VisualStudio.Implementation
- NuGet.VisualStudio.Interop

## Consumed By
- NuGet.Tools.Test
- NuGet.VisualStudio.Client

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.VisualStudio.Sdk |  |
| Microsoft.VSSDK.BuildTools |  |


---

*[Back to Index](../index.md)*
