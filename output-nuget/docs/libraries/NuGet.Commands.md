# NuGet.Commands

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Core/NuGet.Commands/NuGet.Commands.csproj` |
| Project References | 2 |
| NuGet Dependencies | 2 |
| Consumers | 7 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Commands["<strong>NuGet.Commands</strong>"]
    NuGet_Credentials["NuGet.Credentials"]
    NuGet_Commands --> NuGet_Credentials
    NuGet_ProjectModel["NuGet.ProjectModel"]
    NuGet_Commands --> NuGet_ProjectModel
    NuGet_Commands_Test["NuGet.Commands.Test"]
    NuGet_Commands_Test -.-> NuGet_Commands
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_Commands
    NuGet_PackageManagement["NuGet.PackageManagement"]
    NuGet_PackageManagement -.-> NuGet_Commands
    NuGet_CommandLine_XPlat["NuGet.CommandLine.XPlat"]
    NuGet_CommandLine_XPlat -.-> NuGet_Commands
    Microsoft_Build_NuGetSdkResolver["Microsoft.Build.NuGetSdkResolver"]
    Microsoft_Build_NuGetSdkResolver -.-> NuGet_Commands
    NuGet_Build_Tasks_Pack["NuGet.Build.Tasks.Pack"]
    NuGet_Build_Tasks_Pack -.-> NuGet_Commands
    NuGet_Build_Tasks["NuGet.Build.Tasks"]
    NuGet_Build_Tasks -.-> NuGet_Commands
```

## Project References
- NuGet.Credentials
- NuGet.ProjectModel

## Consumed By
- NuGet.Commands.Test
- NuGet.VisualStudio.Client
- NuGet.PackageManagement
- NuGet.CommandLine.XPlat
- Microsoft.Build.NuGetSdkResolver
- NuGet.Build.Tasks.Pack
- NuGet.Build.Tasks

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.Extensions.FileSystemGlobbing |  |
| Microsoft.Extensions.FileProviders.Abstractions |  |


---

*[Back to Index](../index.md)*
