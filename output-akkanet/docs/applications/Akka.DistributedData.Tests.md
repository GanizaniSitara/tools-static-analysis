# Akka.DistributedData.Tests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/contrib/cluster/Akka.DistributedData.Tests/Akka.DistributedData.Tests.csproj` |
| Project References | 4 |
| NuGet Dependencies | 4 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_DistributedData_Tests["<strong>Akka.DistributedData.Tests</strong>"]
    Akka_Cluster_Sharding["Akka.Cluster.Sharding"]
    Akka_DistributedData_Tests --> Akka_Cluster_Sharding
    Akka_DistributedData_LightningDB["Akka.DistributedData.LightningDB"]
    Akka_DistributedData_Tests --> Akka_DistributedData_LightningDB
    Akka_DistributedData["Akka.DistributedData"]
    Akka_DistributedData_Tests --> Akka_DistributedData
    Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    Akka_DistributedData_Tests --> Akka_Tests_Shared_Internals
```

## Project References
- Akka.Cluster.Sharding
- Akka.DistributedData.LightningDB
- Akka.DistributedData
- Akka.Tests.Shared.Internals

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.NET.Test.Sdk | 17.9.0 |
| xunit | 2.8.1 |
| xunit.runner.visualstudio | 2.8.1 |
| FluentAssertions | 5.10.3 |


---

*[Back to Index](../index.md)*
