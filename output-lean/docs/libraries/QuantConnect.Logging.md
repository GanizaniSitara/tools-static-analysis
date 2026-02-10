# QuantConnect.Logging

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | Lean |
| Path | `Logging/QuantConnect.Logging.csproj` |
| Project References | 0 |
| NuGet Dependencies | 1 |
| Consumers | 18 |

## Dependency Diagram

```mermaid
graph TD
    QuantConnect_Logging["<strong>QuantConnect.Logging</strong>"]
    QuantConnect_Api["QuantConnect.Api"]
    QuantConnect_Api -.-> QuantConnect_Logging
    QuantConnect_Configuration["QuantConnect.Configuration"]
    QuantConnect_Configuration -.-> QuantConnect_Logging
    QuantConnect_Compression["QuantConnect.Compression"]
    QuantConnect_Compression -.-> QuantConnect_Logging
    QuantConnect_Optimizer_Launcher["QuantConnect.Optimizer.Launcher"]
    QuantConnect_Optimizer_Launcher -.-> QuantConnect_Logging
    QuantConnect_Messaging["QuantConnect.Messaging"]
    QuantConnect_Messaging -.-> QuantConnect_Logging
    QuantConnect_Research["QuantConnect.Research"]
    QuantConnect_Research -.-> QuantConnect_Logging
    QuantConnect_Brokerages["QuantConnect.Brokerages"]
    QuantConnect_Brokerages -.-> QuantConnect_Logging
    QuantConnect_DownloaderDataProvider_Launcher["QuantConnect.DownloaderDataProvider.Launcher"]
    QuantConnect_DownloaderDataProvider_Launcher -.-> QuantConnect_Logging
    QuantConnect_Lean_Engine["QuantConnect.Lean.Engine"]
    QuantConnect_Lean_Engine -.-> QuantConnect_Logging
    QuantConnect_Queues["QuantConnect.Queues"]
    QuantConnect_Queues -.-> QuantConnect_Logging
    QuantConnect_AlgorithmFactory["QuantConnect.AlgorithmFactory"]
    QuantConnect_AlgorithmFactory -.-> QuantConnect_Logging
    QuantConnect["QuantConnect"]
    QuantConnect -.-> QuantConnect_Logging
    QuantConnect_Tests["QuantConnect.Tests"]
    QuantConnect_Tests -.-> QuantConnect_Logging
    QuantConnect_Indicators["QuantConnect.Indicators"]
    QuantConnect_Indicators -.-> QuantConnect_Logging
    QuantConnect_Optimizer["QuantConnect.Optimizer"]
    QuantConnect_Optimizer -.-> QuantConnect_Logging
    more_consumers["... +3 more"]
    more_consumers -.-> QuantConnect_Logging
```

## Consumed By
- QuantConnect.Api
- QuantConnect.Configuration
- QuantConnect.Compression
- QuantConnect.Optimizer.Launcher
- QuantConnect.Messaging
- QuantConnect.Research
- QuantConnect.Brokerages
- QuantConnect.DownloaderDataProvider.Launcher
- QuantConnect.Lean.Engine
- QuantConnect.Queues
- QuantConnect.AlgorithmFactory
- QuantConnect
- QuantConnect.Tests
- QuantConnect.Indicators
- QuantConnect.Optimizer
- QuantConnect.Lean.Launcher
- QuantConnect.Report
- QuantConnect.Algorithm

## External NuGet Packages
| Package | Version |
|---------|---------||
| System.ComponentModel.Composition | 6.0.0 |


---

*[Back to Index](../index.md)*
