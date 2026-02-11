# KurrentDB.Auth.StreamPolicyPlugin

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `KurrentDB.Auth.StreamPolicyPlugin/KurrentDB.Auth.StreamPolicyPlugin.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    KurrentDB_Auth_StreamPolicyPlugin["<strong>KurrentDB.Auth.StreamPolicyPlugin</strong>"]
    KurrentDB_Core["KurrentDB.Core"]
    KurrentDB_Auth_StreamPolicyPlugin --> KurrentDB_Core
    KurrentDB_Auth_StreamPolicyPlugin_Tests["KurrentDB.Auth.StreamPolicyPlugin.Tests"]
    KurrentDB_Auth_StreamPolicyPlugin_Tests -.-> KurrentDB_Auth_StreamPolicyPlugin
    KurrentDB["KurrentDB"]
    KurrentDB -.-> KurrentDB_Auth_StreamPolicyPlugin
```

## Project References
- KurrentDB.Core

## Consumed By
- KurrentDB.Auth.StreamPolicyPlugin.Tests
- KurrentDB

## External NuGet Packages
| Package | Version |
|---------|---------||
| System.ComponentModel.Composition |  |


---

*[Back to Index](../index.md)*
