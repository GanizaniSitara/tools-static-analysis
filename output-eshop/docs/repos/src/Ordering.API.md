# Ordering.API

## Overview

| Property | Value |
|----------|-------|
| Category | WebApp |
| Repository | src |
| Path | `Ordering.API/Ordering.API.csproj` |
| Project References | 5 |
| NuGet Dependencies | 5 |
| Consumers | 3 |

## Dependency Diagram

```mermaid
graph TD
    Ordering_API["<strong>Ordering.API</strong>"]
    EventBusRabbitMQ["EventBusRabbitMQ"]
    Ordering_API --> EventBusRabbitMQ
    IntegrationEventLogEF["IntegrationEventLogEF"]
    Ordering_API --> IntegrationEventLogEF
    eShop_ServiceDefaults["eShop.ServiceDefaults"]
    Ordering_API --> eShop_ServiceDefaults
    Ordering_Domain["Ordering.Domain"]
    Ordering_API --> Ordering_Domain
    Ordering_Infrastructure["Ordering.Infrastructure"]
    Ordering_API --> Ordering_Infrastructure
    eShop_AppHost["eShop.AppHost"]
    eShop_AppHost -.-> Ordering_API
    Ordering_UnitTests["Ordering.UnitTests"]
    Ordering_UnitTests -.-> Ordering_API
    Ordering_FunctionalTests["Ordering.FunctionalTests"]
    Ordering_FunctionalTests -.-> Ordering_API
```

## Project References
- EventBusRabbitMQ
- IntegrationEventLogEF
- eShop.ServiceDefaults
- Ordering.Domain
- Ordering.Infrastructure

## Consumed By
- eShop.AppHost
- Ordering.UnitTests
- Ordering.FunctionalTests

## External NuGet Packages
| Package | Version |
|---------|---------||
| Asp.Versioning.Http |  |
| Aspire.Npgsql.EntityFrameworkCore.PostgreSQL |  |
| FluentValidation |  |
| FluentValidation.DependencyInjectionExtensions |  |
| Microsoft.EntityFrameworkCore.Tools |  |

## Data Access Patterns
### ConnectionString
| File | Line | Context |
|------|------|---------||
| `src/Ordering.API/Extensions/Extensions.cs` | 17 | `options.UseNpgsql(builder.Configuration.GetConnectionString("orderingd` |

### EntityFramework
| File | Line | Context |
|------|------|---------||
| `src/Ordering.API/Extensions/Extensions.cs` | 17 | `options.UseNpgsql(builder.Configuration.GetConnectionString("orderingd` |


---

*[Back to Index](../../index.md)*
