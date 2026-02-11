# KurrentDB.Logging

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `KurrentDB.Logging/KurrentDB.Logging.csproj` |
| Project References | 1 |
| NuGet Dependencies | 4 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_Logging["<strong>KurrentDB.Logging</strong>"]
    KurrentDB_Common["KurrentDB.Common"]
    KurrentDB_Logging --> KurrentDB_Common
    KurrentDB_OtlpExporterPlugin["KurrentDB.OtlpExporterPlugin"]
    KurrentDB_OtlpExporterPlugin -.-> KurrentDB_Logging
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_Core -.-> KurrentDB_Logging
```

## Project References
- KurrentDB.Common

## Consumed By
- KurrentDB.OtlpExporterPlugin
- KurrentDB.Core

## External NuGet Packages
| Package | Version |
|---------|---------||
| OpenTelemetry.Exporter.OpenTelemetryProtocol |  |
| Serilog.Expressions |  |
| Serilog.Sinks.OpenTelemetry |  |
| System.Reactive |  |


---

*[Back to Index](../index.md)*
