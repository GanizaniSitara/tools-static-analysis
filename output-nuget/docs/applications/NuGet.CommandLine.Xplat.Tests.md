# NuGet.CommandLine.Xplat.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/NuGet.Core.Tests/NuGet.CommandLine.Xplat.Tests/NuGet.CommandLine.Xplat.Tests.csproj` |
| Project References | 2 |
| NuGet Dependencies | 5 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_CommandLine_Xplat_Tests["<strong>NuGet.CommandLine.Xplat.Tests</strong>"]
    Test_Utility["Test.Utility"]
    NuGet_CommandLine_Xplat_Tests --> Test_Utility
    NuGet_CommandLine_XPlat["NuGet.CommandLine.XPlat"]
    NuGet_CommandLine_Xplat_Tests --> NuGet_CommandLine_XPlat
    NuGet_XPlat_FuncTest["NuGet.XPlat.FuncTest"]
    NuGet_XPlat_FuncTest -.-> NuGet_CommandLine_Xplat_Tests
```

## Project References
- Test.Utility
- NuGet.CommandLine.XPlat

## Consumed By
- NuGet.XPlat.FuncTest

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.Build |  |
| Microsoft.Build.Framework |  |
| Microsoft.Build.Locator |  |
| Spectre.Console.Testing |  |
| System.CommandLine |  |


---

*[Back to Index](../index.md)*
