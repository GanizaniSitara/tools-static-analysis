# QuantConnect.Report

## Overview

| Property | Value |
|----------|-------|
| Category | Application |
| Repository | Lean |
| Path | `Report/QuantConnect.Report.csproj` |
| Project References | 9 |
| NuGet Dependencies | 5 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    QuantConnect_Report["<strong>QuantConnect.Report</strong>"]
    QuantConnect_Algorithm["QuantConnect.Algorithm"]
    QuantConnect_Report --> QuantConnect_Algorithm
    QuantConnect_Api["QuantConnect.Api"]
    QuantConnect_Report --> QuantConnect_Api
    QuantConnect_Brokerages["QuantConnect.Brokerages"]
    QuantConnect_Report --> QuantConnect_Brokerages
    QuantConnect["QuantConnect"]
    QuantConnect_Report --> QuantConnect
    QuantConnect_Configuration["QuantConnect.Configuration"]
    QuantConnect_Report --> QuantConnect_Configuration
    QuantConnect_Lean_Engine["QuantConnect.Lean.Engine"]
    QuantConnect_Report --> QuantConnect_Lean_Engine
    QuantConnect_Logging["QuantConnect.Logging"]
    QuantConnect_Report --> QuantConnect_Logging
    QuantConnect_Messaging["QuantConnect.Messaging"]
    QuantConnect_Report --> QuantConnect_Messaging
    QuantConnect_ToolBox["QuantConnect.ToolBox"]
    QuantConnect_Report --> QuantConnect_ToolBox
    QuantConnect_Tests["QuantConnect.Tests"]
    QuantConnect_Tests -.-> QuantConnect_Report
```

## Project References
- QuantConnect.Algorithm
- QuantConnect.Api
- QuantConnect.Brokerages
- QuantConnect
- QuantConnect.Configuration
- QuantConnect.Lean.Engine
- QuantConnect.Logging
- QuantConnect.Messaging
- QuantConnect.ToolBox

## Consumed By
- QuantConnect.Tests

## External NuGet Packages
| Package | Version |
|---------|---------||
| QuantConnect.pythonnet | 2.0.52 |
| Deedle | 2.1.0 |
| MathNet.Numerics | 5.0.0 |
| Newtonsoft.Json | 13.0.2 |
| NodaTime | 3.0.5 |


---

*[Back to Index](../index.md)*
