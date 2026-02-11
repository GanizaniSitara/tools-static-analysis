# NuGet.Console

## Overview

| Property | Value |
|----------|-------|
| Category | Tool |
| Repository | NuGet.Client |
| Path | `src/NuGet.Clients/NuGet.Console/NuGet.Console.csproj` |
| Project References | 1 |
| NuGet Dependencies | 2 |
| Consumers | 4 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Console["<strong>NuGet.Console</strong>"]
    NuGet_PackageManagement_UI["NuGet.PackageManagement.UI"]
    NuGet_Console --> NuGet_PackageManagement_UI
    NuGet_Console_TestContract["NuGet.Console.TestContract"]
    NuGet_Console_TestContract -.-> NuGet_Console
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_Console
    NuGet_Tools["NuGet.Tools"]
    NuGet_Tools -.-> NuGet_Console
    NuGet_PackageManagement_PowerShellCmdlets["NuGet.PackageManagement.PowerShellCmdlets"]
    NuGet_PackageManagement_PowerShellCmdlets -.-> NuGet_Console
```

## Project References
- NuGet.PackageManagement.UI

## Consumed By
- NuGet.Console.TestContract
- NuGet.VisualStudio.Client
- NuGet.Tools
- NuGet.PackageManagement.PowerShellCmdlets

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.VisualStudio.Sdk |  |
| Microsoft.PowerShell.3.ReferenceAssemblies |  |


---

*[Back to Index](../index.md)*
