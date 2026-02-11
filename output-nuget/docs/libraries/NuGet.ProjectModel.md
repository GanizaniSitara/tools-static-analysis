# NuGet.ProjectModel

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Core/NuGet.ProjectModel/NuGet.ProjectModel.csproj` |
| Project References | 1 |
| NuGet Dependencies | 2 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_ProjectModel["<strong>NuGet.ProjectModel</strong>"]
    NuGet_DependencyResolver_Core["NuGet.DependencyResolver.Core"]
    NuGet_ProjectModel --> NuGet_DependencyResolver_Core
    NuGet_ProjectModel_Test["NuGet.ProjectModel.Test"]
    NuGet_ProjectModel_Test -.-> NuGet_ProjectModel
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_ProjectModel
    NuGet_Commands["NuGet.Commands"]
    NuGet_Commands -.-> NuGet_ProjectModel
```

## Project References
- NuGet.DependencyResolver.Core

## Consumed By
- NuGet.ProjectModel.Test
- NuGet.VisualStudio.Client
- NuGet.Commands

## External NuGet Packages
| Package | Version |
|---------|---------||
| System.Collections.Immutable |  |
| System.Text.Json |  |


---

*[Back to Index](../index.md)*
