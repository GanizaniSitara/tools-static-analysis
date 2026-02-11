# KurrentDB.OtlpExporterPlugin

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `KurrentDB.OtlpExporterPlugin/KurrentDB.OtlpExporterPlugin.csproj` |
| Project References | 1 |
| NuGet Dependencies | 4 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_OtlpExporterPlugin["<strong>KurrentDB.OtlpExporterPlugin</strong>"]
    KurrentDB_Logging["KurrentDB.Logging"]
    KurrentDB_OtlpExporterPlugin --> KurrentDB_Logging
    KurrentDB_OtlpExporterPlugin_Tests["KurrentDB.OtlpExporterPlugin.Tests"]
    KurrentDB_OtlpExporterPlugin_Tests -.-> KurrentDB_OtlpExporterPlugin
    KurrentDB["KurrentDB"]
    KurrentDB -.-> KurrentDB_OtlpExporterPlugin
```

## Project References
- KurrentDB.Logging

## Consumed By
- KurrentDB.OtlpExporterPlugin.Tests
- KurrentDB

## External NuGet Packages
| Package | Version |
|---------|---------||
| OpenTelemetry.Exporter.OpenTelemetryProtocol |  |
| OpenTelemetry.Extensions.Hosting |  |
| Serilog |  |
| Serilog.Sinks.OpenTelemetry |  |


---

*[Back to Index](../index.md)*
