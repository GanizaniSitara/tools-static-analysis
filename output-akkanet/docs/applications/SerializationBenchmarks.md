# SerializationBenchmarks

## Overview

| Property | Value |
|----------|-------|
| Category | Application |
| Repository | akka.net |
| Path | `src/benchmark/SerializationBenchmarks/SerializationBenchmarks.csproj` |
| Project References | 2 |
| NuGet Dependencies | 1 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    SerializationBenchmarks["<strong>SerializationBenchmarks</strong>"]
    Akka_Serialization_Hyperion["Akka.Serialization.Hyperion"]
    SerializationBenchmarks --> Akka_Serialization_Hyperion
    Akka["Akka"]
    SerializationBenchmarks --> Akka
```

## Project References
- Akka.Serialization.Hyperion
- Akka

## External NuGet Packages
| Package | Version |
|---------|---------||
| BenchmarkDotNet | 0.13.11 |


---

*[Back to Index](../index.md)*
