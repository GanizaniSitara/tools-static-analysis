# Localization

## Overview

| Property | Value |
|----------|-------|
| Category | Localization |
| Repository | StockSharp |
| Path | `Localization/Localization.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    Localization["<strong>Localization</strong>"]
    Localization_Generator["Localization.Generator"]
    Localization --> Localization_Generator
    Messages["Messages"]
    Messages -.-> Localization
```

## Project References
- Localization.Generator

## Consumed By
- Messages

## Internal NuGet Packages
| Package | Version |
|---------|---------|
| Ecng.ComponentModel | 1.0.* |


---

*[Back to Index](../index.md)*
