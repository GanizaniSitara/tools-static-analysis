# OrchardCore.Media.Indexing.OpenXML

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `OrchardCore.Modules/OrchardCore.Media.Indexing.OpenXML/OrchardCore.Media.Indexing.OpenXML.csproj` |
| Project References | 4 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrchardCore_Media_Indexing_OpenXML["<strong>OrchardCore.Media.Indexing.OpenXML</strong>"]
    OrchardCore_Indexing_Abstractions["OrchardCore.Indexing.Abstractions"]
    OrchardCore_Media_Indexing_OpenXML --> OrchardCore_Indexing_Abstractions
    OrchardCore_Media_Abstractions["OrchardCore.Media.Abstractions"]
    OrchardCore_Media_Indexing_OpenXML --> OrchardCore_Media_Abstractions
    OrchardCore_Module_Targets["OrchardCore.Module.Targets"]
    OrchardCore_Media_Indexing_OpenXML --> OrchardCore_Module_Targets
    OrchardCore_ResourceManagement["OrchardCore.ResourceManagement"]
    OrchardCore_Media_Indexing_OpenXML --> OrchardCore_ResourceManagement
    OrchardCore_Application_Cms_Core_Targets["OrchardCore.Application.Cms.Core.Targets"]
    OrchardCore_Application_Cms_Core_Targets -.-> OrchardCore_Media_Indexing_OpenXML
```

## Project References
- OrchardCore.Indexing.Abstractions
- OrchardCore.Media.Abstractions
- OrchardCore.Module.Targets
- OrchardCore.ResourceManagement

## Consumed By
- OrchardCore.Application.Cms.Core.Targets

## External NuGet Packages
| Package | Version |
|---------|---------||
| DocumentFormat.OpenXml |  |


---

*[Back to Index](../../index.md)*
