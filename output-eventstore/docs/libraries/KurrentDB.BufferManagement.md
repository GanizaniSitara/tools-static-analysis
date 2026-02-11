# KurrentDB.BufferManagement

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `KurrentDB.BufferManagement/KurrentDB.BufferManagement.csproj` |
| Project References | 0 |
| NuGet Dependencies | 1 |
| Consumers | 4 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_BufferManagement["<strong>KurrentDB.BufferManagement</strong>"]
    KurrentDB_Transport_Http["KurrentDB.Transport.Http"]
    KurrentDB_Transport_Http -.-> KurrentDB_BufferManagement
    KurrentDB_BufferManagement_Tests["KurrentDB.BufferManagement.Tests"]
    KurrentDB_BufferManagement_Tests -.-> KurrentDB_BufferManagement
    KurrentDB_Transport_Tcp["KurrentDB.Transport.Tcp"]
    KurrentDB_Transport_Tcp -.-> KurrentDB_BufferManagement
    KurrentDB_TestClient["KurrentDB.TestClient"]
    KurrentDB_TestClient -.-> KurrentDB_BufferManagement
```

## Consumed By
- KurrentDB.Transport.Http
- KurrentDB.BufferManagement.Tests
- KurrentDB.Transport.Tcp
- KurrentDB.TestClient

## External NuGet Packages
| Package | Version |
|---------|---------||
| Serilog |  |


---

*[Back to Index](../index.md)*
