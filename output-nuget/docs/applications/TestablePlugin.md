# TestablePlugin

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/TestExtensions/TestablePlugin/TestablePlugin.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    TestablePlugin["<strong>TestablePlugin</strong>"]
    NuGet_Protocol["NuGet.Protocol"]
    TestablePlugin --> NuGet_Protocol
    NuGet_Versioning["NuGet.Versioning"]
    TestablePlugin --> NuGet_Versioning
    NuGet_Protocol_FuncTest["NuGet.Protocol.FuncTest"]
    NuGet_Protocol_FuncTest -.-> TestablePlugin
```

## Project References
- NuGet.Protocol
- NuGet.Versioning

## Consumed By
- NuGet.Protocol.FuncTest


---

*[Back to Index](../index.md)*
