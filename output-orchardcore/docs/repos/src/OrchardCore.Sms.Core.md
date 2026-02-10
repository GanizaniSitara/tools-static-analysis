# OrchardCore.Sms.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Sms.Core/OrchardCore.Sms.Core.csproj` |
| Project References | 5 |
| NuGet Dependencies | 2 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Sms_Core["<strong>OrchardCore.Sms.Core</strong>"]
    OrchardCore_Abstractions["OrchardCore.Abstractions"]
    OrchardCore_Sms_Core --> OrchardCore_Abstractions
    OrchardCore_Infrastructure_Abstractions["OrchardCore.Infrastructure.Abstractions"]
    OrchardCore_Sms_Core --> OrchardCore_Infrastructure_Abstractions
    OrchardCore_Notifications_Abstractions["OrchardCore.Notifications.Abstractions"]
    OrchardCore_Sms_Core --> OrchardCore_Notifications_Abstractions
    OrchardCore_Sms_Abstractions["OrchardCore.Sms.Abstractions"]
    OrchardCore_Sms_Core --> OrchardCore_Sms_Abstractions
    OrchardCore_Users_Core["OrchardCore.Users.Core"]
    OrchardCore_Sms_Core --> OrchardCore_Users_Core
    OrchardCore_Sms["OrchardCore.Sms"]
    OrchardCore_Sms -.-> OrchardCore_Sms_Core
    OrchardCore_Users["OrchardCore.Users"]
    OrchardCore_Users -.-> OrchardCore_Sms_Core
    OrchardCore_Sms_Azure["OrchardCore.Sms.Azure"]
    OrchardCore_Sms_Azure -.-> OrchardCore_Sms_Core
```

## Project References
- OrchardCore.Abstractions
- OrchardCore.Infrastructure.Abstractions
- OrchardCore.Notifications.Abstractions
- OrchardCore.Sms.Abstractions
- OrchardCore.Users.Core

## Consumed By
- OrchardCore.Sms
- OrchardCore.Users
- OrchardCore.Sms.Azure

## External NuGet Packages
| Package | Version |
|---------|---------||
| libphonenumber-csharp |  |
| Microsoft.Extensions.Http.Resilience |  |


---

*[Back to Index](../../index.md)*
