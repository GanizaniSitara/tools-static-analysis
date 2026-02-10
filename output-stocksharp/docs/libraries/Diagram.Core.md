# Diagram.Core

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | StockSharp |
| Path | `Diagram.Core/Diagram.Core.csproj` |
| Project References | 3 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    Diagram_Core["<strong>Diagram.Core</strong>"]
    Alerts_Interfaces["Alerts.Interfaces"]
    Diagram_Core --> Alerts_Interfaces
    Algo_Strategies["Algo.Strategies"]
    Diagram_Core --> Algo_Strategies
    Algo_Indicators["Algo.Indicators"]
    Diagram_Core --> Algo_Indicators
    Tests["Tests"]
    Tests -.-> Diagram_Core
```

## Project References
- Alerts.Interfaces
- Algo.Strategies
- Algo.Indicators

## Consumed By
- Tests


---

*[Back to Index](../index.md)*
