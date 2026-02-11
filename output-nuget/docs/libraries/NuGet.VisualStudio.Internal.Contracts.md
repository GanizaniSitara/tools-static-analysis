# NuGet.VisualStudio.Internal.Contracts

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Clients/NuGet.VisualStudio.Internal.Contracts/NuGet.VisualStudio.Internal.Contracts.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_VisualStudio_Internal_Contracts["<strong>NuGet.VisualStudio.Internal.Contracts</strong>"]
    NuGet_PackageManagement["NuGet.PackageManagement"]
    NuGet_VisualStudio_Internal_Contracts --> NuGet_PackageManagement
    NuGet_VisualStudio_Internal_Contracts_Test["NuGet.VisualStudio.Internal.Contracts.Test"]
    NuGet_VisualStudio_Internal_Contracts_Test -.-> NuGet_VisualStudio_Internal_Contracts
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_VisualStudio_Internal_Contracts
    NuGet_VisualStudio_Common["NuGet.VisualStudio.Common"]
    NuGet_VisualStudio_Common -.-> NuGet_VisualStudio_Internal_Contracts
```

## Project References
- NuGet.PackageManagement

## Consumed By
- NuGet.VisualStudio.Internal.Contracts.Test
- NuGet.VisualStudio.Client
- NuGet.VisualStudio.Common

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.VisualStudio.Sdk |  |


---

*[Back to Index](../index.md)*
