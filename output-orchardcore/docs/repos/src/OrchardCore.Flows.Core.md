# OrchardCore.Flows.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Flows.Core/OrchardCore.Flows.Core.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Flows_Core["<strong>OrchardCore.Flows.Core</strong>"]
    OrchardCore_ContentManagement_Abstractions["OrchardCore.ContentManagement.Abstractions"]
    OrchardCore_Flows_Core --> OrchardCore_ContentManagement_Abstractions
    OrchardCore_Flows["OrchardCore.Flows"]
    OrchardCore_Flows -.-> OrchardCore_Flows_Core
    OrchardCore_Search_AzureAI["OrchardCore.Search.AzureAI"]
    OrchardCore_Search_AzureAI -.-> OrchardCore_Flows_Core
```

## Project References
- OrchardCore.ContentManagement.Abstractions

## Consumed By
- OrchardCore.Flows
- OrchardCore.Search.AzureAI


---

*[Back to Index](../../index.md)*
