# Dependency Visualizations

## landscape

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

## core libraries

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

## data infrastructure

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
        datasource_src_MongoDB_Read[("MongoDB.Read")]
        datasource_src_Dapper_Execute[("Dapper.Execute")]
        datasource_src_DbContext[("DbContext")]
        datasource_src_DbSet[("DbSet")]
        datasource_src_EntityFramework[("EntityFramework")]
        datasource_src_SQL_Insert[("SQL.Insert")]
        datasource_src_Redis[("Redis")]
        datasource_src_Redis_Read[("Redis.Read")]
        datasource_src_RabbitMQ[("RabbitMQ")]
        datasource_src_Redis_Write[("Redis.Write")]
        datasource_tests_Redis_Read[("Redis.Read")]
        datasource_tests_Dapper_Execute[("Dapper.Execute")]
    end
```

## data flow

```mermaid
graph LR
    subgraph Projects["Services & Projects"]
        Catalog_API["Catalog.API"]
        Ordering_API["Ordering.API"]
        Ordering_Infrastructure["Ordering.Infrastructure"]
        WebhookClient["WebhookClient"]
        Webhooks_API["Webhooks.API"]
        eShop_ServiceDefaults["eShop.ServiceDefaults"]
    end
    subgraph Database["Database / Storage"]
        entity_CatalogItem[("CatalogItem")]
        entity_CatalogBrand[("CatalogBrand")]
        entity_CatalogType[("CatalogType")]
        entity_Order[("Order")]
        entity_OrderItem[("OrderItem")]
    end
    subgraph APIs["API Routes"]
        route__(["/"])
        route__items(["/items"])
        route__items_by(["/items/by"])
        route__items__id_int_(["/items/{id:int}"])
        route__items_by__name_minlength_1__(["/items/by/{name:minlength(1)}"])
        route__items__id_int__pic(["/items/{id:int}/pic"])
        route__items_withsemanticrelevance__text_minlength_1__(["/items/withsemanticrelevance/{text:minlength(1)}"])
        route__items_withsemanticrelevance(["/items/withsemanticrelevance"])
        route__items_type__typeId__brand__brandId__(["/items/type/{typeId}/brand/{brandId?}"])
        route__items_type_all_brand__brandId_int__(["/items/type/all/brand/{brandId:int?}"])
        route__catalogtypes(["/catalogtypes"])
        route__catalogbrands(["/catalogbrands"])
        route_api_catalog(["api/catalog"])
        route__orderId_int_(["{orderId:int}"])
        route__cardtypes(["/cardtypes"])
        route__draft(["/draft"])
        route__cancel(["/cancel"])
        route__ship(["/ship"])
        route_api_orders(["api/orders"])
        route___id_int_(["/{id:int}"])
        route__api_webhooks(["/api/webhooks"])
        route__webhook_received(["/webhook-received"])
        route__logout(["/logout"])
        url__api_webhooks(["/api/webhooks"])
    end
    Catalog_API ==>|write| entity_CatalogItem
    entity_CatalogItem -.->|read| Catalog_API
    Catalog_API ==>|write| entity_CatalogBrand
    entity_CatalogBrand -.->|read| Catalog_API
    Catalog_API ==>|write| entity_CatalogType
    entity_CatalogType -.->|read| Catalog_API
    Ordering_Infrastructure ==>|write| entity_Order
    entity_Order -.->|read| Ordering_Infrastructure
    Ordering_Infrastructure ==>|write| entity_OrderItem
    entity_OrderItem -.->|read| Ordering_Infrastructure
    Ordering_API ==>|expose| route__
    Webhooks_API ==>|expose| route__
    eShop_ServiceDefaults ==>|expose| route__
    Catalog_API ==>|expose| route__items
    Catalog_API ==>|expose| route__items_by
    Catalog_API ==>|expose| route__items__id_int_
    Catalog_API ==>|expose| route__items_by__name_minlength_1__
    Catalog_API ==>|expose| route__items__id_int__pic
    Catalog_API ==>|expose| route__items_withsemanticrelevance__text_minlength_1__
    Catalog_API ==>|expose| route__items_withsemanticrelevance
    Catalog_API ==>|expose| route__items_type__typeId__brand__brandId__
    Catalog_API ==>|expose| route__items_type_all_brand__brandId_int__
    Catalog_API ==>|expose| route__catalogtypes
    Catalog_API ==>|expose| route__catalogbrands
    Catalog_API ==>|expose| route_api_catalog
    Ordering_API ==>|expose| route__orderId_int_
    Ordering_API ==>|expose| route__cardtypes
    Ordering_API ==>|expose| route__draft
    Ordering_API ==>|expose| route__cancel
    Ordering_API ==>|expose| route__ship
    Ordering_API ==>|expose| route_api_orders
    Webhooks_API ==>|expose| route___id_int_
    Webhooks_API ==>|expose| route__api_webhooks
    WebhookClient ==>|expose| route__webhook_received
    WebhookClient ==>|expose| route__logout
    url__api_webhooks -.->|consume| WebhookClient
