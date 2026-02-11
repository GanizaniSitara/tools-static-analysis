# Microsoft.Build.NuGetSdkResolver

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Core/Microsoft.Build.NuGetSdkResolver/Microsoft.Build.NuGetSdkResolver.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    Microsoft_Build_NuGetSdkResolver["<strong>Microsoft.Build.NuGetSdkResolver</strong>"]
    NuGet_Commands["NuGet.Commands"]
    Microsoft_Build_NuGetSdkResolver --> NuGet_Commands
    Dotnet_Integration_Test["Dotnet.Integration.Test"]
    Dotnet_Integration_Test -.-> Microsoft_Build_NuGetSdkResolver
    Msbuild_Integration_Test["Msbuild.Integration.Test"]
    Msbuild_Integration_Test -.-> Microsoft_Build_NuGetSdkResolver
    NuGet_XPlat_FuncTest["NuGet.XPlat.FuncTest"]
    NuGet_XPlat_FuncTest -.-> Microsoft_Build_NuGetSdkResolver
    Microsoft_Build_NuGetSdkResolver_Test["Microsoft.Build.NuGetSdkResolver.Test"]
    Microsoft_Build_NuGetSdkResolver_Test -.-> Microsoft_Build_NuGetSdkResolver
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> Microsoft_Build_NuGetSdkResolver
```

## Project References
- NuGet.Commands

## Consumed By
- Dotnet.Integration.Test
- Msbuild.Integration.Test
- NuGet.XPlat.FuncTest
- Microsoft.Build.NuGetSdkResolver.Test
- NuGet.VisualStudio.Client

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.Build.Framework |  |


---

*[Back to Index](../index.md)*
