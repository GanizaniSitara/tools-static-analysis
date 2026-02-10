# OrderProcessor

## Overview

| Property | Value |
|----------|-------|
| Category | Service |
| Repository | src |
| Path | `OrderProcessor/OrderProcessor.csproj` |
| Project References | 2 |
| NuGet Dependencies | 1 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    OrderProcessor["<strong>OrderProcessor</strong>"]
    eShop_ServiceDefaults["eShop.ServiceDefaults"]
    OrderProcessor --> eShop_ServiceDefaults
    EventBusRabbitMQ["EventBusRabbitMQ"]
    OrderProcessor --> EventBusRabbitMQ
    eShop_AppHost["eShop.AppHost"]
    eShop_AppHost -.-> OrderProcessor
```

## Project References
- eShop.ServiceDefaults
- EventBusRabbitMQ

## Consumed By
- eShop.AppHost

## External NuGet Packages
| Package | Version |
|---------|---------||
| Aspire.Npgsql |  |


---

*[Back to Index](../../index.md)*
