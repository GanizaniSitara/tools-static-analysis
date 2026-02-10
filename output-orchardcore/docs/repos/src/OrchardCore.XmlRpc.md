# OrchardCore.XmlRpc

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.XmlRpc/OrchardCore.XmlRpc.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_XmlRpc["<strong>OrchardCore.XmlRpc</strong>"]
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_XmlRpc --> OrchardCore_Module_Targets
    OrchardCore_XmlRpc_Abstractions["OrchardCore.XmlRpc.Abstractions"]
    OrchardCore_XmlRpc --> OrchardCore_XmlRpc_Abstractions
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_XmlRpc
```

## Project References
- OrchardCore.Module.Targets
- OrchardCore.XmlRpc.Abstractions

## Consumed By
- OrchardCore.Application.Cms.Core.Targets


---

*[Back to Index](../../index.md)*
