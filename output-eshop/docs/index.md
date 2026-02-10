# Dependency Map

## Overview

| Metric | Count |
|--------|-------|
| Repositories | 2 |
| Total Projects | 24 |
| NuGet Packages | 69 |
| Project References | 46 |
| Cross-Repo References | 10 |
| Data Access Findings | 77 |
| Config Files | 31 |

## Repositories

| Repo | Projects | Categories |
|------|----------|------------|
| **src** | 19 | WebApp:8, Library:5, Application:2, Service:2, Tool:2 |
| **tests** | 5 | Test:5 |

## Project Categories

| Category | Count |
|----------|-------|
| WebApp | 8 |
| Library | 5 |
| Test | 5 |
| Application | 2 |
| Service | 2 |
| Tool | 2 |

## Full Landscape

```mermaid
graph LR
    subgraph src["src"]
        subgraph src_webapp["webapp"]
            src_WebApp["WebApp"]
            src_Identity_API["Identity.API"]
            src_Catalog_API["Catalog.API"]
            src_WebAppComponents["WebAppComponents"]
            src_PaymentProcessor["PaymentProcessor"]
            src_Basket_API["Basket.API"]
            src_Ordering_API["Ordering.API"]
            src_Webhooks_API["Webhooks.API"]
        end
        subgraph src_library["library"]
            src_Ordering_Domain["Ordering.Domain"]
            src_Ordering_Infrastructure["Ordering.Infrastructure"]
            src_IntegrationEventLogEF["IntegrationEventLogEF"]
            src_EventBus["EventBus"]
            src_EventBusRabbitMQ["EventBusRabbitMQ"]
        end
        subgraph src_application["application"]
            src_eShop_AppHost["eShop.AppHost"]
            src_HybridApp["HybridApp"]
        end
        subgraph src_service["service"]
            src_OrderProcessor["OrderProcessor"]
            src_eShop_ServiceDefaults["eShop.ServiceDefaults"]
        end
        subgraph src_tool["tool"]
            src_ClientApp["ClientApp"]
            src_WebhookClient["WebhookClient"]
        end
    end
    subgraph tests["tests"]
        subgraph tests_test["test"]
            tests_Ordering_UnitTests["Ordering.UnitTests"]
            tests_Ordering_FunctionalTests["Ordering.FunctionalTests"]
            tests_Catalog_FunctionalTests["Catalog.FunctionalTests"]
            tests_Basket_UnitTests["Basket.UnitTests"]
            tests_ClientApp_UnitTests["ClientApp.UnitTests"]
        end
    end
    src_WebApp --> src_eShop_ServiceDefaults
    src_WebApp --> src_EventBusRabbitMQ
    src_WebApp --> src_WebAppComponents
    src_Identity_API --> src_eShop_ServiceDefaults
    src_Catalog_API --> src_EventBusRabbitMQ
    src_Catalog_API --> src_IntegrationEventLogEF
    src_Catalog_API --> src_eShop_ServiceDefaults
    src_eShop_AppHost --> src_Basket_API
    src_eShop_AppHost --> src_Catalog_API
    src_eShop_AppHost --> src_Identity_API
    src_eShop_AppHost --> src_Ordering_API
    src_eShop_AppHost --> src_OrderProcessor
    src_eShop_AppHost --> src_PaymentProcessor
    src_eShop_AppHost --> src_Webhooks_API
    src_eShop_AppHost --> src_WebApp
    src_eShop_AppHost --> src_WebhookClient
    src_Ordering_Infrastructure --> src_IntegrationEventLogEF
    src_Ordering_Infrastructure --> src_Ordering_Domain
    src_PaymentProcessor --> src_eShop_ServiceDefaults
    src_PaymentProcessor --> src_EventBusRabbitMQ
    src_OrderProcessor --> src_eShop_ServiceDefaults
    src_OrderProcessor --> src_EventBusRabbitMQ
    src_HybridApp --> src_WebAppComponents
    src_Basket_API --> src_eShop_ServiceDefaults
    src_Basket_API --> src_EventBusRabbitMQ
    src_IntegrationEventLogEF --> src_EventBus
    src_Ordering_API --> src_EventBusRabbitMQ
    src_Ordering_API --> src_IntegrationEventLogEF
    src_Ordering_API --> src_eShop_ServiceDefaults
    src_Ordering_API --> src_Ordering_Domain
    src_Ordering_API --> src_Ordering_Infrastructure
    src_EventBusRabbitMQ --> src_EventBus
    src_Webhooks_API --> src_EventBusRabbitMQ
    src_Webhooks_API --> src_IntegrationEventLogEF
    src_Webhooks_API --> src_eShop_ServiceDefaults
    src_WebhookClient --> src_eShop_ServiceDefaults
    tests_Ordering_UnitTests -.-> src_Ordering_API
    tests_Ordering_UnitTests -.-> src_Ordering_Domain
    tests_Ordering_UnitTests -.-> src_Ordering_Infrastructure
    tests_Ordering_FunctionalTests -.-> src_Ordering_API
    tests_Ordering_FunctionalTests -.-> src_Identity_API
    tests_Ordering_FunctionalTests -.-> src_Ordering_Domain
    tests_Ordering_FunctionalTests -.-> src_Ordering_Infrastructure
    tests_Catalog_FunctionalTests -.-> src_Catalog_API
    tests_Basket_UnitTests -.-> src_Basket_API
    tests_ClientApp_UnitTests -.-> src_ClientApp
```

