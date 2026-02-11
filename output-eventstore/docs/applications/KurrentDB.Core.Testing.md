# KurrentDB.Core.Testing

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | src |
| Path | `KurrentDB.Core.Testing/KurrentDB.Core.Testing.csproj` |
| Project References | 2 |
| NuGet Dependencies | 6 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_Core_Testing["<strong>KurrentDB.Core.Testing</strong>"]
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_Core_Testing --> KurrentDB_Core
    KurrentDB_PluginHosting["KurrentDB.PluginHosting"]
    KurrentDB_Core_Testing --> KurrentDB_PluginHosting
    KurrentDB_Core_Testing_NUnit["KurrentDB.Core.Testing.NUnit"]
    KurrentDB_Core_Testing_NUnit -.-> KurrentDB_Core_Testing
    KurrentDB_Projections_Core_XUnit_Tests["KurrentDB.Projections.Core.XUnit.Tests"]
    KurrentDB_Projections_Core_XUnit_Tests -.-> KurrentDB_Core_Testing
    KurrentDB_Auth_StreamPolicyPlugin_Tests["KurrentDB.Auth.StreamPolicyPlugin.Tests"]
    KurrentDB_Auth_StreamPolicyPlugin_Tests -.-> KurrentDB_Core_Testing
    KurrentDB_Core_Testing_XUnit["KurrentDB.Core.Testing.XUnit"]
    KurrentDB_Core_Testing_XUnit -.-> KurrentDB_Core_Testing
    KurrentDB_TcpPlugin_Tests["KurrentDB.TcpPlugin.Tests"]
    KurrentDB_TcpPlugin_Tests -.-> KurrentDB_Core_Testing
```

## Project References
- KurrentDB.Core
- KurrentDB.PluginHosting

## Consumed By
- KurrentDB.Core.Testing.NUnit
- KurrentDB.Projections.Core.XUnit.Tests
- KurrentDB.Auth.StreamPolicyPlugin.Tests
- KurrentDB.Core.Testing.XUnit
- KurrentDB.TcpPlugin.Tests

## External NuGet Packages
| Package | Version |
|---------|---------||
| EventStore.Client |  |
| FluentAssertions |  |
| Microsoft.AspNetCore.TestHost |  |
| Serilog.Sinks.InMemory |  |
| Serilog.AspNetCore |  |
| IgnoresAccessChecksToGenerator |  |


---

*[Back to Index](../index.md)*
