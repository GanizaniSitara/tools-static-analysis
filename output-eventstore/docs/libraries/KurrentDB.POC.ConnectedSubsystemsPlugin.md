# KurrentDB.POC.ConnectedSubsystemsPlugin

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `KurrentDB.POC.ConnectedSubsystemsPlugin/KurrentDB.POC.ConnectedSubsystemsPlugin.csproj` |
| Project References | 3 |
| NuGet Dependencies | 1 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_POC_ConnectedSubsystemsPlugin["<strong>KurrentDB.POC.ConnectedSubsystemsPlugin</strong>"]
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_POC_ConnectedSubsystemsPlugin --> KurrentDB_Core
    KurrentDB_PluginHosting["KurrentDB.PluginHosting"]
    KurrentDB_POC_ConnectedSubsystemsPlugin --> KurrentDB_PluginHosting
    KurrentDB_POC_IO_Core["KurrentDB.POC.IO.Core"]
    KurrentDB_POC_ConnectedSubsystemsPlugin --> KurrentDB_POC_IO_Core
    KurrentDB_AutoScavenge["KurrentDB.AutoScavenge"]
    KurrentDB_AutoScavenge -.-> KurrentDB_POC_ConnectedSubsystemsPlugin
    KurrentDB["KurrentDB"]
    KurrentDB -.-> KurrentDB_POC_ConnectedSubsystemsPlugin
```

## Project References
- KurrentDB.Core
- KurrentDB.PluginHosting
- KurrentDB.POC.IO.Core

## Consumed By
- KurrentDB.AutoScavenge
- KurrentDB

## External NuGet Packages
| Package | Version |
|---------|---------||
| System.Linq.Async |  |


---

*[Back to Index](../index.md)*
