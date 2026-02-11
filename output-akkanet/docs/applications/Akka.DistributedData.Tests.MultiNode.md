# Akka.DistributedData.Tests.MultiNode

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/contrib/cluster/Akka.DistributedData.Tests.MultiNode/Akka.DistributedData.Tests.MultiNode.csproj` |
| Project References | 4 |
| NuGet Dependencies | 5 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_DistributedData_Tests_MultiNode["<strong>Akka.DistributedData.Tests.MultiNode</strong>"]
    Akka_DistributedData_LightningDB["Akka.DistributedData.LightningDB"]
    Akka_DistributedData_Tests_MultiNode --> Akka_DistributedData_LightningDB
    Akka_DistributedData["Akka.DistributedData"]
    Akka_DistributedData_Tests_MultiNode --> Akka_DistributedData
    Akka_Cluster_TestKit["Akka.Cluster.TestKit"]
    Akka_DistributedData_Tests_MultiNode --> Akka_Cluster_TestKit
    Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    Akka_DistributedData_Tests_MultiNode --> Akka_Tests_Shared_Internals
```

## Project References
- Akka.DistributedData.LightningDB
- Akka.DistributedData
- Akka.Cluster.TestKit
- Akka.Tests.Shared.Internals

## External NuGet Packages
| Package | Version |
|---------|---------||
| Akka.MultiNode.TestAdapter | 1.5.40 |
| Microsoft.NET.Test.Sdk | 17.9.0 |
| FluentAssertions | 5.10.3 |
| xunit | 2.8.1 |
| xunit.runner.visualstudio | 2.8.1 |


---

*[Back to Index](../index.md)*
