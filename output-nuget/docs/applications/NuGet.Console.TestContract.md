# NuGet.Console.TestContract

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/NuGet.Tests.Apex/NuGet.Console.TestContract/NuGet.Console.TestContract.csproj` |
| Project References | 1 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Console_TestContract["<strong>NuGet.Console.TestContract</strong>"]
    NuGet_Console["NuGet.Console"]
    NuGet_Console_TestContract --> NuGet_Console
    NuGet_Tests_Apex_Daily["NuGet.Tests.Apex.Daily"]
    NuGet_Tests_Apex_Daily -.-> NuGet_Console_TestContract
    NuGet_Tests_Apex["NuGet.Tests.Apex"]
    NuGet_Tests_Apex -.-> NuGet_Console_TestContract
```

## Project References
- NuGet.Console

## Consumed By
- NuGet.Tests.Apex.Daily
- NuGet.Tests.Apex


---

*[Back to Index](../index.md)*
