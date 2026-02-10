# BusinessEntities

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | StockSharp |
| Path | `BusinessEntities/BusinessEntities.csproj` |
| Project References | 1 |
| NuGet Dependencies | 2 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    BusinessEntities["<strong>BusinessEntities</strong>"]
    Messages["Messages"]
    BusinessEntities --> Messages
    Charting_Interfaces["Charting.Interfaces"]
    Charting_Interfaces -.-> BusinessEntities
    Alerts_Interfaces["Alerts.Interfaces"]
    Alerts_Interfaces -.-> BusinessEntities
    02_Misc_Unit_fromsrc["02_Misc.Unit_fromsrc"]
    02_Misc_Unit_fromsrc -.-> BusinessEntities
```

## Project References
- Messages

## Consumed By
- Charting.Interfaces
- Alerts.Interfaces
- 02_Misc.Unit_fromsrc

## Internal NuGet Packages
| Package | Version |
|---------|---------|
| Ecng.Configuration | 1.0.* |
| Ecng.Drawing | 1.0.* |


---

*[Back to Index](../index.md)*
