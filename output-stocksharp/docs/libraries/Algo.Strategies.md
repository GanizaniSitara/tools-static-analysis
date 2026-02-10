# Algo.Strategies

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | StockSharp |
| Path | `Algo.Strategies/Algo.Strategies.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 4 |

## Dependency Diagram

```mermaid
graph TD
    Algo_Strategies["<strong>Algo.Strategies</strong>"]
    Alerts_Interfaces["Alerts.Interfaces"]
    Algo_Strategies --> Alerts_Interfaces
    Algo_Testing["Algo.Testing"]
    Algo_Strategies --> Algo_Testing
    Diagram_Core["Diagram.Core"]
    Diagram_Core -.-> Algo_Strategies
    Tests["Tests"]
    Tests -.-> Algo_Strategies
    04_Testing_HistoryConsole["04_Testing.HistoryConsole"]
    04_Testing_HistoryConsole -.-> Algo_Strategies
    04_Testing_HistoryConsole_fromsrc["04_Testing.HistoryConsole_fromsrc"]
    04_Testing_HistoryConsole_fromsrc -.-> Algo_Strategies
```

## Project References
- Alerts.Interfaces
- Algo.Testing

## Consumed By
- Diagram.Core
- Tests
- 04_Testing.HistoryConsole
- 04_Testing.HistoryConsole_fromsrc


---

*[Back to Index](../index.md)*
