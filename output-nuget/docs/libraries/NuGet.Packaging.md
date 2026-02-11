# NuGet.Packaging

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | NuGet.Client |
| Path | `src/NuGet.Core/NuGet.Packaging/NuGet.Packaging.csproj` |
| Project References | 2 |
| NuGet Dependencies | 3 |
| Consumers | 7 |

## Dependency Diagram

```mermaid
graph TD
    NuGet_Packaging["<strong>NuGet.Packaging</strong>"]
    NuGet_Configuration["NuGet.Configuration"]
    NuGet_Packaging --> NuGet_Configuration
    NuGet_Versioning["NuGet.Versioning"]
    NuGet_Packaging --> NuGet_Versioning
    NuGet_Packaging_FuncTest["NuGet.Packaging.FuncTest"]
    NuGet_Packaging_FuncTest -.-> NuGet_Packaging
    NuGet_Signing_CrossFramework_Test["NuGet.Signing.CrossFramework.Test"]
    NuGet_Signing_CrossFramework_Test -.-> NuGet_Packaging
    NuGet_Frameworks_Test["NuGet.Frameworks.Test"]
    NuGet_Frameworks_Test -.-> NuGet_Packaging
    NuGet_Packaging_Test["NuGet.Packaging.Test"]
    NuGet_Packaging_Test -.-> NuGet_Packaging
    Microsoft_Internal_NuGet_Testing_SignedPackages["Microsoft.Internal.NuGet.Testing.SignedPackages"]
    Microsoft_Internal_NuGet_Testing_SignedPackages -.-> NuGet_Packaging
    NuGet_VisualStudio_Client["NuGet.VisualStudio.Client"]
    NuGet_VisualStudio_Client -.-> NuGet_Packaging
    NuGet_Protocol["NuGet.Protocol"]
    NuGet_Protocol -.-> NuGet_Packaging
```

## Project References
- NuGet.Configuration
- NuGet.Versioning

## Consumed By
- NuGet.Packaging.FuncTest
- NuGet.Signing.CrossFramework.Test
- NuGet.Frameworks.Test
- NuGet.Packaging.Test
- Microsoft.Internal.NuGet.Testing.SignedPackages
- NuGet.VisualStudio.Client
- NuGet.Protocol

## External NuGet Packages
| Package | Version |
|---------|---------||
| Newtonsoft.Json |  |
| System.Text.Json |  |
| System.Security.Cryptography.Pkcs |  |


---

*[Back to Index](../index.md)*
