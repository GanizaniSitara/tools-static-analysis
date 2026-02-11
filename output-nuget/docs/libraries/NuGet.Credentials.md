# NuGet.Credentials

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Core/NuGet.Credentials/NuGet.Credentials.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Credentials["<strong>NuGet.Credentials</strong>"]
    NuGet_Protocol["NuGet.Protocol"]
    NuGet_Credentials --> NuGet_Protocol
    NuGet_Credentials_Test["NuGet.Credentials.Test"]
    NuGet_Credentials_Test -.-> NuGet_Credentials
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_Credentials
    NuGet_Commands["NuGet.Commands"]
    NuGet_Commands -.-> NuGet_Credentials
```

## Project References
- NuGet.Protocol

## Consumed By
- NuGet.Credentials.Test
- NuGet.VisualStudio.Client
- NuGet.Commands


---

*[Back to Index](../index.md)*
