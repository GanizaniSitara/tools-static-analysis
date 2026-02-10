# PaymentProcessor

## Overview

| Property | Value |
|----------|-------|
| Category | WebApp |
| Repository | src |
| Path | `PaymentProcessor/PaymentProcessor.csproj` |
| Project References | 2 |
| NuGet Dependencies | 0 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    PaymentProcessor["<strong>PaymentProcessor</strong>"]
    eShop_ServiceDefaults["eShop.ServiceDefaults"]
    PaymentProcessor --> eShop_ServiceDefaults
    EventBusRabbitMQ["EventBusRabbitMQ"]
    PaymentProcessor --> EventBusRabbitMQ
    eShop_AppHost["eShop.AppHost"]
    eShop_AppHost -.-> PaymentProcessor
```

## Project References
- eShop.ServiceDefaults
- EventBusRabbitMQ

## Consumed By
- eShop.AppHost


---

*[Back to Index](../../index.md)*
