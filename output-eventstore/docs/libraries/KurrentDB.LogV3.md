# KurrentDB.LogV3

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `KurrentDB.LogV3/KurrentDB.LogV3.csproj` |
| Project References | 1 |
| NuGet Dependencies | 2 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_LogV3["<strong>KurrentDB.LogV3</strong>"]
    KurrentDB_LogCommon["KurrentDB.LogCommon"]
    KurrentDB_LogV3 --> KurrentDB_LogCommon
    KurrentDB_LogV3_Tests["KurrentDB.LogV3.Tests"]
    KurrentDB_LogV3_Tests -.-> KurrentDB_LogV3
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_Core -.-> KurrentDB_LogV3
```

## Project References
- KurrentDB.LogCommon

## Consumed By
- KurrentDB.LogV3.Tests
- KurrentDB.Core

## External NuGet Packages
| Package | Version |
|---------|---------||
| Google.Protobuf |  |
| Grpc.Tools |  |


---

*[Back to Index](../index.md)*
