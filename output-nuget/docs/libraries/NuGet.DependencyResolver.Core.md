# NuGet.DependencyResolver.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Core/NuGet.DependencyResolver.Core/NuGet.DependencyResolver.Core.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_DependencyResolver_Core["<strong>NuGet.DependencyResolver.Core</strong>"]
    NuGet_Configuration["NuGet.Configuration"]
    NuGet_DependencyResolver_Core --> NuGet_Configuration
    NuGet_LibraryModel["NuGet.LibraryModel"]
    NuGet_DependencyResolver_Core --> NuGet_LibraryModel
    NuGet_Protocol["NuGet.Protocol"]
    NuGet_DependencyResolver_Core --> NuGet_Protocol
    NuGet_DependencyResolver_Core_Tests["NuGet.DependencyResolver.Core.Tests"]
    NuGet_DependencyResolver_Core_Tests -.-> NuGet_DependencyResolver_Core
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_DependencyResolver_Core
    NuGet_ProjectModel["NuGet.ProjectModel"]
    NuGet_ProjectModel -.-> NuGet_DependencyResolver_Core
```

## Project References
- NuGet.Configuration
- NuGet.LibraryModel
- NuGet.Protocol

## Consumed By
- NuGet.DependencyResolver.Core.Tests
- NuGet.VisualStudio.Client
- NuGet.ProjectModel


---

*[Back to Index](../index.md)*
