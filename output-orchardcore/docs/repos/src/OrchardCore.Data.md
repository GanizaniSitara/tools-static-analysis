# OrchardCore.Data

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Data/OrchardCore.Data.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Data["<strong>OrchardCore.Data</strong>"]
    OrchardCore_Data_Abstractions["OrchardCore.Data.Abstractions"]
    OrchardCore_Data --> OrchardCore_Data_Abstractions
    OrchardCore_Abstractions["OrchardCore.Abstractions"]
    OrchardCore_Data --> OrchardCore_Abstractions
    OrchardCore_Setup["OrchardCore.Setup"]
    OrchardCore_Setup -.-> OrchardCore_Data
    OrchardCore_Data_YesSql["OrchardCore.Data.YesSql"]
    OrchardCore_Data_YesSql -.-> OrchardCore_Data
```

## Project References
- OrchardCore.Data.Abstractions
- OrchardCore.Abstractions

## Consumed By
- OrchardCore.Setup
- OrchardCore.Data.YesSql


---

*[Back to Index](../../index.md)*
