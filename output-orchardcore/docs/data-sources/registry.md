# Data Source Registry

## Summary

| Type | Occurrences |
|------|-------------|
| database | 258 |
| config | 154 |
| messaging | 15 |
| api | 12 |
| cache | 12 |
| storage | 11 |

## Database

### Dapper (252 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/DeploymentPlanController.cs` | 76 | `var deploymentPlans = _session.Query<DeploymentPlan, Deploym` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/DeploymentPlanController.cs` | 135 | `var checkedItems = await _session.Query<DeploymentPlan, Depl` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/DeploymentPlanService.cs` | 30 | `var deploymentPlanQuery = _session.Query<DeploymentPlan, Dep` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/DeploymentPlanService.cs` | 93 | `var existingDeploymentPlans = (await _session.Query<Deployme` |
| src | `src/OrchardCore.Modules/OrchardCore.AuditTrail/Services/DefaultAuditTrailAdminListFilterProvider.cs` | 146 | `return sortOption.Query(val, query, ctx);` |
| src | `src/OrchardCore.Modules/OrchardCore.AuditTrail/Services/DefaultAuditTrailAdminListFilterProvider.cs` | 149 | `return options.DefaultSortOption.Query(val, query, ctx);` |
| src | `src/OrchardCore.Modules/OrchardCore.AuditTrail/Services/AuditTrailManager.cs` | 109 | `_session.Query<AuditTrailEvent, AuditTrailEventIndex>(collec` |
| src | `src/OrchardCore.Modules/OrchardCore.AuditTrail/Services/AuditTrailManager.cs` | 117 | `var events = await _session.Query<AuditTrailEvent, AuditTrai` |
| src | `src/OrchardCore.Modules/OrchardCore.AuditTrail/Services/DefaultAuditTrailAdminListQueryService.cs` | 43 | `var query = _session.Query<AuditTrailEvent>(collection: Audi` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Settings/TaxonomyContentsAdminListSettingsDisplayDriver.cs` | 43 | `var taxonomies = await _session.Query<ContentItem, ContentIt` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Helper/TaxonomyOrchardHelperExtensions.cs` | 64 | `var contentItems = await query(session.Query<ContentItem, Ta` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Controllers/WorkflowController.cs` | 116 | `var workflowsQuery = _session.Query<Workflow, WorkflowIndex>` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Controllers/WorkflowController.cs` | 310 | `var checkedEntries = await _session.Query<Workflow, Workflow` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Controllers/WorkflowTypeController.cs` | 99 | `var query = _session.Query<WorkflowType, WorkflowTypeIndex>(` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Controllers/WorkflowTypeController.cs` | 184 | `var checkedEntries = await _session.Query<WorkflowType, Work` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Trimming/Services/WorkflowTrimmingService.cs` | 50 | `.Query<Workflow, WorkflowIndex>(x => x.WorkflowStatus.IsIn(s` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Http/Services/WorkflowInstanceRouteEntries.cs` | 17 | `var workflowTypeDictionary = (await Session.Query<WorkflowTy` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Http/Services/WorkflowInstanceRouteEntries.cs` | 26 | `.Query<Workflow, WorkflowBlockingActivitiesIndex>(index =>` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Http/Services/WorkflowTypeRouteEntries.cs` | 17 | `var workflowTypeDictionary = (await Session.Query<WorkflowTy` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Services/WorkflowTypeStore.cs` | 34 | `return _session.Query<WorkflowType, WorkflowTypeIndex>(x => ` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Services/WorkflowTypeStore.cs` | 39 | `return _session.Query<WorkflowType, WorkflowTypeIndex>().Lis` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Services/WorkflowTypeStore.cs` | 45 | `.Query<WorkflowType, WorkflowTypeStartActivitiesIndex>(index` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Services/WorkflowTypeStore.cs` | 71 | `var workflows = await _session.Query<Workflow, WorkflowIndex` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Services/WorkflowStore.cs` | 25 | `return FilterByWorkflowTypeId(_session.Query<Workflow, Workf` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Services/WorkflowStore.cs` | 30 | `return (await _session.Query<Workflow, WorkflowBlockingActiv` |

*... and 227 more*

**Repos:** src, test

### EntityFramework (5 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore/OrchardCore.Data.YesSql/OrchardCoreBuilderExtensions.cs` | 76 | `.UseSqlServer(shellSettings["ConnectionString"], yesSqlOptio` |
| src | `src/OrchardCore/OrchardCore.Data.YesSql/OrchardCoreBuilderExtensions.cs` | 94 | `.UseMySql(shellSettings["ConnectionString"], yesSqlOptions.I` |
| test | `test/OrchardCore.Tests/Apis/GraphQL/Queries/PredicateQueryTests.cs` | 17 | `.UseSqlServer("Fake database connection string for testing;"` |
| test | `test/OrchardCore.Tests/Apis/GraphQL/Queries/PredicateQueryTests.cs` | 86 | `.UseMySql("Fake database connection string for testing;", "T` |
| test | `test/OrchardCore.Tests/Apis/GraphQL/Queries/PredicateQueryTests.cs` | 98 | `.UseSqlServer("Fake database connection string for testing;"` |

**Repos:** src, test

### SqlClient (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore/OrchardCore.Data.YesSql/DbConnectionValidator.cs` | 1 | `using Microsoft.Data.SqlClient;` |

**Repos:** src

## Config

### ConnectionString (154 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.Email.Azure/Models/AzureEmailOptions.cs` | 9 | `public string ConnectionString { get; set; }` |
| src | `src/OrchardCore.Modules/OrchardCore.Email.Azure/Models/AzureEmailOptions.cs` | 12 | `=> !string.IsNullOrWhiteSpace(DefaultSender) && !string.IsNu` |
| src | `src/OrchardCore.Modules/OrchardCore.Email.Azure/Models/AzureEmailSettings.cs` | 15 | `public string ConnectionString { get; set; }` |
| src | `src/OrchardCore.Modules/OrchardCore.Email.Azure/Drivers/AzureEmailSettingsDisplayDriver.cs` | 61 | `model.HasConnectionString = !string.IsNullOrWhiteSpace(setti` |
| src | `src/OrchardCore.Modules/OrchardCore.Email.Azure/Drivers/AzureEmailSettingsDisplayDriver.cs` | 107 | `if (string.IsNullOrWhiteSpace(model.ConnectionString)` |
| src | `src/OrchardCore.Modules/OrchardCore.Email.Azure/Drivers/AzureEmailSettingsDisplayDriver.cs` | 108 | `&& settings.ConnectionString is null)` |
| src | `src/OrchardCore.Modules/OrchardCore.Email.Azure/Drivers/AzureEmailSettingsDisplayDriver.cs` | 110 | `context.Updater.ModelState.AddModelError(Prefix, nameof(mode` |
| src | `src/OrchardCore.Modules/OrchardCore.Email.Azure/Drivers/AzureEmailSettingsDisplayDriver.cs` | 112 | `else if (!string.IsNullOrWhiteSpace(model.ConnectionString))` |
| src | `src/OrchardCore.Modules/OrchardCore.Email.Azure/Drivers/AzureEmailSettingsDisplayDriver.cs` | 117 | `var protectedConnection = protector.Protect(model.Connection` |
| src | `src/OrchardCore.Modules/OrchardCore.Email.Azure/Drivers/AzureEmailSettingsDisplayDriver.cs` | 120 | `hasChanges \|= protectedConnection != settings.ConnectionStri` |
| src | `src/OrchardCore.Modules/OrchardCore.Email.Azure/Drivers/AzureEmailSettingsDisplayDriver.cs` | 122 | `settings.ConnectionString = protectedConnection;` |
| src | `src/OrchardCore.Modules/OrchardCore.Email.Azure/Services/AzureEmailProviderBase.cs` | 138 | `_emailClient ??= new EmailClient(_providerOptions.Connection` |
| src | `src/OrchardCore.Modules/OrchardCore.Email.Azure/Services/AzureEmailOptionsConfiguration.cs` | 31 | `if (!string.IsNullOrEmpty(settings.ConnectionString))` |
| src | `src/OrchardCore.Modules/OrchardCore.Email.Azure/Services/AzureEmailOptionsConfiguration.cs` | 35 | `options.ConnectionString = protector.Unprotect(settings.Conn` |
| src | `src/OrchardCore.Modules/OrchardCore.Email.Azure/ViewModels/AzureEmailSettingsViewModel.cs` | 12 | `public string ConnectionString { get; set; }` |
| src | `src/OrchardCore.Modules/OrchardCore.Email.Azure/ViewModels/AzureEmailSettingsViewModel.cs` | 15 | `public bool HasConnectionString { get; set; }` |
| src | `src/OrchardCore.Modules/OrchardCore.Media.Azure/Controllers/AdminController.cs` | 38 | `ConnectionString = _options.ConnectionString,` |
| src | `src/OrchardCore.Modules/OrchardCore.Media.Azure/Startup.cs` | 48 | `var connectionString = section.GetValue<string>(nameof(Media` |
| src | `src/OrchardCore.Modules/OrchardCore.Media.Azure/Startup.cs` | 51 | `if (CheckOptions(connectionString, containerName, _logger))` |
| src | `src/OrchardCore.Modules/OrchardCore.Media.Azure/Startup.cs` | 124 | `private static bool CheckOptions(string connectionString, st` |
| src | `src/OrchardCore.Modules/OrchardCore.Media.Azure/Startup.cs` | 128 | `if (string.IsNullOrWhiteSpace(connectionString))` |
| src | `src/OrchardCore.Modules/OrchardCore.Media.Azure/Startup.cs` | 130 | `logger.LogError("Azure Media Storage is enabled but not acti` |
| src | `src/OrchardCore.Modules/OrchardCore.Media.Azure/Startup.cs` | 168 | `var connectionString = section.GetValue<string>(nameof(Media` |
| src | `src/OrchardCore.Modules/OrchardCore.Media.Azure/Startup.cs` | 171 | `if (!CheckOptions(connectionString, containerName))` |
| src | `src/OrchardCore.Modules/OrchardCore.Media.Azure/Startup.cs` | 184 | `private bool CheckOptions(string connectionString, string co` |

*... and 129 more*

**Repos:** src, test

## Messaging

### RabbitMQ (15 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.XmlRpc/MethodCallModelBinder.cs` | 10 | `public class MethodCallModelBinder : IModelBinder` |
| src | `src/OrchardCore/OrchardCore.Notifications.Core/Services/NotificationFilterEngineModelBinder.cs` | 5 | `public class NotificationFilterEngineModelBinder : IModelBin` |
| src | `src/OrchardCore/OrchardCore.Mvc.Core/ModelBinding/CheckMarkModelBinder.cs` | 5 | `public class CheckMarkModelBinder : IModelBinder` |
| src | `src/OrchardCore/OrchardCore.Mvc.Core/ModelBinding/SafeBoolModelBinderProvider.cs` | 5 | `internal sealed class SafeBoolModelBinderProvider : IModelBi` |
| src | `src/OrchardCore/OrchardCore.Mvc.Core/ModelBinding/SafeBoolModelBinderProvider.cs` | 7 | `public IModelBinder GetBinder(ModelBinderProviderContext con` |
| src | `src/OrchardCore/OrchardCore.Mvc.Core/ModelBinding/CheckMarkModelBinderProvider.cs` | 6 | `/// An <see cref="IModelBinderProvider"/> for <see cref="Che` |
| src | `src/OrchardCore/OrchardCore.Mvc.Core/ModelBinding/CheckMarkModelBinderProvider.cs` | 8 | `public class CheckMarkModelBinderProvider : IModelBinderProv` |
| src | `src/OrchardCore/OrchardCore.Mvc.Core/ModelBinding/CheckMarkModelBinderProvider.cs` | 11 | `public IModelBinder GetBinder(ModelBinderProviderContext con` |
| src | `src/OrchardCore/OrchardCore.Mvc.Core/ModelBinding/SafeBoolModelBinder.cs` | 12 | `internal sealed class SafeBoolModelBinder : IModelBinder` |
| src | `src/OrchardCore/OrchardCore.Infrastructure.Abstractions/Entities/ModelHandlerBase.cs` | 3 | `public abstract class ModelHandlerBase<T> : IModelHandler<T>` |
| src | `src/OrchardCore/OrchardCore.Infrastructure.Abstractions/Entities/IModelHandler.cs` | 3 | `public interface IModelHandler<T>` |
| src | `src/OrchardCore/OrchardCore.Indexing.Abstractions/IIndexProfileHandler.cs` | 6 | `public interface IIndexProfileHandler : IModelHandler<IndexP` |
| src | `src/OrchardCore/OrchardCore.Contents.Core/Services/ContentItemFilterEngineModelBinder.cs` | 5 | `public class ContentItemFilterEngineModelBinder : IModelBind` |
| src | `src/OrchardCore/OrchardCore.Users.Core/Services/UserFilterEngineModelBinder.cs` | 5 | `public class UserFilterEngineModelBinder : IModelBinder` |
| src | `src/OrchardCore/OrchardCore.AuditTrail.Abstractions/Services/AuditTrailFilterEngineModelBinder.cs` | 5 | `public class AuditTrailFilterEngineModelBinder : IModelBinde` |

**Repos:** src

## Api

### HttpClient.Injection (7 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.Twitter/Startup.cs` | 44 | `services.AddHttpClient<TwitterClient>()` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Http/Startup.cs` | 31 | `services.AddHttpClient();` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment.Remote/Startup.cs` | 14 | `services.AddHttpClient();` |
| src | `src/OrchardCore.Modules/OrchardCore.Media/Startup.cs` | 69 | `services.AddHttpClient();` |
| src | `src/OrchardCore/OrchardCore/Modules/Extensions/ServiceCollectionExtensions.cs` | 57 | `.AddHttpClient()` |
| src | `src/OrchardCore/OrchardCore.ReCaptcha.Core/ServiceCollectionExtensions.cs` | 20 | `.AddHttpClient(nameof(ReCaptchaService))` |
| src | `src/OrchardCore/OrchardCore.Sms.Core/ServiceCollectionExtensions.cs` | 46 | `services.AddHttpClient(TwilioSmsProvider.TechnicalName, clie` |

**Repos:** src

### HttpClient.New (3 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore/OrchardCore/Modules/Overrides/HttpClient/TenantHttpClientFactory.cs` | 119 | `var client = new HttpClient(handler, disposeHandler: false);` |
| test | `test/OrchardCore.Tests/Modules/OrchardCore.Resources/SubResourceIntegrityTests.cs` | 30 | `using var httpClient = new HttpClient();` |
| test | `test/OrchardCore.Tests/Modules/OrchardCore.Twitter/TwitterClientTests.cs` | 69 | `new HttpClient(_mockFakeHttpMessageHandler.Object), Mock.Of<` |

**Repos:** src, test

### HttpClient.BaseAddress (2 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.Twitter/Services/TwitterClient.cs` | 14 | `_client.BaseAddress = new Uri("https://api.twitter.com");` |
| src | `src/OrchardCore/OrchardCore.Sms.Core/ServiceCollectionExtensions.cs` | 48 | `client.BaseAddress = new Uri("https://api.twilio.com/2010-04` |

**Repos:** src

## Cache

### Redis (12 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.Redis/Startup.cs` | 19 | `using StackExchange.Redis;` |
| src | `src/OrchardCore.Modules/OrchardCore.Redis/Services/RedisDatabaseFactory.cs` | 4 | `using StackExchange.Redis;` |
| src | `src/OrchardCore.Modules/OrchardCore.Redis/Services/RedisLock.cs` | 6 | `using StackExchange.Redis;` |
| src | `src/OrchardCore.Modules/OrchardCore.Redis/Services/RedisCacheWrapper.cs` | 3 | `using StackExchange.Redis;` |
| src | `src/OrchardCore.Modules/OrchardCore.Redis/Services/RedisCacheWrapper.cs` | 8 | `/// Wrapper preventing the <see cref="RedisCache"/> to dispo` |
| src | `src/OrchardCore.Modules/OrchardCore.Redis/Services/RedisBus.cs` | 5 | `using StackExchange.Redis;` |
| src | `src/OrchardCore.Modules/OrchardCore.Redis/Services/RedisService.cs` | 3 | `using StackExchange.Redis;` |
| src | `src/OrchardCore.Modules/OrchardCore.Redis/Services/RedisService.cs` | 18 | `public IConnectionMultiplexer Connection => Database?.Multip` |
| src | `src/OrchardCore/OrchardCore.Redis.Abstractions/IRedisDatabaseFactory.cs` | 1 | `using StackExchange.Redis;` |
| src | `src/OrchardCore/OrchardCore.Redis.Abstractions/RedisOptions.cs` | 1 | `using StackExchange.Redis;` |
| src | `src/OrchardCore/OrchardCore.Redis.Abstractions/IRedisService.cs` | 2 | `using StackExchange.Redis;` |
| src | `src/OrchardCore/OrchardCore.Redis.Abstractions/IRedisService.cs` | 10 | `IConnectionMultiplexer Connection { get; }` |

**Repos:** src

## Storage

### FileStorage (11 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.OpenId/Services/OpenIdServerService.cs` | 521 | `using var stream = File.Open(path, FileMode.Open, FileAccess` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment.Remote/Controllers/ImportRemoteInstanceController.cs` | 79 | `using (var fs = System.IO.File.Create(tempArchiveName))` |
| src | `src/OrchardCore.Modules/OrchardCore.Media/Services/ChunkFileUploadService.cs` | 157 | `true => File.Open(tempFilePath, FileMode.Open, FileAccess.Re` |
| src | `src/OrchardCore.Modules/OrchardCore.Media/Services/ChunkFileUploadService.cs` | 186 | `var stream = File.Create(tempPath);` |
| src | `src/OrchardCore.Modules/OrchardCore.Sitemaps/Cache/DefaultSitemapCacheProvider.cs` | 51 | `using var fileStream = File.Create(cachePath);` |
| src | `src/OrchardCore/OrchardCore.Data/Documents/FileDocumentStore.cs` | 122 | `using var stream = File.Create(filename);` |
| src | `src/OrchardCore/OrchardCore.Media.Core/DefaultMediaFileStoreCacheFileProvider.cs` | 64 | `using var fileStream = File.Create(cachePath);` |
| src | `src/OrchardCore/OrchardCore/Shell/Configuration/ShellsSettingsSources.cs` | 53 | `using var streamWriter = File.Create(_tenants);` |
| src | `src/OrchardCore/OrchardCore/Shell/Configuration/ShellsSettingsSources.cs` | 69 | `using var streamWriter = File.Create(_tenants);` |
| src | `src/OrchardCore/OrchardCore/Shell/Configuration/ShellConfigurationSources.cs` | 61 | `using var streamWriter = File.Create(appsettings);` |
| src | `src/OrchardCore/OrchardCore.Deployment.Core/Services/TemporaryFileBuilder.cs` | 42 | `using var fs = File.Create(fullname, 4 * 1024, FileOptions.N` |

**Repos:** src


---

*[Back to Index](../index.md)*
