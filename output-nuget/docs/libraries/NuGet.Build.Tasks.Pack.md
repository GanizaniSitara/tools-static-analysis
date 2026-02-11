# NuGet.Build.Tasks.Pack

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Core/NuGet.Build.Tasks.Pack/NuGet.Build.Tasks.Pack.csproj` |
| Project References | 1 |
| NuGet Dependencies | 3 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Build_Tasks_Pack["<strong>NuGet.Build.Tasks.Pack</strong>"]
    NuGet_Commands["NuGet.Commands"]
    NuGet_Build_Tasks_Pack --> NuGet_Commands
    Dotnet_Integration_Test["Dotnet.Integration.Test"]
    Dotnet_Integration_Test -.-> NuGet_Build_Tasks_Pack
    Msbuild_Integration_Test["Msbuild.Integration.Test"]
    Msbuild_Integration_Test -.-> NuGet_Build_Tasks_Pack
    NuGet_Signing_CrossFramework_Test["NuGet.Signing.CrossFramework.Test"]
    NuGet_Signing_CrossFramework_Test -.-> NuGet_Build_Tasks_Pack
    NuGet_Build_Tasks_Pack_Test["NuGet.Build.Tasks.Pack.Test"]
    NuGet_Build_Tasks_Pack_Test -.-> NuGet_Build_Tasks_Pack
    NuGet_Build_Tasks["NuGet.Build.Tasks"]
    NuGet_Build_Tasks -.-> NuGet_Build_Tasks_Pack
```

## Project References
- NuGet.Commands

## Consumed By
- Dotnet.Integration.Test
- Msbuild.Integration.Test
- NuGet.Signing.CrossFramework.Test
- NuGet.Build.Tasks.Pack.Test
- NuGet.Build.Tasks

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.Build.Framework |  |
| Microsoft.Build.Tasks.Core |  |
| Microsoft.Build.Utilities.Core |  |


---

*[Back to Index](../index.md)*
