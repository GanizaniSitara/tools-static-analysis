# NuGet.Configuration

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Core/NuGet.Configuration/NuGet.Configuration.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 4 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Configuration["<strong>NuGet.Configuration</strong>"]
    NuGet_Common["NuGet.Common"]
    NuGet_Configuration --> NuGet_Common
    NuGet_Configuration_Test["NuGet.Configuration.Test"]
    NuGet_Configuration_Test -.-> NuGet_Configuration
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_Configuration
    NuGet_DependencyResolver_Core["NuGet.DependencyResolver.Core"]
    NuGet_DependencyResolver_Core -.-> NuGet_Configuration
    NuGet_Packaging["NuGet.Packaging"]
    NuGet_Packaging -.-> NuGet_Configuration
```

## Project References
- NuGet.Common

## Consumed By
- NuGet.Configuration.Test
- NuGet.VisualStudio.Client
- NuGet.DependencyResolver.Core
- NuGet.Packaging

## External NuGet Packages
| Package | Version |
|---------|---------||
| System.Security.Cryptography.ProtectedData |  |


---

*[Back to Index](../index.md)*
