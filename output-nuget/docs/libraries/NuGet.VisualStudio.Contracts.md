# NuGet.VisualStudio.Contracts

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Clients/NuGet.VisualStudio.Contracts/NuGet.VisualStudio.Contracts.csproj` |
| Project References | 0 |
| NuGet Dependencies | 2 |
| Consumers | 4 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_VisualStudio_Contracts["<strong>NuGet.VisualStudio.Contracts</strong>"]
    NuGet_Tests_Apex_Daily["NuGet.Tests.Apex.Daily"]
    NuGet_Tests_Apex_Daily -.-> NuGet_VisualStudio_Contracts
    NuGet_Tests_Apex["NuGet.Tests.Apex"]
    NuGet_Tests_Apex -.-> NuGet_VisualStudio_Contracts
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_VisualStudio_Contracts
    NuGet_VisualStudio_Implementation["NuGet.VisualStudio.Implementation"]
    NuGet_VisualStudio_Implementation -.-> NuGet_VisualStudio_Contracts
```

## Consumed By
- NuGet.Tests.Apex.Daily
- NuGet.Tests.Apex
- NuGet.VisualStudio.Client
- NuGet.VisualStudio.Implementation

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.ServiceHub.Framework |  |
| Newtonsoft.Json |  |


---

*[Back to Index](../index.md)*
