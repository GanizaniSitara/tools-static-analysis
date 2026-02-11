# Data Source Registry

## Summary

| Type | Occurrences |
|------|-------------|
| api | 128 |
| cache | 77 |
| database | 39 |
| ui | 15 |
| config | 14 |
| pattern | 4 |
| messaging | 4 |
| storage | 1 |

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

## Api

### HttpClient.GetAsync (23 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| tests | `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 30 | `var response = await _httpClient.GetAsync("api/orders", Test` |
| tests | `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 101 | `var response = await _httpClient.GetAsync("api/orders/cardty` |
| tests | `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 113 | `var response = await _httpClient.GetAsync("api/orders/1", Te` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 34 | `var response = await _httpClient.GetAsync("/api/catalog/item` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 55 | `var response = await _httpClient.GetAsync("/api/catalog/item` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 72 | `response = await _httpClient.GetAsync("/api/catalog/items/1"` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 90 | `var response = await _httpClient.GetAsync("/api/catalog/item` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 108 | `response = await _httpClient.GetAsync("/api/catalog/items/1"` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 127 | `var response = await _httpClient.GetAsync("/api/catalog/item` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 146 | `var response = await _httpClient.GetAsync("/api/catalog/item` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 168 | `1.0 => await _httpClient.GetAsync("api/catalog/items/by/Wand` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 169 | `2.0 => await _httpClient.GetAsync("api/catalog/items?name=Wa` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 196 | `1.0 => await _httpClient.GetAsync("api/catalog/items/by/Alpi` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 197 | `2.0 => await _httpClient.GetAsync("api/catalog/items?name=Al` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 222 | `var response = await _httpClient.GetAsync("api/catalog/items` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 242 | `1.0 => await _httpClient.GetAsync("api/catalog/items/withsem` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 243 | `2.0 => await _httpClient.GetAsync("api/catalog/items/withsem` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 269 | `1.0 => await _httpClient.GetAsync("api/catalog/items/type/3/` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 270 | `2.0 => await _httpClient.GetAsync("api/catalog/items?type=3&` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 298 | `1.0 => await _httpClient.GetAsync("api/catalog/items/type/al` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 299 | `2.0 => await _httpClient.GetAsync("api/catalog/items?brand=3` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 324 | `var response = await _httpClient.GetAsync("api/catalog/catal` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 344 | `var response = await _httpClient.GetAsync("api/catalog/catal` |

**Repos:** tests

### API.MapGet (18 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 21 | `v1.MapGet("/items", GetAllItemsV1)` |
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 26 | `v2.MapGet("/items", GetAllItems)` |
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 31 | `api.MapGet("/items/by", GetItemsByIds)` |
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 36 | `api.MapGet("/items/{id:int}", GetItemById)` |
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 41 | `v1.MapGet("/items/by/{name:minlength(1)}", GetItemsByName)` |
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 46 | `api.MapGet("/items/{id:int}/pic", GetItemPictureById)` |
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 53 | `v1.MapGet("/items/withsemanticrelevance/{text:minlength(1)}"` |
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 60 | `v2.MapGet("/items/withsemanticrelevance", GetItemsBySemantic` |
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 67 | `v1.MapGet("/items/type/{typeId}/brand/{brandId?}", GetItemsB` |
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 72 | `v1.MapGet("/items/type/all/brand/{brandId:int?}", GetItemsBy` |
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 77 | `api.MapGet("/catalogtypes",` |
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 84 | `api.MapGet("/catalogbrands",` |
| src | `src/Ordering.API/Apis/OrdersApi.cs` | 13 | `api.MapGet("{orderId:int}", GetOrderAsync);` |
| src | `src/Ordering.API/Apis/OrdersApi.cs` | 14 | `api.MapGet("/", GetOrdersByUserAsync);` |
| src | `src/Ordering.API/Apis/OrdersApi.cs` | 15 | `api.MapGet("/cardtypes", GetCardTypesAsync);` |
| src | `src/eShop.ServiceDefaults/OpenApi.Extensions.cs` | 33 | `app.MapGet("/", () => Results.Redirect("/scalar/v1")).Exclud` |
| src | `src/Webhooks.API/Apis/WebHooksApi.cs` | 13 | `api.MapGet("/", async (WebhooksContext context, ClaimsPrinci` |
| src | `src/Webhooks.API/Apis/WebHooksApi.cs` | 20 | `api.MapGet("/{id:int}", async Task<Results<Ok<WebhookSubscri` |

**Repos:** src

### gRPC (17 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/WebApp/Components/Chatbot/ChatState.cs` | 145 | `catch (Grpc.Core.RpcException e) when (e.StatusCode == Grpc.` |
| src | `src/Basket.API/GlobalUsings.cs` | 4 | `global using Grpc.Core;` |
| src | `src/ClientApp/Services/Basket/Protos/Basket.cs` | 8 | `using pb = global::Google.Protobuf;` |
| src | `src/ClientApp/Services/Basket/Protos/Basket.cs` | 9 | `using pbc = global::Google.Protobuf.Collections;` |
| src | `src/ClientApp/Services/Basket/Protos/Basket.cs` | 10 | `using pbr = global::Google.Protobuf.Reflection;` |
| src | `src/ClientApp/Services/Basket/Protos/BasketGrpc.cs` | 8 | `using grpc = global::Grpc.Core;` |
| src | `src/ClientApp/Services/Basket/Protos/BasketGrpc.cs` | 16 | `static void __Helper_SerializeMessage(global::Google.Protobu` |
| src | `src/ClientApp/Services/Basket/Protos/BasketGrpc.cs` | 19 | `if (message is global::Google.Protobuf.IBufferMessage)` |
| src | `src/ClientApp/Services/Basket/Protos/BasketGrpc.cs` | 22 | `global::Google.Protobuf.MessageExtensions.WriteTo(message, c` |
| src | `src/ClientApp/Services/Basket/Protos/BasketGrpc.cs` | 27 | `context.Complete(global::Google.Protobuf.MessageExtensions.T` |
| src | `src/ClientApp/Services/Basket/Protos/BasketGrpc.cs` | 33 | `public static readonly bool IsBufferMessage = global::System` |
| src | `src/ClientApp/Services/Basket/Protos/BasketGrpc.cs` | 37 | `static T __Helper_DeserializeMessage<T>(grpc::Deserializatio` |
| src | `src/ClientApp/Services/Basket/Protos/BasketGrpc.cs` | 84 | `public static global::Google.Protobuf.Reflection.ServiceDesc` |
| src | `src/ClientApp/Services/Basket/BasketService.cs` | 6 | `using Google.Protobuf;` |
| src | `src/ClientApp/Services/Basket/BasketService.cs` | 7 | `using Grpc.Core;` |
| src | `src/ClientApp/Services/Basket/BasketService.cs` | 8 | `using Grpc.Net.Client;` |
| tests | `tests/Basket.UnitTests/Helpers/TestServerCallContext.cs` | 1 | `﻿using Grpc.Core;` |

**Repos:** src, tests

### gRPC.Server (14 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Basket.API/Program.cs` | 12 | `app.MapGrpcService<BasketService>();` |
| src | `src/Basket.API/Grpc/BasketService.cs` | 13 | `public override async Task<CustomerBasketResponse> GetBasket` |
| src | `src/Basket.API/Grpc/BasketService.cs` | 36 | `public override async Task<CustomerBasketResponse> UpdateBas` |
| src | `src/Basket.API/Grpc/BasketService.cs` | 59 | `public override async Task<DeleteBasketResponse> DeleteBaske` |
| src | `src/Basket.API/Extensions/ServerCallContextIdentityExtensions.cs` | 5 | `internal static class ServerCallContextIdentityExtensions` |
| src | `src/Basket.API/Extensions/ServerCallContextIdentityExtensions.cs` | 7 | `public static string? GetUserIdentity(this ServerCallContext` |
| src | `src/Basket.API/Extensions/ServerCallContextIdentityExtensions.cs` | 8 | `public static string? GetUserName(this ServerCallContext con` |
| tests | `tests/Basket.UnitTests/BasketServiceTests.cs` | 21 | `var serverCallContext = TestServerCallContext.Create(cancell` |
| tests | `tests/Basket.UnitTests/BasketServiceTests.cs` | 37 | `var serverCallContext = TestServerCallContext.Create(cancell` |
| tests | `tests/Basket.UnitTests/BasketServiceTests.cs` | 55 | `var serverCallContext = TestServerCallContext.Create(cancell` |
| tests | `tests/Basket.UnitTests/Helpers/TestServerCallContext.cs` | 5 | `public class TestServerCallContext : ServerCallContext` |
| tests | `tests/Basket.UnitTests/Helpers/TestServerCallContext.cs` | 16 | `private TestServerCallContext(Metadata requestHeaders, Cance` |
| tests | `tests/Basket.UnitTests/Helpers/TestServerCallContext.cs` | 57 | `public static TestServerCallContext Create(Metadata requestH` |
| tests | `tests/Basket.UnitTests/Helpers/TestServerCallContext.cs` | 59 | `return new TestServerCallContext(requestHeaders: new Metadat` |

**Repos:** src, tests

### API.HttpGet (8 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Identity.API/Quickstart/Account/ExternalController.cs` | 33 | `[HttpGet]` |
| src | `src/Identity.API/Quickstart/Account/ExternalController.cs` | 63 | `[HttpGet]` |
| src | `src/Identity.API/Quickstart/Account/AccountController.cs` | 39 | `[HttpGet]` |
| src | `src/Identity.API/Quickstart/Account/AccountController.cs` | 146 | `[HttpGet]` |
| src | `src/Identity.API/Quickstart/Account/AccountController.cs` | 196 | `[HttpGet]` |
| src | `src/Identity.API/Quickstart/Consent/ConsentController.cs` | 32 | `[HttpGet]` |
| src | `src/Identity.API/Quickstart/Device/DeviceController.cs` | 27 | `[HttpGet]` |
| src | `src/Identity.API/Quickstart/Grants/GrantsController.cs` | 32 | `[HttpGet]` |

**Repos:** src

### API.Controller (7 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Identity.API/Quickstart/Account/ExternalController.cs` | 5 | `public class ExternalController : Controller` |
| src | `src/Identity.API/Quickstart/Account/AccountController.cs` | 8 | `public class AccountController : Controller` |
| src | `src/Identity.API/Quickstart/Home/HomeController.cs` | 8 | `public class HomeController : Controller` |
| src | `src/Identity.API/Quickstart/Consent/ConsentController.cs` | 11 | `public class ConsentController : Controller` |
| src | `src/Identity.API/Quickstart/Device/DeviceController.cs` | 8 | `public class DeviceController : Controller` |
| src | `src/Identity.API/Quickstart/Grants/GrantsController.cs` | 11 | `public class GrantsController : Controller` |
| src | `src/Identity.API/Quickstart/Diagnostics/DiagnosticsController.cs` | 9 | `public class DiagnosticsController : Controller` |

**Repos:** src

### API.HttpPost (6 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Identity.API/Quickstart/Account/AccountController.cs` | 59 | `[HttpPost]` |
| src | `src/Identity.API/Quickstart/Account/AccountController.cs` | 165 | `[HttpPost]` |
| src | `src/Identity.API/Quickstart/Consent/ConsentController.cs` | 47 | `[HttpPost]` |
| src | `src/Identity.API/Quickstart/Device/DeviceController.cs` | 41 | `[HttpPost]` |
| src | `src/Identity.API/Quickstart/Device/DeviceController.cs` | 51 | `[HttpPost]` |
| src | `src/Identity.API/Quickstart/Grants/GrantsController.cs` | 41 | `[HttpPost]` |

**Repos:** src

### API.MapPost (6 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 103 | `api.MapPost("/items", CreateItem)` |
| src | `src/Ordering.API/Apis/OrdersApi.cs` | 16 | `api.MapPost("/draft", CreateOrderDraftAsync);` |
| src | `src/Ordering.API/Apis/OrdersApi.cs` | 17 | `api.MapPost("/", CreateOrderAsync);` |
| src | `src/Webhooks.API/Apis/WebHooksApi.cs` | 35 | `api.MapPost("/", async Task<Results<Created, BadRequest<stri` |
| src | `src/WebhookClient/Endpoints/WebhookEndpoints.cs` | 31 | `app.MapPost("/webhook-received", async (WebhookData hook, Ht` |
| src | `src/WebhookClient/Endpoints/AuthenticationEndpoints.cs` | 12 | `app.MapPost("/logout", async (HttpContext httpContext, IAnti` |

**Repos:** src

### HttpClient.PostAsync (6 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/WebhookClient/Services/WebHooksClient.cs` | 7 | `return client.PostAsJsonAsync("/api/webhooks", payload);` |
| tests | `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 128 | `var response = await _httpClient.PostAsync("api/orders", con` |
| tests | `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 155 | `var response = await _httpClient.PostAsync("api/orders", con` |
| tests | `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 181 | `var response = await _httpClient.PostAsync("api/orders/draft` |
| tests | `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 196 | `var response = await _httpClient.PostAsync("api/orders/draft` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 384 | `var response = await _httpClient.PostAsJsonAsync("/api/catal` |

**Repos:** src, tests

### HttpClient.PutAsync (6 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| tests | `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 46 | `var response = await _httpClient.PutAsync("/api/orders/cance` |
| tests | `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 61 | `var response = await _httpClient.PutAsync("api/orders/cancel` |
| tests | `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 76 | `var response = await _httpClient.PutAsync("api/orders/ship",` |
| tests | `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 91 | `var response = await _httpClient.PutAsync("api/orders/ship",` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 65 | `1.0 => await _httpClient.PutAsJsonAsync("/api/catalog/items"` |
| tests | `tests/Catalog.FunctionalTests/CatalogApiTests.cs` | 101 | `1.0 => await _httpClient.PutAsJsonAsync("/api/catalog/items"` |

**Repos:** tests

### API.MapGroup (5 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 16 | `var api = vApi.MapGroup("api/catalog").HasApiVersion(1, 0).H` |
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 17 | `var v1 = vApi.MapGroup("api/catalog").HasApiVersion(1, 0);` |
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 18 | `var v2 = vApi.MapGroup("api/catalog").HasApiVersion(2, 0);` |
| src | `src/Ordering.API/Apis/OrdersApi.cs` | 9 | `var api = app.MapGroup("api/orders").HasApiVersion(1.0);` |
| src | `src/Webhooks.API/Apis/WebHooksApi.cs` | 11 | `var api = app.MapGroup("/api/webhooks").HasApiVersion(1.0);` |

**Repos:** src

### HttpClient.Injection (4 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/WebApp/Extensions/Extensions.cs` | 34 | `builder.Services.AddHttpClient<CatalogService>(o => o.BaseAd` |
| src | `src/WebApp/Extensions/Extensions.cs` | 38 | `builder.Services.AddHttpClient<OrderingService>(o => o.BaseA` |
| src | `src/HybridApp/MauiProgram.cs` | 30 | `builder.Services.AddHttpClient<CatalogService>(o => o.BaseAd` |
| src | `src/WebhookClient/Extensions/Extensions.cs` | 19 | `builder.Services.AddHttpClient<WebhooksClient>(o => o.BaseAd` |

**Repos:** src

### API.MapPut (4 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 93 | `v1.MapPut("/items", UpdateItemV1)` |
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 98 | `v2.MapPut("/items/{id:int}", UpdateItem)` |
| src | `src/Ordering.API/Apis/OrdersApi.cs` | 11 | `api.MapPut("/cancel", CancelOrderAsync);` |
| src | `src/Ordering.API/Apis/OrdersApi.cs` | 12 | `api.MapPut("/ship", ShipOrderAsync);` |

**Repos:** src

### API.MapDelete (2 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 107 | `api.MapDelete("/items/{id:int}", DeleteItemById)` |
| src | `src/Webhooks.API/Apis/WebHooksApi.cs` | 66 | `api.MapDelete("/{id:int}", async Task<Results<Accepted, NotF` |

**Repos:** src

### HttpClient.New (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/ClientApp/Services/RequestProvider/RequestProvider.cs` | 15 | `var httpClient = _messageHandler is not null ? new HttpClien` |

**Repos:** src

### gRPC.Client (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/ClientApp/Services/Basket/BasketService.cs` | 125 | `_channel = GrpcChannel.ForAddress(_settingsService.GatewayBa` |

**Repos:** src

## Cache

### Redis.Read (57 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Ordering.API/Application/Commands/SetStockConfirmedOrderStatusCommandHandler.cs` | 24 | `var orderToUpdate = await _orderRepository.GetAsync(command.` |
| src | `src/Ordering.API/Application/Commands/SetAwaitingValidationOrderStatusCommandHandler.cs` | 21 | `var orderToUpdate = await _orderRepository.GetAsync(command.` |
| src | `src/Ordering.API/Application/Commands/CancelOrderCommandHandler.cs` | 21 | `var orderToUpdate = await _orderRepository.GetAsync(command.` |
| src | `src/Ordering.API/Application/Commands/SetPaidOrderStatusCommandHandler.cs` | 24 | `var orderToUpdate = await _orderRepository.GetAsync(command.` |
| src | `src/Ordering.API/Application/Commands/SetStockRejectedOrderStatusCommandHandler.cs` | 24 | `var orderToUpdate = await _orderRepository.GetAsync(command.` |
| src | `src/Ordering.API/Application/Commands/ShipOrderCommandHandler.cs` | 21 | `var orderToUpdate = await _orderRepository.GetAsync(command.` |
| src | `src/Ordering.API/Application/DomainEventHandlers/OrderStatusChangedToStockConfirmedDomainEventHandler.cs` | 27 | `var order = await _orderRepository.GetAsync(domainEvent.Orde` |
| src | `src/Ordering.API/Application/DomainEventHandlers/UpdateOrderWhenBuyerAndPaymentMethodVerifiedDomainEventHandler.cs` | 21 | `var orderToUpdate = await _orderRepository.GetAsync(domainEv` |
| src | `src/Ordering.API/Application/DomainEventHandlers/OrderStatusChangedToAwaitingValidationDomainEventHandler.cs` | 27 | `var order = await _orderRepository.GetAsync(domainEvent.Orde` |
| src | `src/Ordering.API/Application/DomainEventHandlers/OrderStatusChangedToPaidDomainEventHandler.cs` | 26 | `var order = await _orderRepository.GetAsync(domainEvent.Orde` |
| src | `src/Ordering.API/Application/DomainEventHandlers/OrderShippedDomainEventHandler.cs` | 27 | `var order = await _orderRepository.GetAsync(domainEvent.Orde` |
| src | `src/Ordering.API/Application/DomainEventHandlers/OrderCancelledDomainEventHandler.cs` | 27 | `var order = await _orderRepository.GetAsync(domainEvent.Orde` |
| src | `src/ClientApp/Services/RequestProvider/RequestProvider.cs` | 24 | `using var response = await httpClient.GetAsync(uri).Configur` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 44 | `var userToken = await SecureStorage.GetAsync(UserAccessToken` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 51 | `get => Preferences.Get(IdUseMocks, UseMocksDefault);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 57 | `get => Preferences.Get(nameof(DefaultEndpoint), string.Empty` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 63 | `get => Preferences.Get(nameof(RegistrationEndpoint), string.` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 69 | `get => Preferences.Get(nameof(AuthorizeEndpoint), string.Emp` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 75 | `get => Preferences.Get(nameof(UserInfoEndpoint), string.Empt` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 81 | `get => Preferences.Get(nameof(ClientId), DefaultClientId);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 87 | `get => Preferences.Get(nameof(ClientSecret), DefaultClientSe` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 93 | `get => Preferences.Get(nameof(CallbackUri), DefaultCallbackU` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 99 | `get => Preferences.Get(IdIdentityBase, string.Empty);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 105 | `get => Preferences.Get(IdGatewayShoppingBase, string.Empty);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 111 | `get => Preferences.Get(IdGatewayMarketingBase, string.Empty)` |

*... and 32 more*

**Repos:** src, tests

### Redis.Write (18 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 38 | `.SetAsync(UserAccessToken, userToken is not null ? JsonSeria` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 52 | `set => Preferences.Set(IdUseMocks, value);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 58 | `set => Preferences.Set(nameof(DefaultEndpoint), value);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 64 | `set => Preferences.Set(nameof(RegistrationEndpoint), value);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 70 | `set => Preferences.Set(nameof(AuthorizeEndpoint), value);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 76 | `set => Preferences.Set(nameof(UserInfoEndpoint), value);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 82 | `set => Preferences.Set(nameof(ClientId), value);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 88 | `set => Preferences.Set(nameof(ClientSecret), value);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 94 | `set => Preferences.Set(nameof(CallbackUri), value);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 100 | `set => Preferences.Set(IdIdentityBase, value);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 106 | `set => Preferences.Set(IdGatewayShoppingBase, value);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 112 | `set => Preferences.Set(IdGatewayMarketingBase, value);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 118 | `set => Preferences.Set(IdGatewayOrdersBase, value);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 124 | `set => Preferences.Set(IdGatewayBasketBase, value);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 130 | `set => Preferences.Set(IdUseFakeLocation, value);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 136 | `set => Preferences.Set(IdLatitude, value);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 142 | `set => Preferences.Set(IdLongitude, value);` |
| src | `src/ClientApp/Services/Settings/SettingsService.cs` | 148 | `set => Preferences.Set(IdAllowGpsLocation, value);` |

**Repos:** src

### Redis (2 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Basket.API/GlobalUsings.cs` | 11 | `global using StackExchange.Redis;` |
| src | `src/Basket.API/Repositories/RedisBasketRepository.cs` | 6 | `public class RedisBasketRepository(ILogger<RedisBasketReposi` |

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

### Dapper.Execute (10 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Catalog.API/IntegrationEvents/CatalogIntegrationEventService.cs` | 34 | `await ResilientTransaction.New(catalogContext).ExecuteAsync(` |
| src | `src/IntegrationEventLogEF/Utilities/ResilientTransaction.cs` | 16 | `await strategy.ExecuteAsync(async () =>` |
| src | `src/Ordering.API/Application/Behaviors/TransactionBehavior.cs` | 34 | `await strategy.ExecuteAsync(async () =>` |
| src | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | 57 | `await _pipeline.Execute(async () =>` |
| src | `src/ClientApp/Views/ContentPageBase.cs` | 21 | `await ivmb.InitializeAsyncCommand.ExecuteAsync(null);` |
| src | `src/ClientApp/Views/ProfileView.xaml.cs` | 20 | `_viewModel.RefreshCommand.Execute(null);` |
| src | `src/ClientApp/Controls/ToggleButton.cs` | 77 | `Command.Execute(CommandParameter);` |
| src | `src/Shared/MigrateDbContextExtensions.cs` | 46 | `await strategy.ExecuteAsync(() => InvokeSeeder(seeder, conte` |
| tests | `tests/ClientApp.UnitTests/TestingExtensions.cs` | 12 | `await arc.ExecuteAsync(parameter);` |
| tests | `tests/ClientApp.UnitTests/TestingExtensions.cs` | 16 | `command.Execute(parameter);` |

**Repos:** src, tests

### DbSet (9 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Catalog.API/Infrastructure/CatalogContext.cs` | 14 | `public required DbSet<CatalogItem> CatalogItems { get; set; ` |
| src | `src/Catalog.API/Infrastructure/CatalogContext.cs` | 15 | `public required DbSet<CatalogBrand> CatalogBrands { get; set` |
| src | `src/Catalog.API/Infrastructure/CatalogContext.cs` | 16 | `public required DbSet<CatalogType> CatalogTypes { get; set; ` |
| src | `src/Ordering.Infrastructure/OrderingContext.cs` | 12 | `public DbSet<Order> Orders { get; set; }` |
| src | `src/Ordering.Infrastructure/OrderingContext.cs` | 13 | `public DbSet<OrderItem> OrderItems { get; set; }` |
| src | `src/Ordering.Infrastructure/OrderingContext.cs` | 14 | `public DbSet<PaymentMethod> Payments { get; set; }` |
| src | `src/Ordering.Infrastructure/OrderingContext.cs` | 15 | `public DbSet<Buyer> Buyers { get; set; }` |
| src | `src/Ordering.Infrastructure/OrderingContext.cs` | 16 | `public DbSet<CardType> CardTypes { get; set; }` |
| src | `src/Webhooks.API/Infrastructure/WebhooksContext.cs` | 10 | `public DbSet<WebhookSubscription> Subscriptions { get; set; ` |

**Repos:** src

### MongoDB.Read (6 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Catalog.API/IntegrationEvents/EventHandling/OrderStatusChangedToAwaitingValidationIntegrationEventHandler.cs` | 17 | `var catalogItem = catalogContext.CatalogItems.Find(orderStoc` |
| src | `src/Catalog.API/IntegrationEvents/EventHandling/OrderStatusChangedToPaidIntegrationEventHandler.cs` | 15 | `var catalogItem = catalogContext.CatalogItems.Find(orderStoc` |
| src | `src/Catalog.API/Apis/CatalogApi.cs` | 210 | `var item = await context.CatalogItems.FindAsync(id);` |
| src | `src/Ordering.Domain/SeedWork/ValueObject.cs` | 37 | `.Aggregate((x, y) => x ^ y);` |
| src | `src/Ordering.Infrastructure/Repositories/OrderRepository.cs` | 23 | `var order = await _context.Orders.FindAsync(orderId);` |
| src | `src/Ordering.API/Application/DomainEventHandlers/ValidateOrAddBuyerAggregateWhenOrderStartedDomainEventHandler.cs` | 23 | `var buyer = await _buyerRepository.FindAsync(domainEvent.Use` |

**Repos:** src

### EntityFramework (2 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Catalog.API/Extensions/Extensions.cs` | 17 | `dbContextOptionsBuilder.UseNpgsql(builder =>` |
| src | `src/Ordering.API/Extensions/Extensions.cs` | 17 | `options.UseNpgsql(builder.Configuration.GetConnectionString(` |

**Repos:** src

### SQL.Insert (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Ordering.Infrastructure/Migrations/20240106121712_UseEnumForOrderStatus.cs` | 76 | `INSERT INTO ordering.orderstatus("Id","Name") VALUES` |

**Repos:** src

## Ui

### WPF.ViewModel (15 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/ClientApp/Validations/ValidatableObject.cs` | 3 | `public class ValidatableObject<T> : ObservableObject, IValid` |
| src | `src/ClientApp/ViewModels/CheckoutViewModel.cs` | 13 | `public partial class CheckoutViewModel : ViewModelBase` |
| src | `src/ClientApp/ViewModels/Base/ViewModelBase.cs` | 5 | `public abstract partial class ViewModelBase : ObservableObje` |
| src | `src/ClientApp/ViewModels/ObservableCollectionEx.cs` | 7 | `public class ObservableCollectionEx<T> : ObservableCollectio` |
| src | `src/ClientApp/ViewModels/LoginViewModel.cs` | 11 | `public partial class LoginViewModel : ViewModelBase` |
| src | `src/ClientApp/ViewModels/CatalogViewModel.cs` | 11 | `public partial class CatalogViewModel : ViewModelBase` |
| src | `src/ClientApp/ViewModels/BasketViewModel.cs` | 9 | `public partial class BasketViewModel : ViewModelBase` |
| src | `src/ClientApp/ViewModels/SettingsViewModel.cs` | 13 | `public class SettingsViewModel : ViewModelBase` |
| src | `src/ClientApp/ViewModels/ProfileViewModel.cs` | 9 | `public partial class ProfileViewModel : ViewModelBase` |
| src | `src/ClientApp/ViewModels/OrderDetailViewModel.cs` | 9 | `public partial class OrderDetailViewModel : ViewModelBase, I` |
| src | `src/ClientApp/ViewModels/SelectionViewModel.cs` | 3 | `public partial class SelectionViewModel<T> : ObservableObjec` |
| src | `src/ClientApp/ViewModels/MapViewModel.cs` | 6 | `public partial class MapViewModel : ViewModelBase` |
| src | `src/ClientApp/ViewModels/MainViewModel.cs` | 6 | `public partial class MainViewModel : ViewModelBase` |
| src | `src/ClientApp/ViewModels/CatalogItemViewModel.cs` | 11 | `public partial class CatalogItemViewModel : ViewModelBase` |
| tests | `tests/ClientApp.UnitTests/Mocks/MockViewModel.cs` | 6 | `public class MockViewModel : ViewModelBase` |

**Repos:** src, tests

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

## Pattern

### Repository (4 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Ordering.Infrastructure/Repositories/BuyerRepository.cs` | 3 | `public class BuyerRepository` |
| src | `src/Ordering.Infrastructure/Repositories/OrderRepository.cs` | 3 | `public class OrderRepository` |
| src | `src/Basket.API/Repositories/RedisBasketRepository.cs` | 6 | `public class RedisBasketRepository(ILogger<RedisBasketReposi` |
| src | `src/WebhookClient/Services/HooksRepository.cs` | 5 | `public class HooksRepository` |

**Repos:** src

## Messaging

### RabbitMQ (4 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/EventBusRabbitMQ/GlobalUsings.cs` | 8 | `global using RabbitMQ.Client;` |
| src | `src/EventBusRabbitMQ/GlobalUsings.cs` | 9 | `global using RabbitMQ.Client.Events;` |
| src | `src/EventBusRabbitMQ/GlobalUsings.cs` | 10 | `global using RabbitMQ.Client.Exceptions;` |
| src | `src/EventBusRabbitMQ/RabbitMqDependencyInjectionExtensions.cs` | 23 | `// RabbitMQ.Client doesn't have built-in support for OpenTel` |

**Repos:** src

## Storage

### File.Read (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Catalog.API/Infrastructure/CatalogContextSeed.cs` | 26 | `var sourceJson = File.ReadAllText(sourcePath);` |

**Repos:** src


---

*[Back to Index](../index.md)*
