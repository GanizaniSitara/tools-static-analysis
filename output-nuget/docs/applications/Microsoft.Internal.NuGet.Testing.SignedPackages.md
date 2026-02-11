# Microsoft.Internal.NuGet.Testing.SignedPackages

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | NuGet.Client |
| Path | `test/TestUtilities/Microsoft.Internal.NuGet.Testing.SignedPackages/Microsoft.Internal.NuGet.Testing.SignedPackages.csproj` |
| Project References | 1 |
| NuGet Dependencies | 2 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    Microsoft_Internal_NuGet_Testing_SignedPackages["<strong>Microsoft.Internal.NuGet.Testing.SignedPackages</strong>"]
    NuGet_Packaging["NuGet.Packaging"]
    Microsoft_Internal_NuGet_Testing_SignedPackages --> NuGet_Packaging
    Test_Utility["Test.Utility"]
    Test_Utility -.-> Microsoft_Internal_NuGet_Testing_SignedPackages
    VisualStudio_Test_Utility["VisualStudio.Test.Utility"]
    VisualStudio_Test_Utility -.-> Microsoft_Internal_NuGet_Testing_SignedPackages
```

## Project References
- NuGet.Packaging

## Consumed By
- Test.Utility
- VisualStudio.Test.Utility

## External NuGet Packages
| Package | Version |
|---------|---------||
| System.Formats.Asn1 |  |
| xunit |  |


---

*[Back to Index](../index.md)*
