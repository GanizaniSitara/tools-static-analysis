# OrchardCore.Notifications.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Notifications.Abstractions/OrchardCore.Notifications.Abstractions.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Notifications_Abstractions["<strong>OrchardCore.Notifications.Abstractions</strong>"]
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Notifications_Abstractions --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Notifications_Core["OrchardCore.Notifications.Core"]
    OrchardCore_Notifications_Core -.-> OrchardCore_Notifications_Abstractions
    OrchardCore_Sms_Core["OrchardCore.Sms.Core"]
    OrchardCore_Sms_Core -.-> OrchardCore_Notifications_Abstractions
```

## Project References
- OrchardCore.Infrastructure.Abstractions

## Consumed By
- OrchardCore.Notifications.Core
- OrchardCore.Sms.Core


---

*[Back to Index](../../index.md)*
