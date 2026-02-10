# QuantConnect.Optimizer.Launcher

## Overview

| Property | Value |
|----------|-------|
| Category | Application |
| Repository | Lean |
| Path | `Optimizer.Launcher/QuantConnect.Optimizer.Launcher.csproj` |
| Project References | 4 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    QuantConnect_Optimizer_Launcher["<strong>QuantConnect.Optimizer.Launcher</strong>"]
    QuantConnect["QuantConnect"]
    QuantConnect_Optimizer_Launcher --> QuantConnect
    QuantConnect_Configuration["QuantConnect.Configuration"]
    QuantConnect_Optimizer_Launcher --> QuantConnect_Configuration
    QuantConnect_Logging["QuantConnect.Logging"]
    QuantConnect_Optimizer_Launcher --> QuantConnect_Logging
    QuantConnect_Optimizer["QuantConnect.Optimizer"]
    QuantConnect_Optimizer_Launcher --> QuantConnect_Optimizer
    QuantConnect_Lean_Launcher["QuantConnect.Lean.Launcher"]
    QuantConnect_Lean_Launcher -.-> QuantConnect_Optimizer_Launcher
```

## Project References
- QuantConnect
- QuantConnect.Configuration
- QuantConnect.Logging
- QuantConnect.Optimizer

## Consumed By
- QuantConnect.Lean.Launcher

## External NuGet Packages
| Package | Version |
|---------|---------||
| Newtonsoft.Json | 13.0.2 |


---

*[Back to Index](../index.md)*
