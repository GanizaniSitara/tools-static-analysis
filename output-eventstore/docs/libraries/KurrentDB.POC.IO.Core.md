# KurrentDB.POC.IO.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `KurrentDB.POC.IO.Core/KurrentDB.POC.IO.Core.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_POC_IO_Core["<strong>KurrentDB.POC.IO.Core</strong>"]
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_POC_IO_Core --> KurrentDB_Core
    KurrentDB_POC_ConnectedSubsystemsPlugin["KurrentDB.POC.ConnectedSubsystemsPlugin"]
    KurrentDB_POC_ConnectedSubsystemsPlugin -.-> KurrentDB_POC_IO_Core
    KurrentDB_AutoScavenge["KurrentDB.AutoScavenge"]
    KurrentDB_AutoScavenge -.-> KurrentDB_POC_IO_Core
```

## Project References
- KurrentDB.Core

## Consumed By
- KurrentDB.POC.ConnectedSubsystemsPlugin
- KurrentDB.AutoScavenge


---

*[Back to Index](../index.md)*
