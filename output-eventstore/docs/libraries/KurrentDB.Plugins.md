# KurrentDB.Plugins

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `KurrentDB.Plugins/KurrentDB.Plugins.csproj` |
| Project References | 0 |
| NuGet Dependencies | 3 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_Plugins["<strong>KurrentDB.Plugins</strong>"]
    KurrentDB_Plugins_Tests["KurrentDB.Plugins.Tests"]
    KurrentDB_Plugins_Tests -.-> KurrentDB_Plugins
    KurrentDB_Plugins_TestHelpers["KurrentDB.Plugins.TestHelpers"]
    KurrentDB_Plugins_TestHelpers -.-> KurrentDB_Plugins
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_Core -.-> KurrentDB_Plugins
```

## Consumed By
- KurrentDB.Plugins.Tests
- KurrentDB.Plugins.TestHelpers
- KurrentDB.Core

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.IdentityModel.JsonWebTokens |  |
| YamlDotNet |  |
| System.Reactive |  |


---

*[Back to Index](../index.md)*
