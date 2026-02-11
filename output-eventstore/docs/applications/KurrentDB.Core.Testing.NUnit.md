# KurrentDB.Core.Testing.NUnit

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | src |
| Path | `KurrentDB.Core.Testing.NUnit/KurrentDB.Core.Testing.NUnit.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_Core_Testing_NUnit["<strong>KurrentDB.Core.Testing.NUnit</strong>"]
    KurrentDB_Core_Testing["KurrentDB.Core.Testing"]
    KurrentDB_Core_Testing_NUnit --> KurrentDB_Core_Testing
    KurrentDB_Core_Tests["KurrentDB.Core.Tests"]
    KurrentDB_Core_Tests -.-> KurrentDB_Core_Testing_NUnit
    KurrentDB_Projections_Core_Tests["KurrentDB.Projections.Core.Tests"]
    KurrentDB_Projections_Core_Tests -.-> KurrentDB_Core_Testing_NUnit
```

## Project References
- KurrentDB.Core.Testing

## Consumed By
- KurrentDB.Core.Tests
- KurrentDB.Projections.Core.Tests


---

*[Back to Index](../index.md)*
