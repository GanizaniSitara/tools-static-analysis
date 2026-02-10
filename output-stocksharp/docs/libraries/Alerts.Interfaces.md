# Alerts.Interfaces

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | StockSharp |
| Path | `Alerts.Interfaces/Alerts.Interfaces.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    Alerts_Interfaces["<strong>Alerts.Interfaces</strong>"]
    BusinessEntities["BusinessEntities"]
    Alerts_Interfaces --> BusinessEntities
    Diagram_Core["Diagram.Core"]
    Diagram_Core -.-> Alerts_Interfaces
    Tests["Tests"]
    Tests -.-> Alerts_Interfaces
    Algo_Strategies["Algo.Strategies"]
    Algo_Strategies -.-> Alerts_Interfaces
```

## Project References
- BusinessEntities

## Consumed By
- Diagram.Core
- Tests
- Algo.Strategies


---

*[Back to Index](../index.md)*
