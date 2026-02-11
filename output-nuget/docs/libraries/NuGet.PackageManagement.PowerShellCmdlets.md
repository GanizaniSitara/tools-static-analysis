# NuGet.PackageManagement.PowerShellCmdlets

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Clients/NuGet.PackageManagement.PowerShellCmdlets/NuGet.PackageManagement.PowerShellCmdlets.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_PackageManagement_PowerShellCmdlets["<strong>NuGet.PackageManagement.PowerShellCmdlets</strong>"]
    NuGet_Console["NuGet.Console"]
    NuGet_PackageManagement_PowerShellCmdlets --> NuGet_Console
    NuGetConsole_Host_PowerShell_Test["NuGetConsole.Host.PowerShell.Test"]
    NuGetConsole_Host_PowerShell_Test -.-> NuGet_PackageManagement_PowerShellCmdlets
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_PackageManagement_PowerShellCmdlets
    NuGet_Tools["NuGet.Tools"]
    NuGet_Tools -.-> NuGet_PackageManagement_PowerShellCmdlets
```

## Project References
- NuGet.Console

## Consumed By
- NuGetConsole.Host.PowerShell.Test
- NuGet.VisualStudio.Client
- NuGet.Tools

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.VisualStudio.Sdk |  |


---

*[Back to Index](../index.md)*
