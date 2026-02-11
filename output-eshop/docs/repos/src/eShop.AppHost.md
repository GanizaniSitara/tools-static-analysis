# eShop.AppHost

## Overview

| Property | Value |
|----------|-------|
| Category | Application |
| Repository | src |
| Path | `eShop.AppHost/eShop.AppHost.csproj` |
| Project References | 9 |
| NuGet Dependencies | 6 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    eShop_AppHost["<strong>eShop.AppHost</strong>"]
    Basket_API["Basket.API"]
    eShop_AppHost --> Basket_API
    Catalog_API["Catalog.API"]
    eShop_AppHost --> Catalog_API
    Identity_API["Identity.API"]
    eShop_AppHost --> Identity_API
    Ordering_API["Ordering.API"]
    eShop_AppHost --> Ordering_API
    OrderProcessor["OrderProcessor"]
    eShop_AppHost --> OrderProcessor
    PaymentProcessor["PaymentProcessor"]
    eShop_AppHost --> PaymentProcessor
    Webhooks_API["Webhooks.API"]
    eShop_AppHost --> Webhooks_API
    WebApp["WebApp"]
    eShop_AppHost --> WebApp
    WebhookClient["WebhookClient"]
    eShop_AppHost --> WebhookClient
```

## Project References
- Basket.API
- Catalog.API
- Identity.API
- Ordering.API
- OrderProcessor
- PaymentProcessor
- Webhooks.API
- WebApp
- WebhookClient

## External NuGet Packages
| Package | Version |
|---------|---------||
| Aspire.Hosting.RabbitMQ |  |
| Aspire.Hosting.Redis |  |
| Aspire.Hosting.PostgreSQL |  |
| Aspire.Hosting.Azure.CognitiveServices |  |
| Aspire.Hosting.Yarp |  |
| CommunityToolkit.Aspire.Hosting.Ollama |  |

## Data Access Patterns
### ConnectionString
| File | Line | Context |
|------|------|---------||
| `src/eShop.AppHost/Extensions.cs` | 125 | `var openAIConnectionString = openAIConnectionBuilder.Build();` |
| `src/eShop.AppHost/Extensions.cs` | 127 | `catalogApi.WithReference(builder.AddConnectionString(textEmbeddingName` |
| `src/eShop.AppHost/Extensions.cs` | 129 | `cs.Append($"{openAIConnectionString};Deployment={embeddingModel}");` |
| `src/eShop.AppHost/Extensions.cs` | 131 | `webApp.WithReference(builder.AddConnectionString(chatName, cs =>` |
| `src/eShop.AppHost/Extensions.cs` | 133 | `cs.Append($"{openAIConnectionString};Deployment={chatModel}");` |


---

*[Back to Index](../../index.md)*
