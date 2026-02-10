# Webhooks.API

## Overview

| Property | Value |
|----------|-------|
| Category | WebApp |
| Repository | src |
| Path | `Webhooks.API/Webhooks.API.csproj` |
| Project References | 3 |
| NuGet Dependencies | 3 |
| Consumers | 1 |

## Dependency Diagram

```mermaid
graph TD
    Webhooks_API["<strong>Webhooks.API</strong>"]
    EventBusRabbitMQ["EventBusRabbitMQ"]
    Webhooks_API --> EventBusRabbitMQ
    IntegrationEventLogEF["IntegrationEventLogEF"]
    Webhooks_API --> IntegrationEventLogEF
    eShop_ServiceDefaults["eShop.ServiceDefaults"]
    Webhooks_API --> eShop_ServiceDefaults
    eShop_AppHost["eShop.AppHost"]
    eShop_AppHost -.-> Webhooks_API
```

## Project References
- EventBusRabbitMQ
- IntegrationEventLogEF
- eShop.ServiceDefaults

## Consumed By
- eShop.AppHost

## External NuGet Packages
| Package | Version |
|---------|---------||
| Asp.Versioning.Http |  |
| Aspire.Npgsql.EntityFrameworkCore.PostgreSQL |  |
| Microsoft.EntityFrameworkCore.Tools |  |

## Data Access Patterns
### DbContext
| File | Line | Context |
|------|------|---------||
| `src/Webhooks.API/Infrastructure/WebhooksContext.cs` | 8 | `public class WebhooksContext(DbContextOptions<WebhooksContext> options` |


---

*[Back to Index](../../index.md)*
