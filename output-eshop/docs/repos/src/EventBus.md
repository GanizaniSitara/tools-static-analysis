# EventBus

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `EventBus/EventBus.csproj` |
| Project References | 0 |
| NuGet Dependencies | 1 |
| Consumers | 2 |

## Dependency Diagram

```mermaid
graph TD
    EventBus["<strong>EventBus</strong>"]
    IntegrationEventLogEF["IntegrationEventLogEF"]
    IntegrationEventLogEF -.-> EventBus
    EventBusRabbitMQ["EventBusRabbitMQ"]
    EventBusRabbitMQ -.-> EventBus
```

## Consumed By
- IntegrationEventLogEF
- EventBusRabbitMQ

## External NuGet Packages
| Package | Version |
|---------|---------||
| Microsoft.Extensions.Options |  |


---

*[Back to Index](../../index.md)*
