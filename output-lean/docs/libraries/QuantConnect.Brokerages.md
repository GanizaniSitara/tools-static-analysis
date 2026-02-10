# QuantConnect.Brokerages

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | Lean |
| Path | `Brokerages/QuantConnect.Brokerages.csproj` |
| Project References | 5 |
| NuGet Dependencies | 3 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    QuantConnect_Brokerages["<strong>QuantConnect.Brokerages</strong>"]
    QuantConnect_Api["QuantConnect.Api"]
    QuantConnect_Brokerages --> QuantConnect_Api
    QuantConnect["QuantConnect"]
    QuantConnect_Brokerages --> QuantConnect
    QuantConnect_Compression["QuantConnect.Compression"]
    QuantConnect_Brokerages --> QuantConnect_Compression
    QuantConnect_Configuration["QuantConnect.Configuration"]
    QuantConnect_Brokerages --> QuantConnect_Configuration
    QuantConnect_Logging["QuantConnect.Logging"]
    QuantConnect_Brokerages --> QuantConnect_Logging
    QuantConnect_Lean_Engine["QuantConnect.Lean.Engine"]
    QuantConnect_Lean_Engine -.-> QuantConnect_Brokerages
    QuantConnect_Queues["QuantConnect.Queues"]
    QuantConnect_Queues -.-> QuantConnect_Brokerages
    QuantConnect_Tests["QuantConnect.Tests"]
    QuantConnect_Tests -.-> QuantConnect_Brokerages
    QuantConnect_Lean_Launcher["QuantConnect.Lean.Launcher"]
    QuantConnect_Lean_Launcher -.-> QuantConnect_Brokerages
    QuantConnect_Report["QuantConnect.Report"]
    QuantConnect_Report -.-> QuantConnect_Brokerages
```

## Project References
- QuantConnect.Api
- QuantConnect
- QuantConnect.Compression
- QuantConnect.Configuration
- QuantConnect.Logging

## Consumed By
- QuantConnect.Lean.Engine
- QuantConnect.Queues
- QuantConnect.Tests
- QuantConnect.Lean.Launcher
- QuantConnect.Report

## External NuGet Packages
| Package | Version |
|---------|---------||
| CsvHelper | 19.0.0 |
| Newtonsoft.Json | 13.0.2 |
| RestSharp | 106.12.0 |


---

*[Back to Index](../index.md)*
