# NuGet.Build.Tasks.Console

## Overview

| Property | Value |
|----------|-------|
| Category | Tool |
| Repository | NuGet.Client |
| Path | `src/NuGet.Core/NuGet.Build.Tasks.Console/NuGet.Build.Tasks.Console.csproj` |
| Project References | 1 |
| NuGet Dependencies | 4 |
| Consumers | 6 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Build_Tasks_Console["<strong>NuGet.Build.Tasks.Console</strong>"]
    NuGet_Build_Tasks["NuGet.Build.Tasks"]
    NuGet_Build_Tasks_Console --> NuGet_Build_Tasks
    Dotnet_Integration_Test["Dotnet.Integration.Test"]
    Dotnet_Integration_Test -.-> NuGet_Build_Tasks_Console
    Msbuild_Integration_Test["Msbuild.Integration.Test"]
    Msbuild_Integration_Test -.-> NuGet_Build_Tasks_Console
    NuGet_Signing_CrossFramework_Test["NuGet.Signing.CrossFramework.Test"]
    NuGet_Signing_CrossFramework_Test -.-> NuGet_Build_Tasks_Console
    NuGet_Build_Tasks_Console_Test["NuGet.Build.Tasks.Console.Test"]
    NuGet_Build_Tasks_Console_Test -.-> NuGet_Build_Tasks_Console
    NuGet_Build_Tasks_Test["NuGet.Build.Tasks.Test"]
    NuGet_Build_Tasks_Test -.-> NuGet_Build_Tasks_Console
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_Build_Tasks_Console
```

## Project References
- NuGet.Build.Tasks

## Consumed By
- Dotnet.Integration.Test
- Msbuild.Integration.Test
- NuGet.Signing.CrossFramework.Test
- NuGet.Build.Tasks.Console.Test
- NuGet.Build.Tasks.Test
- NuGet.VisualStudio.Client

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.Build.Framework |  |
| Microsoft.Build |  |
| Microsoft.Build.Tasks.Core |  |
| Microsoft.Build.Utilities.Core |  |


---

*[Back to Index](../index.md)*
