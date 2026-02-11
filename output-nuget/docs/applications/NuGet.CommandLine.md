# NuGet.CommandLine

## Overview

| Property | Value |
|----------|-------|
| Category | Application |
| Repository | NuGet.Client |
| Path | `src/NuGet.Clients/NuGet.CommandLine/NuGet.CommandLine.csproj` |
| Project References | 2 |
| NuGet Dependencies | 4 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_CommandLine["<strong>NuGet.CommandLine</strong>"]
    NuGet_PackageManagement["NuGet.PackageManagement"]
    NuGet_CommandLine --> NuGet_PackageManagement
    NuGet_Build_Tasks["NuGet.Build.Tasks"]
    NuGet_CommandLine --> NuGet_Build_Tasks
    SampleCommandLineExtensions["SampleCommandLineExtensions"]
    SampleCommandLineExtensions -.-> NuGet_CommandLine
    NuGet_CommandLine_Test["NuGet.CommandLine.Test"]
    NuGet_CommandLine_Test -.-> NuGet_CommandLine
    NuGet_MSSigning_Extensions["NuGet.MSSigning.Extensions"]
    NuGet_MSSigning_Extensions -.-> NuGet_CommandLine
```

## Project References
- NuGet.PackageManagement
- NuGet.Build.Tasks

## Consumed By
- SampleCommandLineExtensions
- NuGet.CommandLine.Test
- NuGet.MSSigning.Extensions

## External NuGet Packages
| Package | Version |
|---------|---------||
| NuGet.Core |  |
| Microsoft.VisualStudio.Setup.Configuration.Interop |  |
| ILRepack |  |
| System.Memory |  |


---

*[Back to Index](../index.md)*
