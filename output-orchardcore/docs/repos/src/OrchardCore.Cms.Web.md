# OrchardCore.Cms.Web

## Overview

| Property | Value |
|----------|-------|
| Category | WebApp |
| Repository | src |
| Path | `OrchardCore.Cms.Web/OrchardCore.Cms.Web.csproj` |
| Project References | 2 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Cms_Web["<strong>OrchardCore.Cms.Web</strong>"]
    OrchardCore_Application_Cms_Targets["OrchardCore.Application.Cms.Targets"]
    OrchardCore_Cms_Web --> OrchardCore_Application_Cms_Targets
    OrchardCore_Logging_NLog["OrchardCore.Logging.NLog"]
    OrchardCore_Cms_Web --> OrchardCore_Logging_NLog
    OrchardCore_Tests["OrchardCore.Tests"]
    OrchardCore_Tests -.-> OrchardCore_Cms_Web
```

## Project References
- OrchardCore.Application.Cms.Targets
- OrchardCore.Logging.NLog

## Consumed By
- OrchardCore.Tests

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.AspNetCore.Mvc.Razor.RuntimeCompilation |  |


---

*[Back to Index](../../index.md)*
