# OrchardCore.Email.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Email.Abstractions/OrchardCore.Email.Abstractions.csproj` |
| Project References | 0 |
| NuGet Dependencies | 0 |
| Consumers | 4 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Email_Abstractions["<strong>OrchardCore.Email.Abstractions</strong>"]
    OrchardCore_Users["OrchardCore.Users"]
    OrchardCore_Users -.-> OrchardCore_Email_Abstractions
    OrchardCore_Email_Smtp["OrchardCore.Email.Smtp"]
    OrchardCore_Email_Smtp -.-> OrchardCore_Email_Abstractions
    OrchardCore_Notifications_Core["OrchardCore.Notifications.Core"]
    OrchardCore_Notifications_Core -.-> OrchardCore_Email_Abstractions
    OrchardCore_Email_Core["OrchardCore.Email.Core"]
    OrchardCore_Email_Core -.-> OrchardCore_Email_Abstractions
```

## Consumed By
- OrchardCore.Users
- OrchardCore.Email.Smtp
- OrchardCore.Notifications.Core
- OrchardCore.Email.Core


---

*[Back to Index](../../index.md)*
