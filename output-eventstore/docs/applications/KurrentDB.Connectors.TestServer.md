# KurrentDB.Connectors.TestServer

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | src |
| Path | `Connectors/KurrentDB.Connectors.TestServer/KurrentDB.Connectors.TestServer.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_Connectors_TestServer["<strong>KurrentDB.Connectors.TestServer</strong>"]
    KurrentDB_Connectors["KurrentDB.Connectors"]
    KurrentDB_Connectors_TestServer --> KurrentDB_Connectors
    KurrentDB_SecondaryIndexing_LoadTesting["KurrentDB.SecondaryIndexing.LoadTesting"]
    KurrentDB_SecondaryIndexing_LoadTesting -.-> KurrentDB_Connectors_TestServer
```

## Project References
- KurrentDB.Connectors

## Consumed By
- KurrentDB.SecondaryIndexing.LoadTesting


---

*[Back to Index](../index.md)*
