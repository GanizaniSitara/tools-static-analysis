# KurrentDB.Transport.Tcp

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `KurrentDB.Transport.Tcp/KurrentDB.Transport.Tcp.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_Transport_Tcp["<strong>KurrentDB.Transport.Tcp</strong>"]
    KurrentDB_BufferManagement["KurrentDB.BufferManagement"]
    KurrentDB_Transport_Tcp --> KurrentDB_BufferManagement
    KurrentDB_Common["KurrentDB.Common"]
    KurrentDB_Transport_Tcp --> KurrentDB_Common
    KurrentDB_TestClient["KurrentDB.TestClient"]
    KurrentDB_TestClient -.-> KurrentDB_Transport_Tcp
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_Core -.-> KurrentDB_Transport_Tcp
```

## Project References
- KurrentDB.BufferManagement
- KurrentDB.Common

## Consumed By
- KurrentDB.TestClient
- KurrentDB.Core


---

*[Back to Index](../index.md)*
