# OrchardCore.AuditTrail.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.AuditTrail.Abstractions/OrchardCore.AuditTrail.Abstractions.csproj` |
| Project References | 2 |
| NuGet Dependencies | 1 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_AuditTrail_Abstractions["<strong>OrchardCore.AuditTrail.Abstractions</strong>"]
    OrchardCore_ContentManagement_Abstractions["OrchardCore.ContentManagement.Abstractions"]
    OrchardCore_AuditTrail_Abstractions --> OrchardCore_ContentManagement_Abstractions
    OrchardCore_ContentManagement_Display["OrchardCore.ContentManagement.Display"]
    OrchardCore_AuditTrail_Abstractions --> OrchardCore_ContentManagement_Display
    OrchardCore_AuditTrail["OrchardCore.AuditTrail"]
    OrchardCore_AuditTrail -.-> OrchardCore_AuditTrail_Abstractions
    OrchardCore_Users["OrchardCore.Users"]
    OrchardCore_Users -.-> OrchardCore_AuditTrail_Abstractions
    OrchardCore_Contents["OrchardCore.Contents"]
    OrchardCore_Contents -.-> OrchardCore_AuditTrail_Abstractions
```

## Project References
- OrchardCore.ContentManagement.Abstractions
- OrchardCore.ContentManagement.Display

## Consumed By
- OrchardCore.AuditTrail
- OrchardCore.Users
- OrchardCore.Contents

## External NuGet Packages
| Package | Version |
|---------|---------||
| YesSql.Filters.Query |  |


---

*[Back to Index](../../index.md)*