```

## nuget groups

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

## business layers

```mermaid
graph TD
    layer_Presentation["Presentation (3)"]
    layer_Service["Service (12)"]
    layer_DataAccess["DataAccess (6)"]
    layer_Unclassified["Unclassified (3)"]
    layer_Service -->|10 refs| layer_DataAccess
    layer_DataAccess -->|7 refs| layer_Service
    layer_DataAccess -->|4 refs| layer_Unclassified
    layer_Service -->|2 refs| layer_Unclassified
    layer_Unclassified -->|2 refs| layer_Service
    layer_Unclassified -->|1 refs| layer_DataAccess
    layer_Presentation -->|1 refs| layer_Service
```

## e2e flows

```mermaid
graph TD
    no_data[No end-to-end flow paths found]
```

## field traceability

```mermaid
graph TD
    subgraph XAML["XAML Views"]
        xaml_MapView_Description["MapView\nDescription"]
        xaml_FiltersView_Value_Brand["FiltersView\nValue.Brand"]
        xaml_FiltersView_Value_Type["FiltersView\nValue.Type"]
        xaml_CatalogView_Value_Brand["CatalogView\nValue.Brand"]
        xaml_CatalogView_Value_Type["CatalogView\nValue.Type"]
        xaml_CampaignTemplate_PictureUri["CampaignTemplate\nPictureUri"]
        xaml_CampaignTemplate_Name["CampaignTemplate\nName"]
        xaml_BasketItemTemplate_PictureUrl["BasketItemTemplate\nPictureUrl"]
        xaml_BasketItemTemplate_ProductName["BasketItemTemplate\nProductName"]
        xaml_BasketItemTemplate_UnitPrice["BasketItemTemplate\nUnitPrice"]
        xaml_BasketItemTemplate_Quantity["BasketItemTemplate\nQuantity"]
        xaml_BasketItemTemplate_Total["BasketItemTemplate\nTotal"]
        xaml_OrderItemTemplate_PictureUrl["OrderItemTemplate\nPictureUrl"]
        xaml_OrderItemTemplate_ProductName["OrderItemTemplate\nProductName"]
        xaml_OrderItemTemplate_UnitPrice["OrderItemTemplate\nUnitPrice"]
        xaml_OrderItemTemplate_Quantity["OrderItemTemplate\nQuantity"]
        xaml_OrderItemTemplate_Total["OrderItemTemplate\nTotal"]
        xaml_OrderTemplate_OrderNumber["OrderTemplate\nOrderNumber"]
        xaml_OrderTemplate_Total["OrderTemplate\nTotal"]
        xaml_OrderTemplate_OrderDate["OrderTemplate\nOrderDate"]
    end
    subgraph VM["ViewModels"]
        vm_MapViewModel_Description["MapViewModel\nDescription: string"]
    end
    subgraph Entity["Entities"]
        ent_CatalogItem_Description["CatalogItem\nDescription: string"]
        ent_CatalogBrand_Brand["CatalogBrand\nBrand: string"]
        ent_CatalogType_Type["CatalogType\nType: string"]
        ent_CatalogItem_PictureUri["CatalogItem\nPictureUri: string"]
        ent_CatalogItem_Name["CatalogItem\nName: string"]
        ent_OrderItem_PictureUrl["OrderItem\nPictureUrl: string"]
        ent_OrderItem_ProductName["OrderItem\nProductName: string"]
        ent_OrderItem_UnitPrice["OrderItem\nUnitPrice: decimal"]
        ent_OrderItem_Quantity["OrderItem\nQuantity: int"]
        ent_Order_Total["Order\nTotal: decimal"]
        ent_Order_OrderNumber["Order\nOrderNumber: int"]
        ent_Order_OrderDate["Order\nOrderDate: DateTime"]
    end
    subgraph DB["Database Columns"]
        db_CatalogItems_Description[("CatalogItems\nDescription")]
        db_CatalogBrands_Brand[("CatalogBrands\nBrand")]
        db_CatalogTypes_Type[("CatalogTypes\nType")]
        db_CatalogItems_PictureUri[("CatalogItems\nPictureUri")]
        db_CatalogItems_Name[("CatalogItems\nName")]
        db_OrderItems_PictureUrl[("OrderItems\nPictureUrl")]
        db_OrderItems_ProductName[("OrderItems\nProductName")]
        db_OrderItems_UnitPrice[("OrderItems\nUnitPrice")]
        db_OrderItems_Quantity[("OrderItems\nQuantity")]
        db_Orders_Total[("Orders\nTotal")]
        db_Orders_OrderNumber[("Orders\nOrderNumber")]
        db_Orders_OrderDate[("Orders\nOrderDate")]
    end
    xaml_MapView_Description --> vm_MapViewModel_Description
    vm_MapViewModel_Description --> ent_CatalogItem_Description
    ent_CatalogItem_Description --> db_CatalogItems_Description
    xaml_FiltersView_Value_Brand -.-> ent_CatalogBrand_Brand
    ent_CatalogBrand_Brand -.-> db_CatalogBrands_Brand
    xaml_FiltersView_Value_Type -.-> ent_CatalogType_Type
    ent_CatalogType_Type -.-> db_CatalogTypes_Type
    xaml_CatalogView_Value_Brand -.-> ent_CatalogBrand_Brand
    xaml_CatalogView_Value_Type -.-> ent_CatalogType_Type
    xaml_CampaignTemplate_PictureUri -.-> ent_CatalogItem_PictureUri
    ent_CatalogItem_PictureUri -.-> db_CatalogItems_PictureUri
    xaml_CampaignTemplate_Name -.-> ent_CatalogItem_Name
    ent_CatalogItem_Name -.-> db_CatalogItems_Name
    xaml_BasketItemTemplate_PictureUrl -.-> ent_OrderItem_PictureUrl
    ent_OrderItem_PictureUrl -.-> db_OrderItems_PictureUrl
    xaml_BasketItemTemplate_ProductName -.-> ent_OrderItem_ProductName
    ent_OrderItem_ProductName -.-> db_OrderItems_ProductName
    xaml_BasketItemTemplate_UnitPrice -.-> ent_OrderItem_UnitPrice
    ent_OrderItem_UnitPrice -.-> db_OrderItems_UnitPrice
    xaml_BasketItemTemplate_Quantity -.-> ent_OrderItem_Quantity
    ent_OrderItem_Quantity -.-> db_OrderItems_Quantity
    xaml_BasketItemTemplate_Total -.-> ent_Order_Total
    ent_Order_Total -.-> db_Orders_Total
    xaml_OrderItemTemplate_PictureUrl -.-> ent_OrderItem_PictureUrl
    xaml_OrderItemTemplate_ProductName -.-> ent_OrderItem_ProductName
    xaml_OrderItemTemplate_UnitPrice -.-> ent_OrderItem_UnitPrice
    xaml_OrderItemTemplate_Quantity -.-> ent_OrderItem_Quantity
    xaml_OrderItemTemplate_Total -.-> ent_Order_Total
    xaml_OrderTemplate_OrderNumber -.-> ent_Order_OrderNumber
    ent_Order_OrderNumber -.-> db_Orders_OrderNumber
    xaml_OrderTemplate_Total -.-> ent_Order_Total
    xaml_OrderTemplate_OrderDate -.-> ent_Order_OrderDate
    ent_Order_OrderDate -.-> db_Orders_OrderDate
```
