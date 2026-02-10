# OrchardCore.Roles.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Roles.Abstractions/OrchardCore.Roles.Abstractions.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Roles_Abstractions["<strong>OrchardCore.Roles.Abstractions</strong>"]
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Roles_Abstractions --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Cors["OrchardCore.Cors"]
    OrchardCore_Cors -.-> OrchardCore_Roles_Abstractions
    OrchardCore_Roles_Core["OrchardCore.Roles.Core"]
    OrchardCore_Roles_Core -.-> OrchardCore_Roles_Abstractions
```

## Project References
- OrchardCore.Infrastructure.Abstractions

## Consumed By
- OrchardCore.Cors
- OrchardCore.Roles.Core

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.AspNetCore.Authorization |  |


---

*[Back to Index](../../index.md)*
