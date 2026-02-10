# OrchardCore.Email.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Email.Core/OrchardCore.Email.Core.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Email_Core["<strong>OrchardCore.Email.Core</strong>"]
    OrchardCore_Email_Abstractions["OrchardCore.Email.Abstractions"]
    OrchardCore_Email_Core --> OrchardCore_Email_Abstractions
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Email_Core --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Email_Azure["OrchardCore.Email.Azure"]
    OrchardCore_Email_Azure -.-> OrchardCore_Email_Core
    OrchardCore_Email["OrchardCore.Email"]
    OrchardCore_Email -.-> OrchardCore_Email_Core
    OrchardCore_Email_Smtp["OrchardCore.Email.Smtp"]
    OrchardCore_Email_Smtp -.-> OrchardCore_Email_Core
```

## Project References
- OrchardCore.Email.Abstractions
- OrchardCore.Infrastructure.Abstractions

## Consumed By
- OrchardCore.Email.Azure
- OrchardCore.Email
- OrchardCore.Email.Smtp


---

*[Back to Index](../../index.md)*
