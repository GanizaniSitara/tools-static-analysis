# Msbuild.Integration.Test

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/NuGet.Core.FuncTests/Msbuild.Integration.Test/Msbuild.Integration.Test.csproj` |
| Project References | 5 |
| NuGet Dependencies | 0 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Msbuild_Integration_Test["<strong>Msbuild.Integration.Test</strong>"]
    Microsoft_Build_NuGetSdkResolver["Microsoft.Build.NuGetSdkResolver"]
    Msbuild_Integration_Test --> Microsoft_Build_NuGetSdkResolver
    NuGet_Build_Tasks_Console["NuGet.Build.Tasks.Console"]
    Msbuild_Integration_Test --> NuGet_Build_Tasks_Console
    NuGet_Build_Tasks_Pack["NuGet.Build.Tasks.Pack"]
    Msbuild_Integration_Test --> NuGet_Build_Tasks_Pack
    NuGet_Build_Tasks["NuGet.Build.Tasks"]
    Msbuild_Integration_Test --> NuGet_Build_Tasks
    Test_Utility["Test.Utility"]
    Msbuild_Integration_Test --> Test_Utility
```

## Project References
- Microsoft.Build.NuGetSdkResolver
- NuGet.Build.Tasks.Console
- NuGet.Build.Tasks.Pack
- NuGet.Build.Tasks
- Test.Utility


---

*[Back to Index](../index.md)*
