# KurrentDB.Projections.Core.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | src |
| Path | `KurrentDB.Projections.Core.Tests/KurrentDB.Projections.Core.Tests.csproj` |
| Project References | 4 |
| NuGet Dependencies | 4 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_Projections_Core_Tests["<strong>KurrentDB.Projections.Core.Tests</strong>"]
    KurrentDB_Common["KurrentDB.Common"]
    KurrentDB_Projections_Core_Tests --> KurrentDB_Common
    KurrentDB_Core_Testing_NUnit["KurrentDB.Core.Testing.NUnit"]
    KurrentDB_Projections_Core_Tests --> KurrentDB_Core_Testing_NUnit
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_Projections_Core_Tests --> KurrentDB_Core
    KurrentDB_Projections_Core["KurrentDB.Projections.Core"]
    KurrentDB_Projections_Core_Tests --> KurrentDB_Projections_Core
    KurrentDB_MicroBenchmarks["KurrentDB.MicroBenchmarks"]
    KurrentDB_MicroBenchmarks -.-> KurrentDB_Projections_Core_Tests
```

## Project References
- KurrentDB.Common
- KurrentDB.Core.Testing.NUnit
- KurrentDB.Core
- KurrentDB.Projections.Core

## Consumed By
- KurrentDB.MicroBenchmarks

## External NuGet Packages
| Package | Version |
|---------|---------||
| Newtonsoft.Json |  |
| Serilog.Sinks.TextWriter |  |
| Google.Protobuf |  |
| Grpc.Tools |  |


---

*[Back to Index](../index.md)*
