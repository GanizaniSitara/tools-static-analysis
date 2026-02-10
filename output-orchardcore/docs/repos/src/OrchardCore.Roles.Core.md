# OrchardCore.Roles.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Roles.Core/OrchardCore.Roles.Core.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Roles_Core["<strong>OrchardCore.Roles.Core</strong>"]
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Roles_Core --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Roles_Abstractions["OrchardCore.Roles.Abstractions"]
    OrchardCore_Roles_Core --> OrchardCore_Roles_Abstractions
    OrchardCore_Settings["OrchardCore.Settings"]
    OrchardCore_Settings -.-> OrchardCore_Roles_Core
    OrchardCore_Users["OrchardCore.Users"]
    OrchardCore_Users -.-> OrchardCore_Roles_Core
    OrchardCore_OpenId["OrchardCore.OpenId"]
    OrchardCore_OpenId -.-> OrchardCore_Roles_Core
    OrchardCore_Roles["OrchardCore.Roles"]
    OrchardCore_Roles -.-> OrchardCore_Roles_Core
    OrchardCore_Users_Core["OrchardCore.Users.Core"]
    OrchardCore_Users_Core -.-> OrchardCore_Roles_Core
```

## Project References
- OrchardCore.Infrastructure.Abstractions
- OrchardCore.Roles.Abstractions

## Consumed By
- OrchardCore.Settings
- OrchardCore.Users
- OrchardCore.OpenId
- OrchardCore.Roles
- OrchardCore.Users.Core


---

*[Back to Index](../../index.md)*
