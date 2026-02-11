# NuGet.Signing.CrossFramework.Test

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/NuGet.Core.FuncTests/NuGet.Signing.CrossFramework.Test/NuGet.Signing.CrossFramework.Test.csproj` |
| Project References | 7 |
| NuGet Dependencies | 0 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Signing_CrossFramework_Test["<strong>NuGet.Signing.CrossFramework.Test</strong>"]
    NuGet_Build_Tasks_Console["NuGet.Build.Tasks.Console"]
    NuGet_Signing_CrossFramework_Test --> NuGet_Build_Tasks_Console
    NuGet_Build_Tasks_Pack["NuGet.Build.Tasks.Pack"]
    NuGet_Signing_CrossFramework_Test --> NuGet_Build_Tasks_Pack
    NuGet_CommandLine_XPlat["NuGet.CommandLine.XPlat"]
    NuGet_Signing_CrossFramework_Test --> NuGet_CommandLine_XPlat
    NuGet_Packaging["NuGet.Packaging"]
    NuGet_Signing_CrossFramework_Test --> NuGet_Packaging
    NuGet_Packaging_FuncTest["NuGet.Packaging.FuncTest"]
    NuGet_Signing_CrossFramework_Test --> NuGet_Packaging_FuncTest
    NuGet_Configuration_Test["NuGet.Configuration.Test"]
    NuGet_Signing_CrossFramework_Test --> NuGet_Configuration_Test
    Test_Utility["Test.Utility"]
    NuGet_Signing_CrossFramework_Test --> Test_Utility
```

## Project References
- NuGet.Build.Tasks.Console
- NuGet.Build.Tasks.Pack
- NuGet.CommandLine.XPlat
- NuGet.Packaging
- NuGet.Packaging.FuncTest
- NuGet.Configuration.Test
- Test.Utility


---

*[Back to Index](../index.md)*
