# OrchardCore.Feeds.Abstractions

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Feeds.Abstractions/OrchardCore.Feeds.Abstractions.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Feeds_Abstractions["<strong>OrchardCore.Feeds.Abstractions</strong>"]
    OrchardCore_DisplayManagement_Abstractions["OrchardCore.DisplayManagement.Abstractions"]
    OrchardCore_Feeds_Abstractions --> OrchardCore_DisplayManagement_Abstractions
    OrchardCore_Lists["OrchardCore.Lists"]
    OrchardCore_Lists -.-> OrchardCore_Feeds_Abstractions
    OrchardCore_Contents["OrchardCore.Contents"]
    OrchardCore_Contents -.-> OrchardCore_Feeds_Abstractions
    OrchardCore_Feeds_Core["OrchardCore.Feeds.Core"]
    OrchardCore_Feeds_Core -.-> OrchardCore_Feeds_Abstractions
```

## Project References
- OrchardCore.DisplayManagement.Abstractions

## Consumed By
- OrchardCore.Lists
- OrchardCore.Contents
- OrchardCore.Feeds.Core


---

*[Back to Index](../../index.md)*
