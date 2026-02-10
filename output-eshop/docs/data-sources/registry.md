# Data Source Registry

## Summary

| Type | Occurrences |
|------|-------------|
| messaging | 29 |
| database | 17 |
| config | 14 |
| api | 11 |
| pattern | 4 |
| cache | 2 |

## Connection Strings Found

| File | Repo | Connection Name | Value |
|------|------|----------------|-------|
| `src/Identity.API/appsettings.Development.json` | src | IdentityDB | `Host=localhost;Database=IdentityDB;Username=postgres;Password=yourWeak(!)Passwor` |
| `src/Catalog.API/appsettings.Development.json` | src | CatalogDB | `Host=localhost;Database=CatalogDB;Username=postgres;Password=yourWeak(!)Password` |
| `src/OrderProcessor/appsettings.Development.json` | src | postgres | `Host=localhost;Database=OrderingDB;Username=postgres;Password=yourWeak(!)Passwor` |
| `src/OrderProcessor/appsettings.json` | src | EventBus | `amqp://localhost` |
| `src/Basket.API/appsettings.json` | src | Redis | `localhost` |
| `src/Basket.API/appsettings.json` | src | EventBus | `amqp://localhost` |
| `src/Ordering.API/appsettings.Development.json` | src | OrderingDB | `Host=localhost;Database=OrderingDB;Username=postgres;Password=yourWeak(!)Passwor` |
| `src/Webhooks.API/appsettings.Development.json` | src | WebHooksDB | `Host=localhost;Database=WebHooksDB;Username=postgres;Password=yourWeak(!)Passwor` |
| `src/Webhooks.API/appsettings.json` | src | EventBus | `amqp://localhost` |

## Messaging

### RabbitMQ (29 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/eShop.AppHost/Program.cs` | 8 | `var rabbitMq = builder.AddRabbitMQ("eventbus")` |
| src | `src/EventBusRabbitMQ/GlobalUsings.cs` | 8 | `global using RabbitMQ.Client;` |
| src | `src/EventBusRabbitMQ/GlobalUsings.cs` | 9 | `global using RabbitMQ.Client.Events;` |
| src | `src/EventBusRabbitMQ/GlobalUsings.cs` | 10 | `global using RabbitMQ.Client.Exceptions;` |
| src | `src/EventBusRabbitMQ/EventBusOptions.cs` | 1 | `﻿namespace eShop.EventBusRabbitMQ;` |
| src | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | 1 | `﻿namespace eShop.EventBusRabbitMQ;` |
| src | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | 13 | `public sealed class RabbitMQEventBus(` |
| src | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | 14 | `ILogger<RabbitMQEventBus> logger,` |
| src | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | 18 | `RabbitMQTelemetry rabbitMQTelemetry) : IEventBus, IDisposabl` |
| src | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | 37 | `logger.LogTrace("Creating RabbitMQ channel to publish event:` |
| src | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | 40 | `using var channel = (await _rabbitMQConnection?.CreateChanne` |
| src | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | 44 | `logger.LogTrace("Declaring RabbitMQ exchange to publish even` |
| src | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | 92 | `logger.LogTrace("Publishing event to RabbitMQ: {EventId}", @` |
| src | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | 187 | `logger.LogTrace("Processing RabbitMQ event: {EventName}", ev` |
| src | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | 233 | `logger.LogInformation("Starting RabbitMQ connection on a bac` |
| src | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | 243 | `logger.LogTrace("Creating RabbitMQ consumer channel");` |
| src | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | 250 | `logger.LogWarning(ea.Exception, "Error with RabbitMQ consume` |
| src | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | 267 | `logger.LogTrace("Starting RabbitMQ basic consume");` |
| src | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | 289 | `logger.LogError(ex, "Error starting RabbitMQ connection");` |
| src | `src/EventBusRabbitMQ/RabbitMqDependencyInjectionExtensions.cs` | 1 | `﻿using eShop.EventBusRabbitMQ;` |
| src | `src/EventBusRabbitMQ/RabbitMqDependencyInjectionExtensions.cs` | 21 | `builder.AddRabbitMQClient(connectionName);` |
| src | `src/EventBusRabbitMQ/RabbitMqDependencyInjectionExtensions.cs` | 23 | `// RabbitMQ.Client doesn't have built-in support for OpenTel` |
| src | `src/EventBusRabbitMQ/RabbitMqDependencyInjectionExtensions.cs` | 27 | `tracing.AddSource(RabbitMQTelemetry.ActivitySourceName);` |
| src | `src/EventBusRabbitMQ/RabbitMqDependencyInjectionExtensions.cs` | 34 | `builder.Services.AddSingleton<RabbitMQTelemetry>();` |
| src | `src/EventBusRabbitMQ/RabbitMqDependencyInjectionExtensions.cs` | 35 | `builder.Services.AddSingleton<IEventBus, RabbitMQEventBus>()` |

