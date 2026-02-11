# NuGet.Packaging.FuncTest

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/NuGet.Core.FuncTests/NuGet.Packaging.FuncTest/NuGet.Packaging.FuncTest.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Packaging_FuncTest["<strong>NuGet.Packaging.FuncTest</strong>"]
    NuGet_Packaging["NuGet.Packaging"]
    NuGet_Packaging_FuncTest --> NuGet_Packaging
    NuGet_Configuration_Test["NuGet.Configuration.Test"]
    NuGet_Packaging_FuncTest --> NuGet_Configuration_Test
    Test_Utility["Test.Utility"]
    NuGet_Packaging_FuncTest --> Test_Utility
    NuGet_Signing_CrossFramework_Test["NuGet.Signing.CrossFramework.Test"]
    NuGet_Signing_CrossFramework_Test -.-> NuGet_Packaging_FuncTest
```

## Project References
- NuGet.Packaging
- NuGet.Configuration.Test
- Test.Utility

## Consumed By
- NuGet.Signing.CrossFramework.Test


---

*[Back to Index](../index.md)*
