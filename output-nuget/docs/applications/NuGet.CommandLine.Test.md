# NuGet.CommandLine.Test

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/NuGet.Clients.Tests/NuGet.CommandLine.Test/NuGet.CommandLine.Test.csproj` |
| Project References | 5 |
| NuGet Dependencies | 2 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_CommandLine_Test["<strong>NuGet.CommandLine.Test</strong>"]
    NuGet_CommandLine["NuGet.CommandLine"]
    NuGet_CommandLine_Test --> NuGet_CommandLine
    NuGet_Configuration_Test["NuGet.Configuration.Test"]
    NuGet_CommandLine_Test --> NuGet_Configuration_Test
    SampleCommandLineExtensions["SampleCommandLineExtensions"]
    NuGet_CommandLine_Test --> SampleCommandLineExtensions
    TestableCredentialProvider["TestableCredentialProvider"]
    NuGet_CommandLine_Test --> TestableCredentialProvider
    Test_Utility["Test.Utility"]
    NuGet_CommandLine_Test --> Test_Utility
    NuGet_MSSigning_Extensions_FuncTest["NuGet.MSSigning.Extensions.FuncTest"]
    NuGet_MSSigning_Extensions_FuncTest -.-> NuGet_CommandLine_Test
    NuGet_CommandLine_FuncTest["NuGet.CommandLine.FuncTest"]
    NuGet_CommandLine_FuncTest -.-> NuGet_CommandLine_Test
```

## Project References
- NuGet.CommandLine
- NuGet.Configuration.Test
- SampleCommandLineExtensions
- TestableCredentialProvider
- Test.Utility

## Consumed By
- NuGet.MSSigning.Extensions.FuncTest
- NuGet.CommandLine.FuncTest

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.Build.Framework |  |
| Microsoft.TestPlatform.Portable |  |


---

*[Back to Index](../index.md)*