*... and 4 more*

**Repos:** src

## Database

### DbContext (11 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Catalog.API/Infrastructure/CatalogContext.cs` | 8 | `public class CatalogContext : DbContext` |
| src | `src/Ordering.Infrastructure/OrderingContext.cs` | 10 | `public class OrderingContext : DbContext, IUnitOfWork` |
| src | `src/IntegrationEventLogEF/Services/IntegrationEventLogService.cs` | 4 | `where TContext : DbContext` |
| src | `src/Webhooks.API/Infrastructure/WebhooksContext.cs` | 8 | `public class WebhooksContext(DbContextOptions<WebhooksContex` |
| src | `src/Shared/MigrateDbContextExtensions.cs` | 11 | `where TContext : DbContext` |
| src | `src/Shared/MigrateDbContextExtensions.cs` | 15 | `where TContext : DbContext` |
| src | `src/Shared/MigrateDbContextExtensions.cs` | 24 | `where TContext : DbContext` |
| src | `src/Shared/MigrateDbContextExtensions.cs` | 31 | `private static async Task MigrateDbContextAsync<TContext>(th` |
| src | `src/Shared/MigrateDbContextExtensions.cs` | 59 | `where TContext : DbContext` |
| src | `src/Shared/MigrateDbContextExtensions.cs` | 77 | `: BackgroundService where TContext : DbContext` |
| src | `src/Shared/MigrateDbContextExtensions.cs` | 90 | `public interface IDbSeeder<in TContext> where TContext : DbC` |

**Repos:** src

### Dapper (4 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | 57 | `await _pipeline.Execute(async () =>` |
| src | `src/ClientApp/Views/ProfileView.xaml.cs` | 20 | `_viewModel.RefreshCommand.Execute(null);` |
| src | `src/ClientApp/Controls/ToggleButton.cs` | 77 | `Command.Execute(CommandParameter);` |
| tests | `tests/ClientApp.UnitTests/TestingExtensions.cs` | 16 | `command.Execute(parameter);` |

**Repos:** src, tests

### EntityFramework (2 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Catalog.API/Extensions/Extensions.cs` | 17 | `dbContextOptionsBuilder.UseNpgsql(builder =>` |
| src | `src/Ordering.API/Extensions/Extensions.cs` | 17 | `options.UseNpgsql(builder.Configuration.GetConnectionString(` |

**Repos:** src

## Config

