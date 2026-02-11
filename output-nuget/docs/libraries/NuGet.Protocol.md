# NuGet.Protocol

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Core/NuGet.Protocol/NuGet.Protocol.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 8 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Protocol["<strong>NuGet.Protocol</strong>"]
    NuGet_Packaging["NuGet.Packaging"]
    NuGet_Protocol --> NuGet_Packaging
    NuGet_Protocol_Tests["NuGet.Protocol.Tests"]
    NuGet_Protocol_Tests -.-> NuGet_Protocol
    TestablePlugin["TestablePlugin"]
    TestablePlugin -.-> NuGet_Protocol
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_Protocol
    NuGet_Indexing["NuGet.Indexing"]
    NuGet_Indexing -.-> NuGet_Protocol
    NuGet_DependencyResolver_Core["NuGet.DependencyResolver.Core"]
    NuGet_DependencyResolver_Core -.-> NuGet_Protocol
    NuGet_Credentials["NuGet.Credentials"]
    NuGet_Credentials -.-> NuGet_Protocol
    NuGet_Resolver["NuGet.Resolver"]
    NuGet_Resolver -.-> NuGet_Protocol
    ensure_nupkg_dependencies_on_source["ensure-nupkg-dependencies-on-source"]
    ensure_nupkg_dependencies_on_source -.-> NuGet_Protocol
```

## Project References
- NuGet.Packaging

## Consumed By
- NuGet.Protocol.Tests
- TestablePlugin
- NuGet.VisualStudio.Client
- NuGet.Indexing
- NuGet.DependencyResolver.Core
- NuGet.Credentials
- NuGet.Resolver
- ensure-nupkg-dependencies-on-source

## External NuGet Packages
| Package | Version |
|---------|---------||
| System.Text.Json |  |


---

*[Back to Index](../index.md)*
