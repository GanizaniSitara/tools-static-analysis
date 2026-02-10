# QuantConnect.Messaging

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | Lean |
| Path | `Messaging/QuantConnect.Messaging.csproj` |
| Project References | 3 |
| NuGet Dependencies | 2 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    QuantConnect_Messaging["<strong>QuantConnect.Messaging</strong>"]
    QuantConnect["QuantConnect"]
    QuantConnect_Messaging --> QuantConnect
    QuantConnect_Configuration["QuantConnect.Configuration"]
    QuantConnect_Messaging --> QuantConnect_Configuration
    QuantConnect_Logging["QuantConnect.Logging"]
    QuantConnect_Messaging --> QuantConnect_Logging
    QuantConnect_Tests["QuantConnect.Tests"]
    QuantConnect_Tests -.-> QuantConnect_Messaging
    QuantConnect_Lean_Launcher["QuantConnect.Lean.Launcher"]
    QuantConnect_Lean_Launcher -.-> QuantConnect_Messaging
    QuantConnect_Report["QuantConnect.Report"]
    QuantConnect_Report -.-> QuantConnect_Messaging
```

## Project References
- QuantConnect
- QuantConnect.Configuration
- QuantConnect.Logging

## Consumed By
- QuantConnect.Tests
- QuantConnect.Lean.Launcher
- QuantConnect.Report

## External NuGet Packages
| Package | Version |
|---------|---------||
| NetMQ | 4.0.1.6 |
| Newtonsoft.Json | 13.0.2 |


---

*[Back to Index](../index.md)*
