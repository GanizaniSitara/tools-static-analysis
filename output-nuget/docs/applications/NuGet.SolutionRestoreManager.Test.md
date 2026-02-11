# NuGet.SolutionRestoreManager.Test

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/NuGet.Clients.Tests/NuGet.SolutionRestoreManager.Test/NuGet.SolutionRestoreManager.Test.csproj` |
| Project References | 3 |
| NuGet Dependencies | 2 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_SolutionRestoreManager_Test["<strong>NuGet.SolutionRestoreManager.Test</strong>"]
    NuGet_PackageManagement_VisualStudio["NuGet.PackageManagement.VisualStudio"]
    NuGet_SolutionRestoreManager_Test --> NuGet_PackageManagement_VisualStudio
    NuGet_SolutionRestoreManager["NuGet.SolutionRestoreManager"]
    NuGet_SolutionRestoreManager_Test --> NuGet_SolutionRestoreManager
    VisualStudio_Test_Utility["VisualStudio.Test.Utility"]
    NuGet_SolutionRestoreManager_Test --> VisualStudio_Test_Utility
```

## Project References
- NuGet.PackageManagement.VisualStudio
- NuGet.SolutionRestoreManager
- VisualStudio.Test.Utility

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.VisualStudio.Sdk.TestFramework.Xunit |  |
| Microsoft.Build.Framework |  |


---

*[Back to Index](../index.md)*
