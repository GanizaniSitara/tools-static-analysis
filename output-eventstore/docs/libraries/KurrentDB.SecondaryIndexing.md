# KurrentDB.SecondaryIndexing

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `KurrentDB.SecondaryIndexing/KurrentDB.SecondaryIndexing.csproj` |
| Project References | 2 |
| NuGet Dependencies | 8 |
| Consumers | 4 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_SecondaryIndexing["<strong>KurrentDB.SecondaryIndexing</strong>"]
    KurrentDB_Common["KurrentDB.Common"]
    KurrentDB_SecondaryIndexing --> KurrentDB_Common
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_SecondaryIndexing --> KurrentDB_Core
    KurrentDB_Api_V2["KurrentDB.Api.V2"]
    KurrentDB_Api_V2 -.-> KurrentDB_SecondaryIndexing
    KurrentDB_SecondaryIndexing_LoadTesting["KurrentDB.SecondaryIndexing.LoadTesting"]
    KurrentDB_SecondaryIndexing_LoadTesting -.-> KurrentDB_SecondaryIndexing
    KurrentDB_SecondaryIndexing_Tests["KurrentDB.SecondaryIndexing.Tests"]
    KurrentDB_SecondaryIndexing_Tests -.-> KurrentDB_SecondaryIndexing
    KurrentDB["KurrentDB"]
    KurrentDB -.-> KurrentDB_SecondaryIndexing
```

## Project References
- KurrentDB.Common
- KurrentDB.Core

## Consumed By
- KurrentDB.Api.V2
- KurrentDB.SecondaryIndexing.LoadTesting
- KurrentDB.SecondaryIndexing.Tests
- KurrentDB

## External NuGet Packages
| Package | Version |
|---------|---------||
| Grpc.Tools |  |
| Kurrent.Quack |  |
| Kurrent.Surge.Core |  |
| Eventuous.Application |  |
| Eventuous.Extensions.DependencyInjection |  |
| Microsoft.AspNetCore.Grpc.JsonTranscoding |  |
| System.Linq.Async |  |
| Jint |  |


---

*[Back to Index](../index.md)*
