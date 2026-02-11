# KurrentDB.Transport.Http

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `KurrentDB.Transport.Http/KurrentDB.Transport.Http.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_Transport_Http["<strong>KurrentDB.Transport.Http</strong>"]
    KurrentDB_BufferManagement["KurrentDB.BufferManagement"]
    KurrentDB_Transport_Http --> KurrentDB_BufferManagement
    KurrentDB_Common["KurrentDB.Common"]
    KurrentDB_Transport_Http --> KurrentDB_Common
    KurrentDB_Projections_Core["KurrentDB.Projections.Core"]
    KurrentDB_Projections_Core -.-> KurrentDB_Transport_Http
    KurrentDB_TestClient["KurrentDB.TestClient"]
    KurrentDB_TestClient -.-> KurrentDB_Transport_Http
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_Core -.-> KurrentDB_Transport_Http
```

## Project References
- KurrentDB.BufferManagement
- KurrentDB.Common

## Consumed By
- KurrentDB.Projections.Core
- KurrentDB.TestClient
- KurrentDB.Core


---

*[Back to Index](../index.md)*
