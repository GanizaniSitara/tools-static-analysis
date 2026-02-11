# NuGet.MSSigning.Extensions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Clients/NuGet.MSSigning.Extensions/NuGet.MSSigning.Extensions.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_MSSigning_Extensions["<strong>NuGet.MSSigning.Extensions</strong>"]
    NuGet_CommandLine["NuGet.CommandLine"]
    NuGet_MSSigning_Extensions --> NuGet_CommandLine
    NuGet_MSSigning_Extensions_FuncTest["NuGet.MSSigning.Extensions.FuncTest"]
    NuGet_MSSigning_Extensions_FuncTest -.-> NuGet_MSSigning_Extensions
    NuGet_MSSigning_Extensions_Test["NuGet.MSSigning.Extensions.Test"]
    NuGet_MSSigning_Extensions_Test -.-> NuGet_MSSigning_Extensions
```

## Project References
- NuGet.CommandLine

## Consumed By
- NuGet.MSSigning.Extensions.FuncTest
- NuGet.MSSigning.Extensions.Test

## External NuGet Packages
| Package | Version |
|---------|---------||
| ILRepack |  |


---

*[Back to Index](../index.md)*
