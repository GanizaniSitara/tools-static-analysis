# NuGet.PackageManagement.UI

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Clients/NuGet.PackageManagement.UI/NuGet.PackageManagement.UI.csproj` |
| Project References | 1 |
| NuGet Dependencies | 4 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_PackageManagement_UI["<strong>NuGet.PackageManagement.UI</strong>"]
    NuGet_PackageManagement_VisualStudio["NuGet.PackageManagement.VisualStudio"]
    NuGet_PackageManagement_UI --> NuGet_PackageManagement_VisualStudio
    NuGet_PackageManagement_VisualStudio_Test["NuGet.PackageManagement.VisualStudio.Test"]
    NuGet_PackageManagement_VisualStudio_Test -.-> NuGet_PackageManagement_UI
    NuGet_PackageManagement_UI_Test["NuGet.PackageManagement.UI.Test"]
    NuGet_PackageManagement_UI_Test -.-> NuGet_PackageManagement_UI
    NuGet_PackageManagement_UI_TestContract["NuGet.PackageManagement.UI.TestContract"]
    NuGet_PackageManagement_UI_TestContract -.-> NuGet_PackageManagement_UI
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_PackageManagement_UI
    NuGet_Console["NuGet.Console"]
    NuGet_Console -.-> NuGet_PackageManagement_UI
```

## Project References
- NuGet.PackageManagement.VisualStudio

## Consumed By
- NuGet.PackageManagement.VisualStudio.Test
- NuGet.PackageManagement.UI.Test
- NuGet.PackageManagement.UI.TestContract
- NuGet.VisualStudio.Client
- NuGet.Console

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.VisualStudio.Copilot |  |
| Microsoft.VisualStudio.Markdown.Platform |  |
| Microsoft.VisualStudio.Sdk |  |
| Microsoft.VisualStudio.Shell.Styles |  |


---

*[Back to Index](../index.md)*
