# NuGet.Build.Tasks.Test

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/NuGet.Core.Tests/NuGet.Build.Tasks.Test/NuGet.Build.Tasks.Test.csproj` |
| Project References | 4 |
| NuGet Dependencies | 3 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Build_Tasks_Test["<strong>NuGet.Build.Tasks.Test</strong>"]
    Test_Utility["Test.Utility"]
    NuGet_Build_Tasks_Test --> Test_Utility
    NuGet_Build_Tasks["NuGet.Build.Tasks"]
    NuGet_Build_Tasks_Test --> NuGet_Build_Tasks
    NuGet_Build_Tasks_Console["NuGet.Build.Tasks.Console"]
    NuGet_Build_Tasks_Test --> NuGet_Build_Tasks_Console
    NuGet_Configuration_Test["NuGet.Configuration.Test"]
    NuGet_Build_Tasks_Test --> NuGet_Configuration_Test
```

## Project References
- Test.Utility
- NuGet.Build.Tasks
- NuGet.Build.Tasks.Console
- NuGet.Configuration.Test

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.Build.Framework |  |
| Microsoft.Build.Tasks.Core |  |
| Microsoft.Build.Utilities.Core |  |


---

*[Back to Index](../index.md)*
