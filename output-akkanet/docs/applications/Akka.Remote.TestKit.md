# Akka.Remote.TestKit

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | akka.net |
| Path | `src/core/Akka.Remote.TestKit/Akka.Remote.TestKit.csproj` |
| Project References | 2 |
| NuGet Dependencies | 3 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Remote_TestKit["<strong>Akka.Remote.TestKit</strong>"]
    Akka_Remote["Akka.Remote"]
    Akka_Remote_TestKit --> Akka_Remote
    Akka_TestKit_Xunit2["Akka.TestKit.Xunit2"]
    Akka_Remote_TestKit --> Akka_TestKit_Xunit2
    Akka_Remote_Tests_MultiNode["Akka.Remote.Tests.MultiNode"]
    Akka_Remote_Tests_MultiNode -.-> Akka_Remote_TestKit
    Akka_Cluster_TestKit["Akka.Cluster.TestKit"]
    Akka_Cluster_TestKit -.-> Akka_Remote_TestKit
    Akka_Remote_TestKit_Tests["Akka.Remote.TestKit.Tests"]
    Akka_Remote_TestKit_Tests -.-> Akka_Remote_TestKit
```

## Project References
- Akka.Remote
- Akka.TestKit.Xunit2

## Consumed By
- Akka.Remote.Tests.MultiNode
- Akka.Cluster.TestKit
- Akka.Remote.TestKit.Tests

## External NuGet Packages
| Package | Version |
|---------|---------||
| Google.Protobuf | 3.26.1 |
| Grpc.Tools | 2.60.0 |
| System.Collections.Specialized | 4.3.0 |


---

*[Back to Index](../index.md)*
