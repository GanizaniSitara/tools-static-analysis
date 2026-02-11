# NuGet.PackageManagement.VisualStudio.Test

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/NuGet.Clients.Tests/NuGet.PackageManagement.VisualStudio.Test/NuGet.PackageManagement.VisualStudio.Test.csproj` |
| Project References | 5 |
| NuGet Dependencies | 1 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_PackageManagement_VisualStudio_Test["<strong>NuGet.PackageManagement.VisualStudio.Test</strong>"]
    NuGet_PackageManagement_UI["NuGet.PackageManagement.UI"]
    NuGet_PackageManagement_VisualStudio_Test --> NuGet_PackageManagement_UI
    NuGet_PackageManagement_VisualStudio["NuGet.PackageManagement.VisualStudio"]
    NuGet_PackageManagement_VisualStudio_Test --> NuGet_PackageManagement_VisualStudio
    NuGet_VisualStudio_Common["NuGet.VisualStudio.Common"]
    NuGet_PackageManagement_VisualStudio_Test --> NuGet_VisualStudio_Common
    NuGet_VisualStudio["NuGet.VisualStudio"]
    NuGet_PackageManagement_VisualStudio_Test --> NuGet_VisualStudio
    VisualStudio_Test_Utility["VisualStudio.Test.Utility"]
    NuGet_PackageManagement_VisualStudio_Test --> VisualStudio_Test_Utility
```

## Project References
- NuGet.PackageManagement.UI
- NuGet.PackageManagement.VisualStudio
- NuGet.VisualStudio.Common
- NuGet.VisualStudio
- VisualStudio.Test.Utility

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.VisualStudio.Sdk.TestFramework.Xunit |  |


---

*[Back to Index](../index.md)*
