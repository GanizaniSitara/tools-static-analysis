# NuGet.PackageManagement.Test

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/NuGet.Core.Tests/NuGet.PackageManagement.Test/NuGet.PackageManagement.Test.csproj` |
| Project References | 5 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_PackageManagement_Test["<strong>NuGet.PackageManagement.Test</strong>"]
    Test_Utility["Test.Utility"]
    NuGet_PackageManagement_Test --> Test_Utility
    NuGet_PackageManagement["NuGet.PackageManagement"]
    NuGet_PackageManagement_Test --> NuGet_PackageManagement
    VisualStudio_Test_Utility["VisualStudio.Test.Utility"]
    NuGet_PackageManagement_Test --> VisualStudio_Test_Utility
    NuGet_VisualStudio_Common["NuGet.VisualStudio.Common"]
    NuGet_PackageManagement_Test --> NuGet_VisualStudio_Common
    NuGet_PackageManagement_VisualStudio["NuGet.PackageManagement.VisualStudio"]
    NuGet_PackageManagement_Test --> NuGet_PackageManagement_VisualStudio
    NuGet_VisualStudio_Common_Test["NuGet.VisualStudio.Common.Test"]
    NuGet_VisualStudio_Common_Test -.-> NuGet_PackageManagement_Test
```

## Project References
- Test.Utility
- NuGet.PackageManagement
- VisualStudio.Test.Utility
- NuGet.VisualStudio.Common
- NuGet.PackageManagement.VisualStudio

## Consumed By
- NuGet.VisualStudio.Common.Test


---

*[Back to Index](../index.md)*