### ConnectionString (14 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/WebApp/Extensions/Extensions.cs` | 102 | `else if (!string.IsNullOrWhiteSpace(builder.Configuration.Ge` |
| src | `src/Catalog.API/Extensions/Extensions.cs` | 43 | `else if (!string.IsNullOrWhiteSpace(builder.Configuration.Ge` |
| src | `src/eShop.AppHost/Extensions.cs` | 125 | `var openAIConnectionString = openAIConnectionBuilder.Build()` |
| src | `src/eShop.AppHost/Extensions.cs` | 127 | `catalogApi.WithReference(builder.AddConnectionString(textEmb` |
| src | `src/eShop.AppHost/Extensions.cs` | 129 | `cs.Append($"{openAIConnectionString};Deployment={embeddingMo` |
| src | `src/eShop.AppHost/Extensions.cs` | 131 | `webApp.WithReference(builder.AddConnectionString(chatName, c` |
| src | `src/eShop.AppHost/Extensions.cs` | 133 | `cs.Append($"{openAIConnectionString};Deployment={chatModel}"` |
| src | `src/Ordering.API/Extensions/Extensions.cs` | 17 | `options.UseNpgsql(builder.Configuration.GetConnectionString(` |
| tests | `tests/Ordering.FunctionalTests/OrderingApiFixture.cs` | 17 | `private string _postgresConnectionString;` |
| tests | `tests/Ordering.FunctionalTests/OrderingApiFixture.cs` | 35 | `{ $"ConnectionStrings:{Postgres.Resource.Name}", _postgresCo` |
| tests | `tests/Ordering.FunctionalTests/OrderingApiFixture.cs` | 63 | `_postgresConnectionString = await Postgres.Resource.GetConne` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiFixture.cs` | 15 | `private string _postgresConnectionString;` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiFixture.cs` | 33 | `{ $"ConnectionStrings:{Postgres.Resource.Name}", _postgresCo` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiFixture.cs` | 56 | `_postgresConnectionString = await Postgres.Resource.GetConne` |

**Repos:** src, tests

## Api

### gRPC (6 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/WebApp/Components/Chatbot/ChatState.cs` | 145 | `catch (Grpc.Core.RpcException e) when (e.StatusCode == Grpc.` |
| src | `src/Basket.API/GlobalUsings.cs` | 4 | `global using Grpc.Core;` |
| src | `src/ClientApp/Services/Basket/Protos/BasketGrpc.cs` | 8 | `using grpc = global::Grpc.Core;` |
| src | `src/ClientApp/Services/Basket/BasketService.cs` | 7 | `using Grpc.Core;` |
| src | `src/ClientApp/Services/Basket/BasketService.cs` | 8 | `using Grpc.Net.Client;` |
| tests | `tests/Basket.UnitTests/Helpers/TestServerCallContext.cs` | 1 | `﻿using Grpc.Core;` |

**Repos:** src, tests

### HttpClient.Injection (4 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/WebApp/Extensions/Extensions.cs` | 34 | `builder.Services.AddHttpClient<CatalogService>(o => o.BaseAd` |
| src | `src/WebApp/Extensions/Extensions.cs` | 38 | `builder.Services.AddHttpClient<OrderingService>(o => o.BaseA` |
| src | `src/HybridApp/MauiProgram.cs` | 30 | `builder.Services.AddHttpClient<CatalogService>(o => o.BaseAd` |
| src | `src/WebhookClient/Extensions/Extensions.cs` | 19 | `builder.Services.AddHttpClient<WebhooksClient>(o => o.BaseAd` |

**Repos:** src

### HttpClient.New (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/ClientApp/Services/RequestProvider/RequestProvider.cs` | 15 | `var httpClient = _messageHandler is not null ? new HttpClien` |

**Repos:** src

## Pattern

### Repository (4 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Ordering.Infrastructure/Repositories/BuyerRepository.cs` | 3 | `public class BuyerRepository` |
| src | `src/Ordering.Infrastructure/Repositories/OrderRepository.cs` | 3 | `public class OrderRepository` |
| src | `src/Basket.API/Repositories/RedisBasketRepository.cs` | 6 | `public class RedisBasketRepository(ILogger<RedisBasketReposi` |
| src | `src/WebhookClient/Services/HooksRepository.cs` | 5 | `public class HooksRepository` |

**Repos:** src

## Cache

### Redis (2 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Basket.API/GlobalUsings.cs` | 11 | `global using StackExchange.Redis;` |
| src | `src/Basket.API/Repositories/RedisBasketRepository.cs` | 6 | `public class RedisBasketRepository(ILogger<RedisBasketReposi` |

**Repos:** src


---

*[Back to Index](../index.md)*
