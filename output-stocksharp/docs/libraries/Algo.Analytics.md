# Algo.Analytics

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | StockSharp |
| Path | `Algo.Analytics/Algo.Analytics.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    Algo_Analytics["<strong>Algo.Analytics</strong>"]
    Algo_Indicators["Algo.Indicators"]
    Algo_Analytics --> Algo_Indicators
    Algo_Analytics_CSharp["Algo.Analytics.CSharp"]
    Algo_Analytics_CSharp -.-> Algo_Analytics
    Tests["Tests"]
    Tests -.-> Algo_Analytics
```

## Project References
- Algo.Indicators

## Consumed By
- Algo.Analytics.CSharp
- Tests


---

*[Back to Index](../index.md)*
