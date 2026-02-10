# Algo.Indicators

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | StockSharp |
| Path | `Algo.Indicators/Algo.Indicators.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 7 |

## Dependency Diagram

```mermaid
graph TD
    Algo_Indicators["<strong>Algo.Indicators</strong>"]
    Algo["Algo"]
    Algo_Indicators --> Algo
    Diagram_Core["Diagram.Core"]
    Diagram_Core -.-> Algo_Indicators
    Tests["Tests"]
    Tests -.-> Algo_Indicators
    Algo_Export["Algo.Export"]
    Algo_Export -.-> Algo_Indicators
    Algo_Analytics["Algo.Analytics"]
    Algo_Analytics -.-> Algo_Indicators
    Algo_Gpu["Algo.Gpu"]
    Algo_Gpu -.-> Algo_Indicators
    04_Testing_HistoryConsole["04_Testing.HistoryConsole"]
    04_Testing_HistoryConsole -.-> Algo_Indicators
    04_Testing_HistoryConsole_fromsrc["04_Testing.HistoryConsole_fromsrc"]
    04_Testing_HistoryConsole_fromsrc -.-> Algo_Indicators
```

## Project References
- Algo

## Consumed By
- Diagram.Core
- Tests
- Algo.Export
- Algo.Analytics
- Algo.Gpu
- 04_Testing.HistoryConsole
- 04_Testing.HistoryConsole_fromsrc


---

*[Back to Index](../index.md)*
