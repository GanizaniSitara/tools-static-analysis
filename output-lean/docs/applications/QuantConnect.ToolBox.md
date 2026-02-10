# QuantConnect.ToolBox

## Overview

| Property | Value |
|----------|-------|
| Category | Tool |
| Repository | Lean |
| Path | `ToolBox/QuantConnect.ToolBox.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    QuantConnect_ToolBox["<strong>QuantConnect.ToolBox</strong>"]
    QuantConnect_Lean_Engine["QuantConnect.Lean.Engine"]
    QuantConnect_ToolBox --> QuantConnect_Lean_Engine
    QuantConnect_Tests["QuantConnect.Tests"]
    QuantConnect_Tests -.-> QuantConnect_ToolBox
    QuantConnect_Lean_Launcher["QuantConnect.Lean.Launcher"]
    QuantConnect_Lean_Launcher -.-> QuantConnect_ToolBox
    QuantConnect_Report["QuantConnect.Report"]
    QuantConnect_Report -.-> QuantConnect_ToolBox
```

## Project References
- QuantConnect.Lean.Engine

## Consumed By
- QuantConnect.Tests
- QuantConnect.Lean.Launcher
- QuantConnect.Report


---

*[Back to Index](../index.md)*
