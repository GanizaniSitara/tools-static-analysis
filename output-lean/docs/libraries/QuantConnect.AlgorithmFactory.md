# QuantConnect.AlgorithmFactory

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | Lean |
| Path | `AlgorithmFactory/QuantConnect.AlgorithmFactory.csproj` |
| Project References | 4 |
| NuGet Dependencies | 2 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    QuantConnect_AlgorithmFactory["<strong>QuantConnect.AlgorithmFactory</strong>"]
    QuantConnect_Algorithm["QuantConnect.Algorithm"]
    QuantConnect_AlgorithmFactory --> QuantConnect_Algorithm
    QuantConnect["QuantConnect"]
    QuantConnect_AlgorithmFactory --> QuantConnect
    QuantConnect_Configuration["QuantConnect.Configuration"]
    QuantConnect_AlgorithmFactory --> QuantConnect_Configuration
    QuantConnect_Logging["QuantConnect.Logging"]
    QuantConnect_AlgorithmFactory --> QuantConnect_Logging
    QuantConnect_Lean_Engine["QuantConnect.Lean.Engine"]
    QuantConnect_Lean_Engine -.-> QuantConnect_AlgorithmFactory
    QuantConnect_Tests["QuantConnect.Tests"]
    QuantConnect_Tests -.-> QuantConnect_AlgorithmFactory
    QuantConnect_Lean_Launcher["QuantConnect.Lean.Launcher"]
    QuantConnect_Lean_Launcher -.-> QuantConnect_AlgorithmFactory
```

## Project References
- QuantConnect.Algorithm
- QuantConnect
- QuantConnect.Configuration
- QuantConnect.Logging

## Consumed By
- QuantConnect.Lean.Engine
- QuantConnect.Tests
- QuantConnect.Lean.Launcher

## External NuGet Packages
| Package | Version |
|---------|---------||
| QuantConnect.pythonnet | 2.0.52 |
| NodaTime | 3.0.5 |


---

*[Back to Index](../index.md)*
