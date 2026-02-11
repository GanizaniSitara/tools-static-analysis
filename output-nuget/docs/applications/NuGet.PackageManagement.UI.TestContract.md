# NuGet.PackageManagement.UI.TestContract

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/NuGet.Tests.Apex/NuGet.PackageManagement.UI.TestContract/NuGet.PackageManagement.UI.TestContract.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_PackageManagement_UI_TestContract["<strong>NuGet.PackageManagement.UI.TestContract</strong>"]
    NuGet_PackageManagement_UI["NuGet.PackageManagement.UI"]
    NuGet_PackageManagement_UI_TestContract --> NuGet_PackageManagement_UI
    NuGet_Tests_Apex_Daily["NuGet.Tests.Apex.Daily"]
    NuGet_Tests_Apex_Daily -.-> NuGet_PackageManagement_UI_TestContract
    NuGet_Tests_Apex["NuGet.Tests.Apex"]
    NuGet_Tests_Apex -.-> NuGet_PackageManagement_UI_TestContract
```

## Project References
- NuGet.PackageManagement.UI

## Consumed By
- NuGet.Tests.Apex.Daily
- NuGet.Tests.Apex


---

*[Back to Index](../index.md)*
