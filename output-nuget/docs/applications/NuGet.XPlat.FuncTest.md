# NuGet.XPlat.FuncTest

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/NuGet.XPlat.FuncTest.csproj` |
| Project References | 5 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_XPlat_FuncTest["<strong>NuGet.XPlat.FuncTest</strong>"]
    Test_Utility["Test.Utility"]
    NuGet_XPlat_FuncTest --> Test_Utility
    NuGet_CommandLine_XPlat["NuGet.CommandLine.XPlat"]
    NuGet_XPlat_FuncTest --> NuGet_CommandLine_XPlat
    Microsoft_Build_NuGetSdkResolver["Microsoft.Build.NuGetSdkResolver"]
    NuGet_XPlat_FuncTest --> Microsoft_Build_NuGetSdkResolver
    NuGet_CommandLine_Xplat_Tests["NuGet.CommandLine.Xplat.Tests"]
    NuGet_XPlat_FuncTest --> NuGet_CommandLine_Xplat_Tests
    NuGet_Configuration_Test["NuGet.Configuration.Test"]
    NuGet_XPlat_FuncTest --> NuGet_Configuration_Test
    Dotnet_Integration_Test["Dotnet.Integration.Test"]
    Dotnet_Integration_Test -.-> NuGet_XPlat_FuncTest
```

## Project References
- Test.Utility
- NuGet.CommandLine.XPlat
- Microsoft.Build.NuGetSdkResolver
- NuGet.CommandLine.Xplat.Tests
- NuGet.Configuration.Test

## Consumed By
- Dotnet.Integration.Test

## External NuGet Packages
| Package | Version |
|---------|---------||
| Spectre.Console.Testing |  |


---

*[Back to Index](../index.md)*