## Core Library Hierarchy

```mermaid
graph TD
    subgraph src["src"]
        src_Ordering_Domain["Ordering.Domain"]
        src_Ordering_Infrastructure["Ordering.Infrastructure"]
        src_IntegrationEventLogEF["IntegrationEventLogEF"]
        src_EventBus["EventBus"]
        src_EventBusRabbitMQ["EventBusRabbitMQ"]
    end
    src_Ordering_Infrastructure --> src_IntegrationEventLogEF
    src_Ordering_Infrastructure --> src_Ordering_Domain
    src_IntegrationEventLogEF --> src_EventBus
    src_EventBusRabbitMQ --> src_EventBus
```

## Data Infrastructure

```mermaid
graph LR
    subgraph src["src"]
        src_WebApp["WebApp"]
        src_Identity_API["Identity.API"]
        src_Catalog_API["Catalog.API"]
        src_eShop_AppHost["eShop.AppHost"]
        src_WebAppComponents["WebAppComponents"]
        src_PaymentProcessor["PaymentProcessor"]
        src_OrderProcessor["OrderProcessor"]
        src_HybridApp["HybridApp"]
        src_Basket_API["Basket.API"]
        src_Ordering_API["Ordering.API"]
        src_eShop_ServiceDefaults["eShop.ServiceDefaults"]
        src_Webhooks_API["Webhooks.API"]
    end
    subgraph DataSources
        datasource_src_DbContext[("DbContext")]
        datasource_src_EntityFramework[("EntityFramework")]
        datasource_src_RabbitMQ[("RabbitMQ")]
        datasource_src_Redis[("Redis")]
        datasource_src_Dapper[("Dapper")]
        datasource_tests_Dapper[("Dapper")]
    end
```

## NuGet Package Groups

