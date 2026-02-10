# QuantConnect.DownloaderDataProvider.Launcher

## Overview

| Property | Value |
|----------|-------|
| Category | Application |
| Repository | Lean |
| Path | `DownloaderDataProvider/QuantConnect.DownloaderDataProvider.Launcher.csproj` |
| Project References | 4 |
| NuGet Dependencies | 0 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    QuantConnect_DownloaderDataProvider_Launcher["<strong>QuantConnect.DownloaderDataProvider.Launcher</strong>"]
    QuantConnect["QuantConnect"]
    QuantConnect_DownloaderDataProvider_Launcher --> QuantConnect
    QuantConnect_Configuration["QuantConnect.Configuration"]
    QuantConnect_DownloaderDataProvider_Launcher --> QuantConnect_Configuration
    QuantConnect_Lean_Engine["QuantConnect.Lean.Engine"]
    QuantConnect_DownloaderDataProvider_Launcher --> QuantConnect_Lean_Engine
    QuantConnect_Logging["QuantConnect.Logging"]
    QuantConnect_DownloaderDataProvider_Launcher --> QuantConnect_Logging
    QuantConnect_Tests["QuantConnect.Tests"]
    QuantConnect_Tests -.-> QuantConnect_DownloaderDataProvider_Launcher
    QuantConnect_Lean_Launcher["QuantConnect.Lean.Launcher"]
    QuantConnect_Lean_Launcher -.-> QuantConnect_DownloaderDataProvider_Launcher
```

## Project References
- QuantConnect
- QuantConnect.Configuration
- QuantConnect.Lean.Engine
- QuantConnect.Logging

## Consumed By
- QuantConnect.Tests
- QuantConnect.Lean.Launcher


---

*[Back to Index](../index.md)*
