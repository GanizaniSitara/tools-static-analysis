# QuantConnect.Algorithm.Framework

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | Lean |
| Path | `Algorithm.Framework/QuantConnect.Algorithm.Framework.csproj` |
| Project References | 3 |
| NuGet Dependencies | 6 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    QuantConnect_Algorithm_Framework["<strong>QuantConnect.Algorithm.Framework</strong>"]
    QuantConnect_Algorithm["QuantConnect.Algorithm"]
    QuantConnect_Algorithm_Framework --> QuantConnect_Algorithm
    QuantConnect["QuantConnect"]
    QuantConnect_Algorithm_Framework --> QuantConnect
    QuantConnect_Indicators["QuantConnect.Indicators"]
    QuantConnect_Algorithm_Framework --> QuantConnect_Indicators
    QuantConnect_Research["QuantConnect.Research"]
    QuantConnect_Research -.-> QuantConnect_Algorithm_Framework
    QuantConnect_Algorithm_CSharp["QuantConnect.Algorithm.CSharp"]
    QuantConnect_Algorithm_CSharp -.-> QuantConnect_Algorithm_Framework
    QuantConnect_Tests["QuantConnect.Tests"]
    QuantConnect_Tests -.-> QuantConnect_Algorithm_Framework
```

## Project References
- QuantConnect.Algorithm
- QuantConnect
- QuantConnect.Indicators

## Consumed By
- QuantConnect.Research
- QuantConnect.Algorithm.CSharp
- QuantConnect.Tests

## External NuGet Packages
| Package | Version |
|---------|---------||
| QuantConnect.pythonnet | 2.0.52 |
| Accord | 3.6.0 |
| Accord.Math | 3.6.0 |
| Accord.Statistics | 3.6.0 |
| MathNet.Numerics | 5.0.0 |
| NodaTime | 3.0.5 |


---

*[Back to Index](../index.md)*
