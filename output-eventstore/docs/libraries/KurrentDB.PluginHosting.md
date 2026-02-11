# KurrentDB.PluginHosting

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `KurrentDB.PluginHosting/KurrentDB.PluginHosting.csproj` |
| Project References | 0 |
| NuGet Dependencies | 0 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_PluginHosting["<strong>KurrentDB.PluginHosting</strong>"]
    KurrentDB_Core_Testing["KurrentDB.Core.Testing"]
    KurrentDB_Core_Testing -.-> KurrentDB_PluginHosting
    KurrentDB_POC_ConnectedSubsystemsPlugin["KurrentDB.POC.ConnectedSubsystemsPlugin"]
    KurrentDB_POC_ConnectedSubsystemsPlugin -.-> KurrentDB_PluginHosting
    KurrentDB["KurrentDB"]
    KurrentDB -.-> KurrentDB_PluginHosting
```

## Consumed By
- KurrentDB.Core.Testing
- KurrentDB.POC.ConnectedSubsystemsPlugin
- KurrentDB


---

*[Back to Index](../index.md)*
