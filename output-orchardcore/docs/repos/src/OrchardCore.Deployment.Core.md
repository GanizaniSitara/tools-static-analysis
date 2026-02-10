# OrchardCore.Deployment.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore/OrchardCore.Deployment.Core/OrchardCore.Deployment.Core.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 4 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Deployment_Core["<strong>OrchardCore.Deployment.Core</strong>"]
    OrchardCore_Deployment_Abstractions["OrchardCore.Deployment.Abstractions"]
    OrchardCore_Deployment_Core --> OrchardCore_Deployment_Abstractions
    OrchardCore_Deployment["OrchardCore.Deployment"]
    OrchardCore_Deployment -.-> OrchardCore_Deployment_Core
    OrchardCore_Workflows["OrchardCore.Workflows"]
    OrchardCore_Workflows -.-> OrchardCore_Deployment_Core
    OrchardCore_Contents["OrchardCore.Contents"]
    OrchardCore_Contents -.-> OrchardCore_Deployment_Core
    OrchardCore_Deployment_Remote["OrchardCore.Deployment.Remote"]
    OrchardCore_Deployment_Remote -.-> OrchardCore_Deployment_Core
```

## Project References
- OrchardCore.Deployment.Abstractions

## Consumed By
- OrchardCore.Deployment
- OrchardCore.Workflows
- OrchardCore.Contents
- OrchardCore.Deployment.Remote


---

*[Back to Index](../../index.md)*
