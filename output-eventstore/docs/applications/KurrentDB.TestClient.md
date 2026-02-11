# KurrentDB.TestClient

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | src |
| Path | `KurrentDB.TestClient/KurrentDB.TestClient.csproj` |
| Project References | 5 |
| NuGet Dependencies | 6 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_TestClient["<strong>KurrentDB.TestClient</strong>"]
    KurrentDB_BufferManagement["KurrentDB.BufferManagement"]
    KurrentDB_TestClient --> KurrentDB_BufferManagement
    KurrentDB_Common["KurrentDB.Common"]
    KurrentDB_TestClient --> KurrentDB_Common
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_TestClient --> KurrentDB_Core
    KurrentDB_Transport_Http["KurrentDB.Transport.Http"]
    KurrentDB_TestClient --> KurrentDB_Transport_Http
    KurrentDB_Transport_Tcp["KurrentDB.Transport.Tcp"]
    KurrentDB_TestClient --> KurrentDB_Transport_Tcp
```

## Project References
- KurrentDB.BufferManagement
- KurrentDB.Common
- KurrentDB.Core
- KurrentDB.Transport.Http
- KurrentDB.Transport.Tcp

## External NuGet Packages
| Package | Version |
|---------|---------||
| EventStore.Client |  |
| EventStore.Client.Grpc.Streams |  |
| Google.Protobuf |  |
| Grpc.Net.Client |  |
| Grpc.Tools |  |
| System.CommandLine.DragonFruit |  |


---

*[Back to Index](../index.md)*
