# OrchardCore.Notifications.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Notifications.Core/OrchardCore.Notifications.Core.csproj` |
| Project References | 5 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Notifications_Core["<strong>OrchardCore.Notifications.Core</strong>"]
    OrchardCore_ContentManagement_Abstractions["OrchardCore.ContentManagement.Abstractions"]
    OrchardCore_Notifications_Core --> OrchardCore_ContentManagement_Abstractions
    OrchardCore_Email_Abstractions["OrchardCore.Email.Abstractions"]
    OrchardCore_Notifications_Core --> OrchardCore_Email_Abstractions
    OrchardCore_Infrastructure["OrchardCore.Infrastructure"]
    OrchardCore_Notifications_Core --> OrchardCore_Infrastructure
    OrchardCore_Notifications_Abstractions["OrchardCore.Notifications.Abstractions"]
    OrchardCore_Notifications_Core --> OrchardCore_Notifications_Abstractions
    OrchardCore_Users_Core["OrchardCore.Users.Core"]
    OrchardCore_Notifications_Core --> OrchardCore_Users_Core
    OrchardCore_Notifications["OrchardCore.Notifications"]
    OrchardCore_Notifications -.-> OrchardCore_Notifications_Core
```

## Project References
- OrchardCore.ContentManagement.Abstractions
- OrchardCore.Email.Abstractions
- OrchardCore.Infrastructure
- OrchardCore.Notifications.Abstractions
- OrchardCore.Users.Core

## Consumed By
- OrchardCore.Notifications


---

*[Back to Index](../../index.md)*
