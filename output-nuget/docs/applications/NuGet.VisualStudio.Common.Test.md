# NuGet.VisualStudio.Common.Test

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/NuGet.Clients.Tests/NuGet.VisualStudio.Common.Test/NuGet.VisualStudio.Common.Test.csproj` |
| Project References | 2 |
| NuGet Dependencies | 2 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_VisualStudio_Common_Test["<strong>NuGet.VisualStudio.Common.Test</strong>"]
    NuGet_PackageManagement_Test["NuGet.PackageManagement.Test"]
    NuGet_VisualStudio_Common_Test --> NuGet_PackageManagement_Test
    VisualStudio_Test_Utility["VisualStudio.Test.Utility"]
    NuGet_VisualStudio_Common_Test --> VisualStudio_Test_Utility
```

## Project References
- NuGet.PackageManagement.Test
- VisualStudio.Test.Utility

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.VisualStudio.Sdk.TestFramework.Xunit |  |
| Microsoft.Build.Framework |  |


---

*[Back to Index](../index.md)*
