# KurrentDB.Projections.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `KurrentDB.Projections.Core/KurrentDB.Projections.Core.csproj` |
| Project References | 4 |
| NuGet Dependencies | 3 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_Projections_Core["<strong>KurrentDB.Projections.Core</strong>"]
    KurrentDB_Common["KurrentDB.Common"]
    KurrentDB_Projections_Core --> KurrentDB_Common
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_Projections_Core --> KurrentDB_Core
    KurrentDB_Transport_Http["KurrentDB.Transport.Http"]
    KurrentDB_Projections_Core --> KurrentDB_Transport_Http
    KurrentDB_SourceGenerators["KurrentDB.SourceGenerators"]
    KurrentDB_Projections_Core --> KurrentDB_SourceGenerators
    KurrentDB_Projections_Core_Tests["KurrentDB.Projections.Core.Tests"]
    KurrentDB_Projections_Core_Tests -.-> KurrentDB_Projections_Core
    KurrentDB_Projections_Core_XUnit_Tests["KurrentDB.Projections.Core.XUnit.Tests"]
    KurrentDB_Projections_Core_XUnit_Tests -.-> KurrentDB_Projections_Core
    KurrentDB_MicroBenchmarks["KurrentDB.MicroBenchmarks"]
    KurrentDB_MicroBenchmarks -.-> KurrentDB_Projections_Core
    KurrentDB_Projections_Core_Javascript_Tests["KurrentDB.Projections.Core.Javascript.Tests"]
    KurrentDB_Projections_Core_Javascript_Tests -.-> KurrentDB_Projections_Core
    KurrentDB["KurrentDB"]
    KurrentDB -.-> KurrentDB_Projections_Core
```

## Project References
- KurrentDB.Common
- KurrentDB.Core
- KurrentDB.Transport.Http
- KurrentDB.SourceGenerators

## Consumed By
- KurrentDB.Projections.Core.Tests
- KurrentDB.Projections.Core.XUnit.Tests
- KurrentDB.MicroBenchmarks
- KurrentDB.Projections.Core.Javascript.Tests
- KurrentDB

## External NuGet Packages
| Package | Version |
|---------|---------||
| Grpc.Tools |  |
| Newtonsoft.Json |  |
| Jint |  |


---

*[Back to Index](../index.md)*
