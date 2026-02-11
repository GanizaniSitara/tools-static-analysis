# NuGet.Tests.Apex.Daily

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/NuGet.Tests.Apex/NuGet.Tests.Apex.Daily/NuGet.Tests.Apex.Daily.csproj` |
| Project References | 7 |
| NuGet Dependencies | 4 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Tests_Apex_Daily["<strong>NuGet.Tests.Apex.Daily</strong>"]
    NuGet_VisualStudio["NuGet.VisualStudio"]
    NuGet_Tests_Apex_Daily --> NuGet_VisualStudio
    NuGet_VisualStudio_Contracts["NuGet.VisualStudio.Contracts"]
    NuGet_Tests_Apex_Daily --> NuGet_VisualStudio_Contracts
    Test_Utility["Test.Utility"]
    NuGet_Tests_Apex_Daily --> Test_Utility
    NuGet_Console_TestContract["NuGet.Console.TestContract"]
    NuGet_Tests_Apex_Daily --> NuGet_Console_TestContract
    NuGet_PackageManagement_UI_TestContract["NuGet.PackageManagement.UI.TestContract"]
    NuGet_Tests_Apex_Daily --> NuGet_PackageManagement_UI_TestContract
    NuGet_Tests_Apex["NuGet.Tests.Apex"]
    NuGet_Tests_Apex_Daily --> NuGet_Tests_Apex
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_Tests_Apex_Daily --> NuGet_VisualStudio_Client
```

## Project References
- NuGet.VisualStudio
- NuGet.VisualStudio.Contracts
- Test.Utility
- NuGet.Console.TestContract
- NuGet.PackageManagement.UI.TestContract
- NuGet.Tests.Apex
- NuGet.VisualStudio.Client

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.Test.Apex.VisualStudio |  |
| Microsoft.VisualStudio.Sdk |  |
| MSTest.TestAdapter |  |
| MSTest.TestFramework |  |


---

*[Back to Index](../index.md)*