```mermaid
graph LR
    subgraph Microsoft["Microsoft"]
        nuget_Microsoft_Extensions_ServiceDiscovery_Yarp["Microsoft.Extensions.ServiceDiscovery.Yarp<br/>"]
        nuget_Microsoft_AspNetCore_Authentication_OpenIdConnect["Microsoft.AspNetCore.Authentication.OpenIdConnect<br/>"]
        nuget_Microsoft_AspNetCore_Identity_EntityFrameworkCore["Microsoft.AspNetCore.Identity.EntityFrameworkCore<br/>"]
        nuget_Microsoft_AspNetCore_Identity_UI["Microsoft.AspNetCore.Identity.UI<br/>"]
        nuget_Microsoft_EntityFrameworkCore_Tools["Microsoft.EntityFrameworkCore.Tools<br/>"]
        nuget_Microsoft_Web_LibraryManager_Build["Microsoft.Web.LibraryManager.Build<br/>"]
        nuget_Microsoft_Extensions_ApiDescription_Server["Microsoft.Extensions.ApiDescription.Server<br/>"]
        nuget_Microsoft_AspNetCore_Components_Web["Microsoft.AspNetCore.Components.Web<br/>"]
        Microsoft_more["... +16 more"]
    end
    subgraph Aspire["Aspire"]
        nuget_Aspire_Azure_AI_OpenAI["Aspire.Azure.AI.OpenAI<br/>"]
        nuget_Aspire_Npgsql_EntityFrameworkCore_PostgreSQL["Aspire.Npgsql.EntityFrameworkCore.PostgreSQL<br/>"]
        nuget_Aspire_Hosting_RabbitMQ["Aspire.Hosting.RabbitMQ<br/>"]
        nuget_Aspire_Hosting_Redis["Aspire.Hosting.Redis<br/>"]
        nuget_Aspire_Hosting_PostgreSQL["Aspire.Hosting.PostgreSQL<br/>"]
        nuget_Aspire_Hosting_Azure_CognitiveServices["Aspire.Hosting.Azure.CognitiveServices<br/>"]
        nuget_Aspire_Hosting_Yarp["Aspire.Hosting.Yarp<br/>"]
        nuget_Aspire_Npgsql["Aspire.Npgsql<br/>"]
        Aspire_more["... +2 more"]
    end
    subgraph OpenTelemetry["OpenTelemetry"]
        nuget_OpenTelemetry_Exporter_OpenTelemetryProtocol["OpenTelemetry.Exporter.OpenTelemetryProtocol<br/>"]
        nuget_OpenTelemetry_Extensions_Hosting["OpenTelemetry.Extensions.Hosting<br/>"]
        nuget_OpenTelemetry_Instrumentation_AspNetCore["OpenTelemetry.Instrumentation.AspNetCore<br/>"]
        nuget_OpenTelemetry_Instrumentation_GrpcNetClient["OpenTelemetry.Instrumentation.GrpcNetClient<br/>"]
        nuget_OpenTelemetry_Instrumentation_Http["OpenTelemetry.Instrumentation.Http<br/>"]
        nuget_OpenTelemetry_Instrumentation_Runtime["OpenTelemetry.Instrumentation.Runtime<br/>"]
    end
    subgraph CommunityToolkit["CommunityToolkit"]
        nuget_CommunityToolkit_Aspire_OllamaSharp["CommunityToolkit.Aspire.OllamaSharp<br/>"]
        nuget_CommunityToolkit_Aspire_Hosting_Ollama["CommunityToolkit.Aspire.Hosting.Ollama<br/>"]
        nuget_CommunityToolkit_Maui["CommunityToolkit.Maui<br/>9.1.1"]
        nuget_CommunityToolkit_Mvvm["CommunityToolkit.Mvvm<br/>8.3.2"]
    end
    subgraph Grpc["Grpc"]
        nuget_Grpc_Net_ClientFactory["Grpc.Net.ClientFactory<br/>"]
        nuget_Grpc_Tools["Grpc.Tools<br/>, 2.69.0"]
        nuget_Grpc_AspNetCore["Grpc.AspNetCore<br/>"]
        nuget_Grpc_Net_Client["Grpc.Net.Client<br/>2.67.0"]
    end
    subgraph Duende["Duende"]
        nuget_Duende_IdentityServer_AspNetIdentity["Duende.IdentityServer.AspNetIdentity<br/>"]
        nuget_Duende_IdentityServer_EntityFramework["Duende.IdentityServer.EntityFramework<br/>"]
        nuget_Duende_IdentityServer_Storage["Duende.IdentityServer.Storage<br/>"]
        nuget_Duende_IdentityServer["Duende.IdentityServer<br/>"]
    end
    subgraph Asp["Asp"]
        nuget_Asp_Versioning_Http_Client["Asp.Versioning.Http.Client<br/>"]
        nuget_Asp_Versioning_Http["Asp.Versioning.Http<br/>"]
        nuget_Asp_Versioning_Mvc_ApiExplorer["Asp.Versioning.Mvc.ApiExplorer<br/>"]
    end
    subgraph Pgvector["Pgvector"]
        nuget_Pgvector["Pgvector<br/>"]
        nuget_Pgvector_EntityFrameworkCore["Pgvector.EntityFrameworkCore<br/>"]
    end
    subgraph FluentValidation["FluentValidation"]
        nuget_FluentValidation["FluentValidation<br/>"]
        nuget_FluentValidation_DependencyInjectionExtensions["FluentValidation.DependencyInjectionExtensions<br/>"]
    end
    subgraph IdentityModel["IdentityModel"]
        nuget_IdentityModel_OidcClient["IdentityModel.OidcClient<br/>6.0.0"]
        nuget_IdentityModel["IdentityModel<br/>7.0.0"]
    end
    subgraph NSubstitute["NSubstitute"]
        nuget_NSubstitute["NSubstitute<br/>"]
        nuget_NSubstitute_Analyzers_CSharp["NSubstitute.Analyzers.CSharp<br/>"]
    end
    subgraph Google["Google"]
        nuget_Google_Protobuf["Google.Protobuf<br/>, 3.29.3"]
    end
    subgraph MediatR["MediatR"]
        nuget_MediatR["MediatR<br/>"]
    end
    subgraph System["System"]
        nuget_System_Reflection_TypeExtensions["System.Reflection.TypeExtensions<br/>"]
    end
    subgraph Npgsql["Npgsql"]
        nuget_Npgsql_EntityFrameworkCore_PostgreSQL["Npgsql.EntityFrameworkCore.PostgreSQL<br/>"]
    end
```

