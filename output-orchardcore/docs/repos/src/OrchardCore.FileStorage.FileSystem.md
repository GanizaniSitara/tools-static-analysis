# OrchardCore.FileStorage.FileSystem

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.FileStorage.FileSystem/OrchardCore.FileStorage.FileSystem.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_FileStorage_FileSystem["<strong>OrchardCore.FileStorage.FileSystem</strong>"]
    OrchardCore_FileStorage_Abstractions["OrchardCore.FileStorage.Abstractions"]
    OrchardCore_FileStorage_FileSystem --> OrchardCore_FileStorage_Abstractions
    OrchardCore_Media["OrchardCore.Media"]
    OrchardCore_Media -.-> OrchardCore_FileStorage_FileSystem
```

## Project References
- OrchardCore.FileStorage.Abstractions

## Consumed By
- OrchardCore.Media


---

*[Back to Index](../../index.md)*
