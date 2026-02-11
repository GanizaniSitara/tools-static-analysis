# KurrentDB.TcpPlugin

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `KurrentDB.TcpPlugin/KurrentDB.TcpPlugin.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_TcpPlugin["<strong>KurrentDB.TcpPlugin</strong>"]
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_TcpPlugin --> KurrentDB_Core
    KurrentDB_TcpPlugin_Tests["KurrentDB.TcpPlugin.Tests"]
    KurrentDB_TcpPlugin_Tests -.-> KurrentDB_TcpPlugin
    KurrentDB["KurrentDB"]
    KurrentDB -.-> KurrentDB_TcpPlugin
```

## Project References
- KurrentDB.Core

## Consumed By
- KurrentDB.TcpPlugin.Tests
- KurrentDB


---

*[Back to Index](../index.md)*
