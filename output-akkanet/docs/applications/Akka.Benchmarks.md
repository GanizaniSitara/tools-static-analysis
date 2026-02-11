# Akka.Benchmarks

## Overview

| Property | Value |
|----------|-------|
| Category | Application |
| Repository | akka.net |
| Path | `src/benchmark/Akka.Benchmarks/Akka.Benchmarks.csproj` |
| Project References | 7 |
| NuGet Dependencies | 2 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Akka_Benchmarks["<strong>Akka.Benchmarks</strong>"]
    Akka_DistributedData["Akka.DistributedData"]
    Akka_Benchmarks --> Akka_DistributedData
    Akka_Serialization_Hyperion["Akka.Serialization.Hyperion"]
    Akka_Benchmarks --> Akka_Serialization_Hyperion
    Akka_Cluster["Akka.Cluster"]
    Akka_Benchmarks --> Akka_Cluster
    Akka_Persistence["Akka.Persistence"]
    Akka_Benchmarks --> Akka_Persistence
    Akka_Remote["Akka.Remote"]
    Akka_Benchmarks --> Akka_Remote
    Akka_Streams["Akka.Streams"]
    Akka_Benchmarks --> Akka_Streams
    Akka["Akka"]
    Akka_Benchmarks --> Akka
```

## Project References
- Akka.DistributedData
- Akka.Serialization.Hyperion
- Akka.Cluster
- Akka.Persistence
- Akka.Remote
- Akka.Streams
- Akka

## External NuGet Packages
| Package | Version |
|---------|---------||
| BenchmarkDotNet | 0.15.4 |
| FluentAssertions | 5.10.3 |


---

*[Back to Index](../index.md)*