## Navigation

### src
**Application** (2): [eShop.AppHost](repos/src/eShop.AppHost.md), [HybridApp](repos/src/HybridApp.md)

**Library** (5): [Ordering.Domain](repos/src/Ordering.Domain.md), [Ordering.Infrastructure](repos/src/Ordering.Infrastructure.md), [IntegrationEventLogEF](repos/src/IntegrationEventLogEF.md), [EventBus](repos/src/EventBus.md), [EventBusRabbitMQ](repos/src/EventBusRabbitMQ.md)

**Service** (2): [OrderProcessor](repos/src/OrderProcessor.md), [eShop.ServiceDefaults](repos/src/eShop.ServiceDefaults.md)

**Tool** (2): [ClientApp](repos/src/ClientApp.md), [WebhookClient](repos/src/WebhookClient.md)

**WebApp** (8): [WebApp](repos/src/WebApp.md), [Identity.API](repos/src/Identity.API.md), [Catalog.API](repos/src/Catalog.API.md), [WebAppComponents](repos/src/WebAppComponents.md), [PaymentProcessor](repos/src/PaymentProcessor.md), [Basket.API](repos/src/Basket.API.md), [Ordering.API](repos/src/Ordering.API.md), [Webhooks.API](repos/src/Webhooks.API.md)

### tests
**Test** (5): [Ordering.UnitTests](repos/tests/Ordering.UnitTests.md), [Ordering.FunctionalTests](repos/tests/Ordering.FunctionalTests.md), [Catalog.FunctionalTests](repos/tests/Catalog.FunctionalTests.md), [Basket.UnitTests](repos/tests/Basket.UnitTests.md), [ClientApp.UnitTests](repos/tests/ClientApp.UnitTests.md)

- [Data Source Registry](data-sources/registry.md)

---

*Generated: 2026-02-10*
*Tool: Dependency Mapper (Static Analysis)*
