# KurrentDB.SystemRuntime

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `KurrentDB.SystemRuntime/KurrentDB.SystemRuntime.csproj` |
| Project References | 0 |
| NuGet Dependencies | 2 |
| Consumers | 4 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_SystemRuntime["<strong>KurrentDB.SystemRuntime</strong>"]
    KurrentDB_Native["KurrentDB.Native"]
    KurrentDB_Native -.-> KurrentDB_SystemRuntime
    KurrentDB_Common["KurrentDB.Common"]
    KurrentDB_Common -.-> KurrentDB_SystemRuntime
    KurrentDB_SystemRuntime_Tests["KurrentDB.SystemRuntime.Tests"]
    KurrentDB_SystemRuntime_Tests -.-> KurrentDB_SystemRuntime
    KurrentDB_Connectors["KurrentDB.Connectors"]
    KurrentDB_Connectors -.-> KurrentDB_SystemRuntime
```

## Consumed By
- KurrentDB.Native
- KurrentDB.Common
- KurrentDB.SystemRuntime.Tests
- KurrentDB.Connectors

## External NuGet Packages
| Package | Version |
|---------|---------||
| Serilog |  |
| System.Diagnostics.PerformanceCounter |  |


---

*[Back to Index](../index.md)*
