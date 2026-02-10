# QuantConnect.Compression

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | Lean |
| Path | `Compression/QuantConnect.Compression.csproj` |
| Project References | 1 |
| NuGet Dependencies | 2 |
| Consumers | 5 |

## Dependency Diagram

```mermaid
graph TD
    QuantConnect_Compression["<strong>QuantConnect.Compression</strong>"]
    QuantConnect_Logging["QuantConnect.Logging"]
    QuantConnect_Compression --> QuantConnect_Logging
    QuantConnect_Brokerages["QuantConnect.Brokerages"]
    QuantConnect_Brokerages -.-> QuantConnect_Compression
    QuantConnect_Lean_Engine["QuantConnect.Lean.Engine"]
    QuantConnect_Lean_Engine -.-> QuantConnect_Compression
    QuantConnect["QuantConnect"]
    QuantConnect -.-> QuantConnect_Compression
    QuantConnect_Tests["QuantConnect.Tests"]
    QuantConnect_Tests -.-> QuantConnect_Compression
    QuantConnect_Lean_Launcher["QuantConnect.Lean.Launcher"]
    QuantConnect_Lean_Launcher -.-> QuantConnect_Compression
```

## Project References
- QuantConnect.Logging

## Consumed By
- QuantConnect.Brokerages
- QuantConnect.Lean.Engine
- QuantConnect
- QuantConnect.Tests
- QuantConnect.Lean.Launcher

## External NuGet Packages
| Package | Version |
|---------|---------||
| DotNetZip | 1.16.0 |
| SharpZipLib | 1.3.3 |


---

*[Back to Index](../index.md)*
