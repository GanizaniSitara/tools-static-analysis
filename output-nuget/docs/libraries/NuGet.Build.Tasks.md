# NuGet.Build.Tasks

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Core/NuGet.Build.Tasks/NuGet.Build.Tasks.csproj` |
| Project References | 3 |
| NuGet Dependencies | 3 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Build_Tasks["<strong>NuGet.Build.Tasks</strong>"]
    NuGet_Commands["NuGet.Commands"]
    NuGet_Build_Tasks --> NuGet_Commands
    NuGet_Build_Tasks_Pack["NuGet.Build.Tasks.Pack"]
    NuGet_Build_Tasks --> NuGet_Build_Tasks_Pack
    NuGet_PackageManagement["NuGet.PackageManagement"]
    NuGet_Build_Tasks --> NuGet_PackageManagement
    Msbuild_Integration_Test["Msbuild.Integration.Test"]
    Msbuild_Integration_Test -.-> NuGet_Build_Tasks
    NuGet_Build_Tasks_Test["NuGet.Build.Tasks.Test"]
    NuGet_Build_Tasks_Test -.-> NuGet_Build_Tasks
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_Build_Tasks
    NuGet_CommandLine["NuGet.CommandLine"]
    NuGet_CommandLine -.-> NuGet_Build_Tasks
    NuGet_Build_Tasks_Console["NuGet.Build.Tasks.Console"]
    NuGet_Build_Tasks_Console -.-> NuGet_Build_Tasks
```

## Project References
- NuGet.Commands
- NuGet.Build.Tasks.Pack
- NuGet.PackageManagement

## Consumed By
- Msbuild.Integration.Test
- NuGet.Build.Tasks.Test
- NuGet.VisualStudio.Client
- NuGet.CommandLine
- NuGet.Build.Tasks.Console

## External NuGet Packages
| Package | Version |
|---------|---------||
| System.Threading.Tasks.Dataflow |  |
| Microsoft.Build.Tasks.Core |  |
| Microsoft.Build.Utilities.Core |  |


---

*[Back to Index](../index.md)*
