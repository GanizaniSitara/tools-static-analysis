# OrchardCore.Users.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Users.Abstractions/OrchardCore.Users.Abstractions.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 6 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Users_Abstractions["<strong>OrchardCore.Users.Abstractions</strong>"]
    OrchardCore_Abstractions["OrchardCore.Abstractions"]
    OrchardCore_Users_Abstractions --> OrchardCore_Abstractions
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Users_Abstractions --> OrchardCore_Infrastructure_Abstractions
    TheTheme["TheTheme"]
    TheTheme -.-> OrchardCore_Users_Abstractions
    OrchardCore_OpenId["OrchardCore.OpenId"]
    OrchardCore_OpenId -.-> OrchardCore_Users_Abstractions
    OrchardCore_Lists["OrchardCore.Lists"]
    OrchardCore_Lists -.-> OrchardCore_Users_Abstractions
    OrchardCore_Contents["OrchardCore.Contents"]
    OrchardCore_Contents -.-> OrchardCore_Users_Abstractions
    OrchardCore_ReCaptcha["OrchardCore.ReCaptcha"]
    OrchardCore_ReCaptcha -.-> OrchardCore_Users_Abstractions
    OrchardCore_Users_Core["OrchardCore.Users.Core"]
    OrchardCore_Users_Core -.-> OrchardCore_Users_Abstractions
```

## Project References
- OrchardCore.Abstractions
- OrchardCore.Infrastructure.Abstractions

## Consumed By
- TheTheme
- OrchardCore.OpenId
- OrchardCore.Lists
- OrchardCore.Contents
- OrchardCore.ReCaptcha
- OrchardCore.Users.Core


---

*[Back to Index](../../index.md)*
