# KurrentDB.AutoScavenge

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `KurrentDB.AutoScavenge/KurrentDB.AutoScavenge.csproj` |
| Project References | 2 |
| NuGet Dependencies | 1 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_AutoScavenge["<strong>KurrentDB.AutoScavenge</strong>"]
    KurrentDB_POC_ConnectedSubsystemsPlugin["KurrentDB.POC.ConnectedSubsystemsPlugin"]
    KurrentDB_AutoScavenge --> KurrentDB_POC_ConnectedSubsystemsPlugin
    KurrentDB_POC_IO_Core["KurrentDB.POC.IO.Core"]
    KurrentDB_AutoScavenge --> KurrentDB_POC_IO_Core
    KurrentDB_AutoScavenge_Tests["KurrentDB.AutoScavenge.Tests"]
    KurrentDB_AutoScavenge_Tests -.-> KurrentDB_AutoScavenge
    KurrentDB["KurrentDB"]
    KurrentDB -.-> KurrentDB_AutoScavenge
```

## Project References
- KurrentDB.POC.ConnectedSubsystemsPlugin
- KurrentDB.POC.IO.Core

## Consumed By
- KurrentDB.AutoScavenge.Tests
- KurrentDB

## External NuGet Packages
| Package | Version |
|---------|---------||
| NCrontab |  |


---

*[Back to Index](../index.md)*
