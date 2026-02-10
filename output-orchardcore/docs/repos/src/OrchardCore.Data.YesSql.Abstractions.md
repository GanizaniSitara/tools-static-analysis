# OrchardCore.Data.YesSql.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Data.YesSql.Abstractions/OrchardCore.Data.YesSql.Abstractions.csproj` |
| Project References | 2 |
| NuGet Dependencies | 1 |
| Consumers | 6 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Data_YesSql_Abstractions["<strong>OrchardCore.Data.YesSql.Abstractions</strong>"]
    OrchardCore_Data_Abstractions["OrchardCore.Data.Abstractions"]
    OrchardCore_Data_YesSql_Abstractions --> OrchardCore_Data_Abstractions
    OrchardCore_Abstractions["OrchardCore.Abstractions"]
    OrchardCore_Data_YesSql_Abstractions --> OrchardCore_Abstractions
    OrchardCore_AuditTrail["OrchardCore.AuditTrail"]
    OrchardCore_AuditTrail -.-> OrchardCore_Data_YesSql_Abstractions
    OrchardCore_Lists["OrchardCore.Lists"]
    OrchardCore_Lists -.-> OrchardCore_Data_YesSql_Abstractions
    OrchardCore_Email["OrchardCore.Email"]
    OrchardCore_Email -.-> OrchardCore_Data_YesSql_Abstractions
    OrchardCore_Recipes_Abstractions["OrchardCore.Recipes.Abstractions"]
    OrchardCore_Recipes_Abstractions -.-> OrchardCore_Data_YesSql_Abstractions
    OrchardCore_Data_YesSql["OrchardCore.Data.YesSql"]
    OrchardCore_Data_YesSql -.-> OrchardCore_Data_YesSql_Abstractions
    OrchardCore_ContentManagement_Abstractions["OrchardCore.ContentManagement.Abstractions"]
    OrchardCore_ContentManagement_Abstractions -.-> OrchardCore_Data_YesSql_Abstractions
```

## Project References
- OrchardCore.Data.Abstractions
- OrchardCore.Abstractions

## Consumed By
- OrchardCore.AuditTrail
- OrchardCore.Lists
- OrchardCore.Email
- OrchardCore.Recipes.Abstractions
- OrchardCore.Data.YesSql
- OrchardCore.ContentManagement.Abstractions

## External NuGet Packages
| Package | Version |
|---------|---------||
| YesSql.Abstractions |  |


---

*[Back to Index](../../index.md)*
