# QuantConnect.Algorithm.CSharp

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | Lean |
| Path | `Algorithm.CSharp/QuantConnect.Algorithm.CSharp.csproj` |
| Project References | 4 |
| NuGet Dependencies | 10 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    QuantConnect_Algorithm_CSharp["<strong>QuantConnect.Algorithm.CSharp</strong>"]
    QuantConnect_Algorithm_Framework["QuantConnect.Algorithm.Framework"]
    QuantConnect_Algorithm_CSharp --> QuantConnect_Algorithm_Framework
    QuantConnect_Algorithm["QuantConnect.Algorithm"]
    QuantConnect_Algorithm_CSharp --> QuantConnect_Algorithm
    QuantConnect["QuantConnect"]
    QuantConnect_Algorithm_CSharp --> QuantConnect
    QuantConnect_Indicators["QuantConnect.Indicators"]
    QuantConnect_Algorithm_CSharp --> QuantConnect_Indicators
    QuantConnect_Lean_Engine["QuantConnect.Lean.Engine"]
    QuantConnect_Lean_Engine -.-> QuantConnect_Algorithm_CSharp
    QuantConnect_Tests["QuantConnect.Tests"]
    QuantConnect_Tests -.-> QuantConnect_Algorithm_CSharp
    QuantConnect_Lean_Launcher["QuantConnect.Lean.Launcher"]
    QuantConnect_Lean_Launcher -.-> QuantConnect_Algorithm_CSharp
```

## Project References
- QuantConnect.Algorithm.Framework
- QuantConnect.Algorithm
- QuantConnect
- QuantConnect.Indicators

## Consumed By
- QuantConnect.Lean.Engine
- QuantConnect.Tests
- QuantConnect.Lean.Launcher

## External NuGet Packages
| Package | Version |
|---------|---------||
| QuantConnect.pythonnet | 2.0.52 |
| Accord | 3.6.0 |
| Accord.Fuzzy | 3.6.0 |
| Accord.MachineLearning | 3.6.0 |
| Accord.Math | 3.6.0 |
| Accord.Statistics | 3.6.0 |
| DynamicInterop | 0.9.1 |
| MathNet.Numerics | 5.0.0 |
| Newtonsoft.Json | 13.0.2 |
| NodaTime | 3.0.5 |


---

*[Back to Index](../index.md)*
