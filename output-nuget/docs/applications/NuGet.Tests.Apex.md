# NuGet.Tests.Apex

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/NuGet.Tests.Apex/NuGet.Tests.Apex/NuGet.Tests.Apex.csproj` |
| Project References | 6 |
| NuGet Dependencies | 4 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Tests_Apex["<strong>NuGet.Tests.Apex</strong>"]
    NuGet_VisualStudio["NuGet.VisualStudio"]
    NuGet_Tests_Apex --> NuGet_VisualStudio
    NuGet_VisualStudio_Contracts["NuGet.VisualStudio.Contracts"]
    NuGet_Tests_Apex --> NuGet_VisualStudio_Contracts
    Test_Utility["Test.Utility"]
    NuGet_Tests_Apex --> Test_Utility
    NuGet_Console_TestContract["NuGet.Console.TestContract"]
    NuGet_Tests_Apex --> NuGet_Console_TestContract
    NuGet_PackageManagement_UI_TestContract["NuGet.PackageManagement.UI.TestContract"]
    NuGet_Tests_Apex --> NuGet_PackageManagement_UI_TestContract
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_Tests_Apex --> NuGet_VisualStudio_Client
    NuGet_Tests_Apex_Daily["NuGet.Tests.Apex.Daily"]
    NuGet_Tests_Apex_Daily -.-> NuGet_Tests_Apex
```

## Project References
- NuGet.VisualStudio
- NuGet.VisualStudio.Contracts
- Test.Utility
- NuGet.Console.TestContract
- NuGet.PackageManagement.UI.TestContract
- NuGet.VisualStudio.Client

## Consumed By
- NuGet.Tests.Apex.Daily

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.Test.Apex.VisualStudio |  |
| Microsoft.VisualStudio.Sdk |  |
| MSTest.TestAdapter |  |
| MSTest.TestFramework |  |


---

*[Back to Index](../index.md)*
