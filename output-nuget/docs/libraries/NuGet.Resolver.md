# NuGet.Resolver

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Core/NuGet.Resolver/NuGet.Resolver.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Resolver["<strong>NuGet.Resolver</strong>"]
    NuGet_Protocol["NuGet.Protocol"]
    NuGet_Resolver --> NuGet_Protocol
    NuGet_Resolver_Test["NuGet.Resolver.Test"]
    NuGet_Resolver_Test -.-> NuGet_Resolver
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_Resolver
    NuGet_PackageManagement["NuGet.PackageManagement"]
    NuGet_PackageManagement -.-> NuGet_Resolver
```

## Project References
- NuGet.Protocol

## Consumed By
- NuGet.Resolver.Test
- NuGet.VisualStudio.Client
- NuGet.PackageManagement


---

*[Back to Index](../index.md)*
