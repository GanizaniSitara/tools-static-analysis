# QuantConnect.Api

## Overview

| Property | Value |
|----------|-------|
| Category | WebApp |
| Repository | Lean |
| Path | `Api/QuantConnect.Api.csproj` |
| Project References | 3 |
| NuGet Dependencies | 3 |
| Consumers | 6 |

## Dependency Diagram

```mermaid
graph TD
    QuantConnect_Api["<strong>QuantConnect.Api</strong>"]
    QuantConnect["QuantConnect"]
    QuantConnect_Api --> QuantConnect
    QuantConnect_Configuration["QuantConnect.Configuration"]
    QuantConnect_Api --> QuantConnect_Configuration
    QuantConnect_Logging["QuantConnect.Logging"]
    QuantConnect_Api --> QuantConnect_Logging
    QuantConnect_Research["QuantConnect.Research"]
    QuantConnect_Research -.-> QuantConnect_Api
    QuantConnect_Brokerages["QuantConnect.Brokerages"]
    QuantConnect_Brokerages -.-> QuantConnect_Api
    QuantConnect_Lean_Engine["QuantConnect.Lean.Engine"]
    QuantConnect_Lean_Engine -.-> QuantConnect_Api
    QuantConnect_Tests["QuantConnect.Tests"]
    QuantConnect_Tests -.-> QuantConnect_Api
    QuantConnect_Lean_Launcher["QuantConnect.Lean.Launcher"]
    QuantConnect_Lean_Launcher -.-> QuantConnect_Api
    QuantConnect_Report["QuantConnect.Report"]
    QuantConnect_Report -.-> QuantConnect_Api
```

## Project References
- QuantConnect
- QuantConnect.Configuration
- QuantConnect.Logging

## Consumed By
- QuantConnect.Research
- QuantConnect.Brokerages
- QuantConnect.Lean.Engine
- QuantConnect.Tests
- QuantConnect.Lean.Launcher
- QuantConnect.Report

## External NuGet Packages
| Package | Version |
|---------|---------||
| Newtonsoft.Json | 13.0.2 |
| NodaTime | 3.0.5 |
| RestSharp | 106.12.0 |


---

*[Back to Index](../index.md)*
