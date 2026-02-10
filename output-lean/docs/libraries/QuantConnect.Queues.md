# QuantConnect.Queues

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | Lean |
| Path | `Queues/QuantConnect.Queues.csproj` |
| Project References | 4 |
| NuGet Dependencies | 1 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    QuantConnect_Queues["<strong>QuantConnect.Queues</strong>"]
    QuantConnect_Brokerages["QuantConnect.Brokerages"]
    QuantConnect_Queues --> QuantConnect_Brokerages
    QuantConnect_Configuration["QuantConnect.Configuration"]
    QuantConnect_Queues --> QuantConnect_Configuration
    QuantConnect["QuantConnect"]
    QuantConnect_Queues --> QuantConnect
    QuantConnect_Logging["QuantConnect.Logging"]
    QuantConnect_Queues --> QuantConnect_Logging
    QuantConnect_Research["QuantConnect.Research"]
    QuantConnect_Research -.-> QuantConnect_Queues
    QuantConnect_Tests["QuantConnect.Tests"]
    QuantConnect_Tests -.-> QuantConnect_Queues
    QuantConnect_Lean_Launcher["QuantConnect.Lean.Launcher"]
    QuantConnect_Lean_Launcher -.-> QuantConnect_Queues
```

## Project References
- QuantConnect.Brokerages
- QuantConnect.Configuration
- QuantConnect
- QuantConnect.Logging

## Consumed By
- QuantConnect.Research
- QuantConnect.Tests
- QuantConnect.Lean.Launcher

## External NuGet Packages
| Package | Version |
|---------|---------||
| Newtonsoft.Json | 13.0.2 |


---

*[Back to Index](../index.md)*
