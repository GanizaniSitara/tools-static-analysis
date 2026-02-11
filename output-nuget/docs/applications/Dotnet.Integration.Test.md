# Dotnet.Integration.Test

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/Dotnet.Integration.Test.csproj` |
| Project References | 5 |
| NuGet Dependencies | 0 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Dotnet_Integration_Test["<strong>Dotnet.Integration.Test</strong>"]
    NuGet_XPlat_FuncTest["NuGet.XPlat.FuncTest"]
    Dotnet_Integration_Test --> NuGet_XPlat_FuncTest
    Test_Utility["Test.Utility"]
    Dotnet_Integration_Test --> Test_Utility
    NuGet_Build_Tasks_Pack["NuGet.Build.Tasks.Pack"]
    Dotnet_Integration_Test --> NuGet_Build_Tasks_Pack
    NuGet_Build_Tasks_Console["NuGet.Build.Tasks.Console"]
    Dotnet_Integration_Test --> NuGet_Build_Tasks_Console
    Microsoft_Build_NuGetSdkResolver["Microsoft.Build.NuGetSdkResolver"]
    Dotnet_Integration_Test --> Microsoft_Build_NuGetSdkResolver
```

## Project References
- NuGet.XPlat.FuncTest
- Test.Utility
- NuGet.Build.Tasks.Pack
- NuGet.Build.Tasks.Console
- Microsoft.Build.NuGetSdkResolver


---

*[Back to Index](../index.md)*
