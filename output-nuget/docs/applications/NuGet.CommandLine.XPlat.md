# NuGet.CommandLine.XPlat

## Overview

| Property | Value |
|----------|-------|
| Category | Application |
| Repository | NuGet.Client |
| Path | `src/NuGet.Core/NuGet.CommandLine.XPlat/NuGet.CommandLine.XPlat.csproj` |
| Project References | 1 |
| NuGet Dependencies | 5 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_CommandLine_XPlat["<strong>NuGet.CommandLine.XPlat</strong>"]
    NuGet_Commands["NuGet.Commands"]
    NuGet_CommandLine_XPlat --> NuGet_Commands
    NuGet_XPlat_FuncTest["NuGet.XPlat.FuncTest"]
    NuGet_XPlat_FuncTest -.-> NuGet_CommandLine_XPlat
    NuGet_Signing_CrossFramework_Test["NuGet.Signing.CrossFramework.Test"]
    NuGet_Signing_CrossFramework_Test -.-> NuGet_CommandLine_XPlat
    NuGet_CommandLine_Xplat_Tests["NuGet.CommandLine.Xplat.Tests"]
    NuGet_CommandLine_Xplat_Tests -.-> NuGet_CommandLine_XPlat
```

## Project References
- NuGet.Commands

## Consumed By
- NuGet.XPlat.FuncTest
- NuGet.Signing.CrossFramework.Test
- NuGet.CommandLine.Xplat.Tests

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.Extensions.CommandLineUtils.Sources |  |
| Microsoft.Build |  |
| Spectre.Console |  |
| System.CommandLine |  |
| Microsoft.Build.Locator |  |


---

*[Back to Index](../index.md)*
