# IntegrationEventLogEF

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | src |
| Path | `IntegrationEventLogEF/IntegrationEventLogEF.csproj` |
| Project References | 1 |
| NuGet Dependencies | 1 |
| Consumers | 4 |

## Dependency Diagram

```mermaid
graph TD
    IntegrationEventLogEF["<strong>IntegrationEventLogEF</strong>"]
    EventBus["EventBus"]
    IntegrationEventLogEF --> EventBus
    Catalog_API["Catalog.API"]
    Catalog_API -.-> IntegrationEventLogEF
    Ordering_Infrastructure["Ordering.Infrastructure"]
    Ordering_Infrastructure -.-> IntegrationEventLogEF
    Ordering_API["Ordering.API"]
    Ordering_API -.-> IntegrationEventLogEF
    Webhooks_API["Webhooks.API"]
    Webhooks_API -.-> IntegrationEventLogEF
```

## Project References
- EventBus

## Consumed By
- Catalog.API
- Ordering.Infrastructure
- Ordering.API
- Webhooks.API

## External NuGet Packages
| Package | Version |
|---------|---------||
| Npgsql.EntityFrameworkCore.PostgreSQL |  |

## Data Access Patterns
### DbContext
| File | Line | Context |
|------|------|---------||
| `src/IntegrationEventLogEF/Services/IntegrationEventLogService.cs` | 4 | `where TContext : DbContext` |


---

*[Back to Index](../../index.md)*
