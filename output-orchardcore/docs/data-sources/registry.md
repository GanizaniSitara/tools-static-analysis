# Data Source Registry

## Summary

| Type | Occurrences |
|------|-------------|
| database | 438 |
| api | 405 |
| cache | 367 |
| config | 154 |
| storage | 29 |
| messaging | 1 |

## Database

### Dapper.Query (261 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.Queries/Sql/Controllers/AdminController.cs` | 95 | `model.Documents = await connection.QueryAsync(rawQuery, para` |
| src | `src/OrchardCore.Modules/OrchardCore.Queries/Sql/SqlQuerySource.cs` | 84 | `var queryResults = await connection.QueryAsync(rawQuery, par` |
| src | `src/OrchardCore.Modules/OrchardCore.Queries/Razor/ContentQueryOrchardRazorHelperExtensions.cs` | 17 | `var results = await orchardHelper.QueryAsync(queryName, para` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/DeploymentPlanController.cs` | 76 | `var deploymentPlans = _session.Query<DeploymentPlan, Deploym` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/DeploymentPlanController.cs` | 135 | `var checkedItems = await _session.Query<DeploymentPlan, Depl` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/DeploymentPlanService.cs` | 30 | `var deploymentPlanQuery = _session.Query<DeploymentPlan, Dep` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/DeploymentPlanService.cs` | 93 | `var existingDeploymentPlans = (await _session.Query<Deployme` |
| src | `src/OrchardCore.Modules/OrchardCore.AuditTrail/Controllers/AdminController.cs` | 82 | `var result = await _auditTrailAdminListQueryService.QueryAsy` |
| src | `src/OrchardCore.Modules/OrchardCore.AuditTrail/Services/DefaultAuditTrailAdminListFilterProvider.cs` | 146 | `return sortOption.Query(val, query, ctx);` |
| src | `src/OrchardCore.Modules/OrchardCore.AuditTrail/Services/DefaultAuditTrailAdminListFilterProvider.cs` | 149 | `return options.DefaultSortOption.Query(val, query, ctx);` |
| src | `src/OrchardCore.Modules/OrchardCore.AuditTrail/Services/AuditTrailManager.cs` | 109 | `_session.Query<AuditTrailEvent, AuditTrailEventIndex>(collec` |
| src | `src/OrchardCore.Modules/OrchardCore.AuditTrail/Services/AuditTrailManager.cs` | 117 | `var events = await _session.Query<AuditTrailEvent, AuditTrai` |
| src | `src/OrchardCore.Modules/OrchardCore.AuditTrail/Services/DefaultAuditTrailAdminListQueryService.cs` | 43 | `var query = _session.Query<AuditTrailEvent>(collection: Audi` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Settings/TaxonomyContentsAdminListSettingsDisplayDriver.cs` | 43 | `var taxonomies = await _session.Query<ContentItem, ContentIt` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Helper/TaxonomyOrchardHelperExtensions.cs` | 64 | `var contentItems = await query(session.Query<ContentItem, Ta` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Drivers/TermPartContentDriver.cs` | 72 | `var query = await _contentsTaxonomyListQueryService.QueryAsy` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Controllers/WorkflowController.cs` | 116 | `var workflowsQuery = _session.Query<Workflow, WorkflowIndex>` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Controllers/WorkflowController.cs` | 310 | `var checkedEntries = await _session.Query<Workflow, Workflow` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Controllers/WorkflowTypeController.cs` | 99 | `var query = _session.Query<WorkflowType, WorkflowTypeIndex>(` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Controllers/WorkflowTypeController.cs` | 129 | `var workflowTypeIdsWithInstances = (await connection.QueryAs` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Controllers/WorkflowTypeController.cs` | 184 | `var checkedEntries = await _session.Query<WorkflowType, Work` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Trimming/Services/WorkflowTrimmingService.cs` | 50 | `.Query<Workflow, WorkflowIndex>(x => x.WorkflowStatus.IsIn(s` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Http/Services/WorkflowInstanceRouteEntries.cs` | 17 | `var workflowTypeDictionary = (await Session.Query<WorkflowTy` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Http/Services/WorkflowInstanceRouteEntries.cs` | 26 | `.Query<Workflow, WorkflowBlockingActivitiesIndex>(index =>` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Http/Services/WorkflowTypeRouteEntries.cs` | 17 | `var workflowTypeDictionary = (await Session.Query<WorkflowTy` |

*... and 236 more*

**Repos:** src, test

### Dapper.Execute (118 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.AuditTrail/Services/DefaultAuditTrailAdminListQueryService.cs` | 45 | `query = await options.FilterResult.ExecuteAsync(new AuditTra` |
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Services/WorkflowManager.cs` | 430 | `result = await activityContext.Activity.ExecuteAsync(workflo` |
| src | `src/OrchardCore.Modules/OrchardCore.Users/Migrations.cs` | 274 | `await transaction.Connection.ExecuteAsync(updateCmd, null, t` |
| src | `src/OrchardCore.Modules/OrchardCore.Users/Services/DefaultUsersAdminListQueryService.cs` | 64 | `query = await options.FilterResult.ExecuteAsync(new UserQuer` |
| src | `src/OrchardCore.Modules/OrchardCore.AdminDashboard/Migrations.cs` | 35 | `await _recipeMigrator.ExecuteAsync($"dashboard-widgets{Recip` |
| src | `src/OrchardCore.Modules/OrchardCore.AdminDashboard/Migrations.cs` | 43 | `await _recipeMigrator.ExecuteAsync($"dashboard-widgets{Recip` |
| src | `src/OrchardCore.Modules/OrchardCore.Menu/Migrations.cs` | 26 | `await _recipeMigrator.ExecuteAsync($"menu{RecipesConstants.R` |
| src | `src/OrchardCore.Modules/OrchardCore.Menu/Migrations.cs` | 36 | `await _recipeMigrator.ExecuteAsync($"content-menu-updatefrom` |
| src | `src/OrchardCore.Modules/OrchardCore.Menu/Migrations.cs` | 45 | `await _recipeMigrator.ExecuteAsync($"html-menu-updatefrom2{R` |
| src | `src/OrchardCore.Modules/OrchardCore.Contents/Deployment/ExportContentToDeploymentTarget/ExportContentToDeploymentTargetMigrations.cs` | 29 | `await _recipeMigrator.ExecuteAsync($"exportcontenttodeployme` |
| src | `src/OrchardCore.Modules/OrchardCore.Contents/Services/DefaultContentsAdminListQueryService.cs` | 84 | `query = await model.FilterResult.ExecuteAsync(new ContentQue` |
| src | `src/OrchardCore.Modules/OrchardCore.Facebook/Widgets/WidgetMigrations.cs` | 29 | `await _recipeMigrator.ExecuteAsync($"Widgets/migration{Recip` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Lucene/Migrations.cs` | 200 | `await transaction.Connection.ExecuteAsync(updateCmd, null, t` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Lucene/Migrations.cs` | 204 | `await transaction.Connection.ExecuteAsync(updateCmd, null, t` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Lucene/Migrations.cs` | 208 | `await transaction.Connection.ExecuteAsync(updateCmd, null, t` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Lucene/Migrations.cs` | 212 | `await transaction.Connection.ExecuteAsync(updateCmd, null, t` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Lucene/Migrations.cs` | 216 | `await transaction.Connection.ExecuteAsync(updateCmd, null, t` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Lucene/Migrations.cs` | 220 | `await transaction.Connection.ExecuteAsync(updateCmd, null, t` |
| src | `src/OrchardCore.Modules/OrchardCore.Seo/Migrations.cs` | 40 | `await _recipeMigrator.ExecuteAsync("socialmetasettings.recip` |
| src | `src/OrchardCore.Modules/OrchardCore.Seo/Migrations.cs` | 47 | `await _recipeMigrator.ExecuteAsync($"socialmetasettings{Reci` |
| src | `src/OrchardCore.Modules/OrchardCore.Recipes/Controllers/AdminController.cs` | 111 | `await _recipeExecutor.ExecuteAsync(executionId, recipe, envi` |
| src | `src/OrchardCore.Modules/OrchardCore.Recipes/RecipeSteps/CommandStep.cs` | 45 | `await _commandManager.ExecuteAsync(commandParameters);` |
| src | `src/OrchardCore.Modules/OrchardCore.Recipes/Services/RecipeDeploymentTargetHandler.cs` | 44 | `await _recipeExecutor.ExecuteAsync(executionId, recipeDescri` |
| src | `src/OrchardCore.Modules/OrchardCore.Apis.GraphQL/GraphQLMiddleware.cs` | 146 | `var result = await _executer.ExecuteAsync(options =>` |
| src | `src/OrchardCore.Modules/OrchardCore.Indexing/Migrations.cs` | 83 | `await connection.ExecuteAsync(originalTableQuery, new` |

*... and 93 more*

**Repos:** src, test

### SQL.Select (42 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.Queries/Sql/ViewModels/AdminQueryViewModel.cs` | 7 | `public static string MatchAllQueryBase64 { get; } = Convert.` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 49 | `[InlineData("select a from t", "SELECT [a] FROM [tp_t];")]` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 50 | `[InlineData("SELECT a FROM t", "SELECT [a] FROM [tp_t];")]` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 51 | `[InlineData("SELECT a FROM t as t1", "SELECT [a] FROM [tp_t]` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 52 | `[InlineData("SELECT a FROM t1, t2", "SELECT [a] FROM [tp_t1]` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 93 | `[InlineData("select a where b = (select Avg(c) from d)", "SE` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 123 | `[InlineData("select a from b inner join c on b.b1 = c.c1", "` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 124 | `[InlineData("select a from b as ba inner join c as ca on ba.` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 125 | `[InlineData("select a from b inner join c on b.b1 = c.c1 lef` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 126 | `[InlineData("select a from b inner join c on b.b1 = c.c1 and` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 127 | `[InlineData("select a from b inner join c on b.b1 = c.c1 and` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 128 | `[InlineData("select a from b inner join c on 1 = 1 and @para` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 129 | `[InlineData("select a from b inner join c on 1 = @param left` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 141 | `[InlineData("select a from b as b1 order by b1.c", "SELECT [` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 166 | `[InlineData("select count(a) from b as b1 group by b1.c", "S` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 199 | `[InlineData("select COUNT(1) over () from a", "SELECT COUNT(` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 200 | `[InlineData("select COUNT(1) over () a from b", "SELECT COUN` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 201 | `[InlineData("select COUNT(1) over (partition by a) from b", ` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 202 | `[InlineData("select COUNT(1) over (order by a) from b", "SEL` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 203 | `[InlineData("select COUNT(1) over (order by a, b) from c", "` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 204 | `[InlineData("select COUNT(1) over (order by a asc, b desc, c` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 205 | `[InlineData("select COUNT(1) over (partition by a order by b` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 206 | `[InlineData("select COUNT(1) over () a, MAX(b) over () c fro` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 215 | `[InlineData("select a from b union select c from d", "SELECT` |
| test | `test/OrchardCore.Tests/Orchard.Queries/SqlParserTests.cs` | 216 | `[InlineData("select a from b union all select c from d", "SE` |

*... and 17 more*

**Repos:** src, test

### MongoDB.Read (7 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.OpenId/Controllers/AccessController.cs` | 110 | `var authorizations = await _authorizationManager.FindAsync(` |
| src | `src/OrchardCore.Modules/OrchardCore.OpenId/Controllers/AccessController.cs` | 222 | `var authorizations = await _authorizationManager.FindAsync(` |
| src | `src/OrchardCore.Modules/OrchardCore.OpenId/Controllers/AccessController.cs` | 506 | `var authorizations = await _authorizationManager.FindAsync(` |
| src | `src/OrchardCore.Modules/OrchardCore.OpenId/Services/OpenIdServerService.cs` | 467 | `var certificates = store.Certificates.Find(X509FindType.Find` |
| src | `src/OrchardCore.Modules/OrchardCore.Placements/Services/PlacementProvider.cs` | 56 | `predicate = filters.Aggregate(predicate, BuildPredicate);` |
| src | `src/OrchardCore/OrchardCore.DisplayManagement/Descriptors/ShapePlacementStrategy/ShapePlacementParsingStrategy.cs` | 81 | `predicate = matches.Aggregate(predicate, BuildPredicate);` |
| src | `src/OrchardCore/OrchardCore.DisplayManagement/BaseDisplayManager.cs` | 54 | `return placementResolvers.Aggregate<IPlacementInfoResolver, ` |

**Repos:** src

### EntityFramework (5 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore/OrchardCore.Data.YesSql/OrchardCoreBuilderExtensions.cs` | 76 | `.UseSqlServer(shellSettings["ConnectionString"], yesSqlOptio` |
| src | `src/OrchardCore/OrchardCore.Data.YesSql/OrchardCoreBuilderExtensions.cs` | 94 | `.UseMySql(shellSettings["ConnectionString"], yesSqlOptions.I` |
| test | `test/OrchardCore.Tests/Apis/GraphQL/Queries/PredicateQueryTests.cs` | 17 | `.UseSqlServer("Fake database connection string for testing;"` |
| test | `test/OrchardCore.Tests/Apis/GraphQL/Queries/PredicateQueryTests.cs` | 86 | `.UseMySql("Fake database connection string for testing;", "T` |
| test | `test/OrchardCore.Tests/Apis/GraphQL/Queries/PredicateQueryTests.cs` | 98 | `.UseSqlServer("Fake database connection string for testing;"` |

**Repos:** src, test

### SQL.Delete (4 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore/OrchardCore.OpenId.Core/YesSql/Migrations/OpenIdMigrations.cs` | 378 | `// Delete from the original collection.` |
| src | `src/OrchardCore/OrchardCore.OpenId.Core/YesSql/Migrations/OpenIdMigrations.cs` | 389 | `// Delete from the original collection.` |
| src | `src/OrchardCore/OrchardCore.OpenId.Core/YesSql/Migrations/OpenIdMigrations.cs` | 481 | `// Delete from the original collection.` |
| src | `src/OrchardCore/OrchardCore.OpenId.Core/YesSql/Migrations/OpenIdMigrations.cs` | 492 | `// Delete from the original collection.` |

**Repos:** src

### SqlClient (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore/OrchardCore.Data.YesSql/DbConnectionValidator.cs` | 1 | `using Microsoft.Data.SqlClient;` |

**Repos:** src

## Api

### API.HttpPost (206 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.Queries/Controllers/AdminController.cs` | 108 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.Queries/Controllers/AdminController.cs` | 140 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.Queries/Controllers/AdminController.cs` | 197 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.Queries/Controllers/AdminController.cs` | 235 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.Queries/Controllers/AdminController.cs` | 253 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.Queries/Sql/Controllers/AdminController.cs` | 57 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.AdminMenu/Controllers/MenuController.cs` | 134 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.AdminMenu/Controllers/MenuController.cs` | 178 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.AdminMenu/Controllers/MenuController.cs` | 208 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.AdminMenu/Controllers/MenuController.cs` | 272 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.AdminMenu/Controllers/NodeController.cs` | 115 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.AdminMenu/Controllers/NodeController.cs` | 195 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.AdminMenu/Controllers/NodeController.cs` | 246 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.AdminMenu/Controllers/NodeController.cs` | 281 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.AdminMenu/Controllers/NodeController.cs` | 313 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/DeploymentPlanController.cs` | 208 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/DeploymentPlanController.cs` | 266 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/DeploymentPlanController.cs` | 312 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/ExportFileController.cs` | 32 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/StepController.cs` | 81 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/StepController.cs` | 158 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/StepController.cs` | 197 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/StepController.cs` | 228 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/ImportController.cs` | 57 | `[HttpPost]` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/ImportController.cs` | 140 | `[HttpPost]` |

*... and 181 more*

**Repos:** src

### API.Controller (105 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Themes/TheTheme/Controllers/HomeController.cs` | 5 | `public sealed class HomeController : Controller` |
| src | `src/Templates/OrchardCore.ProjectTemplates/content/OrchardCore.Templates.Mvc.Module/Controllers/HomeController.cs` | 10 | `public sealed class HomeController : Controller` |
| src | `src/Templates/OrchardCore.ProjectTemplates/content/OrchardCore.Templates.Cms.Module/Controllers/HomeController.cs` | 10 | `public sealed class HomeController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.Queries/Controllers/AdminController.cs` | 21 | `public sealed class AdminController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.Queries/Controllers/QueryApiController.cs` | 14 | `public sealed class QueryApiController : ControllerBase` |
| src | `src/OrchardCore.Modules/OrchardCore.Queries/Sql/Controllers/AdminController.cs` | 19 | `public sealed class AdminController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.AdminMenu/Controllers/MenuController.cs` | 20 | `public sealed class MenuController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.AdminMenu/Controllers/NodeController.cs` | 15 | `public sealed class NodeController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/DeploymentPlanController.cs` | 22 | `public sealed class DeploymentPlanController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/ExportFileController.cs` | 16 | `public sealed class ExportFileController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/StepController.cs` | 14 | `public sealed class StepController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/ImportController.cs` | 20 | `public sealed class ImportController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.Shortcodes/Controllers/AdminController.cs` | 25 | `public sealed class AdminController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.AuditTrail/Controllers/AdminController.cs` | 18 | `public sealed class AdminController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.ContentPreview/Controllers/PreviewController.cs` | 14 | `public sealed class PreviewController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.BackgroundTasks/Controllers/BackgroundTaskController.cs` | 20 | `public sealed class BackgroundTaskController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.Settings/Controllers/AdminController.cs` | 16 | `public sealed class AdminController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.Features/Controllers/AdminController.cs` | 18 | `public sealed class AdminController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.Media.Azure/Controllers/AdminController.cs` | 12 | `public sealed class AdminController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Controllers/AdminController.cs` | 19 | `public sealed class AdminController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Controllers/TagController.cs` | 15 | `public sealed class TagController : Controller, IUpdateModel` |
| src | `src/OrchardCore.Modules/OrchardCore.Setup/Controllers/SetupController.cs` | 19 | `public sealed class SetupController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.Flows/Controllers/AdminController.cs` | 15 | `public sealed class AdminController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.XmlRpc/Controllers/MetaWeblogController.cs` | 9 | `public sealed class MetaWeblogController : Controller` |
| src | `src/OrchardCore.Modules/OrchardCore.XmlRpc/Controllers/HomeController.cs` | 10 | `public sealed class HomeController : Controller` |

*... and 80 more*

**Repos:** src

### API.Route (25 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.Queries/Controllers/QueryApiController.cs` | 9 | `[Route("api/queries")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Queries/Controllers/QueryApiController.cs` | 29 | `[Route("{name}")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Elasticsearch/Controllers/ElasticsearchApiController.cs` | 12 | `[Route("api/elasticsearch")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Elasticsearch/Controllers/ElasticsearchApiController.cs` | 29 | `[Route("content")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Elasticsearch/Controllers/ElasticsearchApiController.cs` | 43 | `[Route("content")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Elasticsearch/Controllers/ElasticsearchApiController.cs` | 57 | `[Route("documents")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Elasticsearch/Controllers/ElasticsearchApiController.cs` | 71 | `[Route("documents")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Lucene/Controllers/LuceneApiController.cs` | 10 | `[Route("api/lucene")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Lucene/Controllers/LuceneApiController.cs` | 29 | `[Route("content")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Lucene/Controllers/LuceneApiController.cs` | 43 | `[Route("content")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Lucene/Controllers/LuceneApiController.cs` | 57 | `[Route("documents")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Lucene/Controllers/LuceneApiController.cs` | 71 | `[Route("documents")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Search/Controllers/SearchController.cs` | 63 | `[Route("search/{index?}")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Demo/Controllers/DemoController.cs` | 7 | `[Route("Demo")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Demo/Controllers/DemoController.cs` | 8 | `[Route("Demo/Index")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Demo/Controllers/DemoController.cs` | 13 | `[Route("Demo/About")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Demo/Controllers/DemoController.cs` | 18 | `[Route("Demo/Contact")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Demo/Controllers/ContentApiController.cs` | 8 | `[Route("api/demo")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Tenants/Controllers/TenantApiController.cs` | 27 | `[Route("api/tenants")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Tenants/Controllers/TenantApiController.cs` | 84 | `[Route("create")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Tenants/Controllers/TenantApiController.cs` | 144 | `[Route("edit")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Tenants/Controllers/TenantApiController.cs` | 194 | `[Route("disable/{tenantName}")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Tenants/Controllers/TenantApiController.cs` | 223 | `[Route("enable/{tenantName}")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Tenants/Controllers/TenantApiController.cs` | 252 | `[Route("remove/{tenantName}")]` |
| src | `src/OrchardCore.Modules/OrchardCore.Tenants/Controllers/TenantApiController.cs` | 293 | `[Route("setup")]` |

**Repos:** src

### API.HttpGet (18 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.Workflows/Http/Controllers/HttpWorkflowController.cs` | 215 | `[HttpGet]` |
| src | `src/OrchardCore.Modules/OrchardCore.Users/Controllers/AccountController.cs` | 236 | `[HttpGet]` |
| src | `src/OrchardCore.Modules/OrchardCore.Users/Controllers/ChangeEmailController.cs` | 35 | `[HttpGet]` |
| src | `src/OrchardCore.Modules/OrchardCore.Users/Controllers/ChangeEmailController.cs` | 84 | `[HttpGet]` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Elasticsearch/Controllers/ElasticsearchApiController.cs` | 28 | `[HttpGet]` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Elasticsearch/Controllers/ElasticsearchApiController.cs` | 56 | `[HttpGet]` |
| src | `src/OrchardCore.Modules/OrchardCore.ContentFields/Controllers/LocalizationSetContentPickerAdminController.cs` | 45 | `[HttpGet]` |
| src | `src/OrchardCore.Modules/OrchardCore.OpenId/Controllers/ScopeController.cs` | 74 | `[HttpGet]` |
| src | `src/OrchardCore.Modules/OrchardCore.OpenId/Controllers/ApplicationController.cs` | 93 | `[HttpGet]` |
| src | `src/OrchardCore.Modules/OrchardCore.DataLocalization/Controllers/AdminController.cs` | 88 | `[HttpGet]` |
| src | `src/OrchardCore.Modules/OrchardCore.DataLocalization/Controllers/AdminController.cs` | 106 | `[HttpGet]` |
| src | `src/OrchardCore.Modules/OrchardCore.DataLocalization/Controllers/AdminController.cs` | 153 | `[HttpGet]` |
| src | `src/OrchardCore.Modules/OrchardCore.Contents/Deployment/Download/DownloadController.cs` | 27 | `[HttpGet]` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Lucene/Controllers/LuceneApiController.cs` | 28 | `[HttpGet]` |
| src | `src/OrchardCore.Modules/OrchardCore.Search.Lucene/Controllers/LuceneApiController.cs` | 56 | `[HttpGet]` |
| src | `src/OrchardCore.Modules/OrchardCore.Apis.GraphQL/Controllers/AdminController.cs` | 8 | `[HttpGet]` |
| src | `src/OrchardCore.Modules/OrchardCore.Cors/Controllers/AdminController.cs` | 43 | `[HttpGet]` |
| src | `src/OrchardCore.Modules/OrchardCore.ContentLocalization/Controllers/ContentCulturePickerController.cs` | 29 | `[HttpGet]` |

**Repos:** src

### HttpClient.PostAsync (15 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| test | `test/OrchardCore.Tests/Apis/ContentManagement/DeploymentPlans/BlogPostUpdateDeploymentPlanTests.cs` | 47 | `var content = await context.Client.PostAsJsonAsync("api/cont` |
| test | `test/OrchardCore.Tests/Apis/ContentManagement/DeploymentPlans/BlogPostUpdateDeploymentPlanTests.cs` | 85 | `var content = await context.Client.PostAsJsonAsync("api/cont` |
| test | `test/OrchardCore.Tests/Apis/ContentManagement/DeploymentPlans/BlogPostCreateDeploymentPlanTests.cs` | 57 | `var content = await context.Client.PostAsJsonAsync("api/cont` |
| test | `test/OrchardCore.Tests/Apis/ContentManagement/DeploymentPlans/BlogPostCreateDeploymentPlanTests.cs` | 100 | `var content = await context.Client.PostAsJsonAsync("api/cont` |
| test | `test/OrchardCore.Tests/Apis/ContentManagement/ContentApiController/BlogPostApiControllerTests.cs` | 25 | `var content = await context.Client.PostAsJsonAsync("api/cont` |
| test | `test/OrchardCore.Tests/Apis/ContentManagement/ContentApiController/BlogPostApiControllerTests.cs` | 45 | `var content = await context.Client.PostAsJsonAsync("api/cont` |
| test | `test/OrchardCore.Tests/Apis/ContentManagement/ContentApiController/BlogPostApiControllerTests.cs` | 65 | `await context.Client.PostAsJsonAsync("api/content", context.` |
| test | `test/OrchardCore.Tests/Apis/ContentManagement/ContentApiController/BlogPostApiControllerTests.cs` | 124 | `var content = await context.Client.PostAsJsonAsync("api/cont` |
| test | `test/OrchardCore.Tests/Apis/ContentManagement/ContentApiController/BlogPostApiControllerTests.cs` | 181 | `var content = await context.Client.PostAsJsonAsync("api/cont` |
| test | `test/OrchardCore.Tests/Apis/ContentManagement/ContentApiController/BlogPostApiControllerTests.cs` | 236 | `var result = await context.Client.PostAsJsonAsync("api/conte` |
| test | `test/OrchardCore.Tests/Apis/ContentManagement/ContentApiController/BlogPostApiControllerTests.cs` | 292 | `var content = await context.Client.PostAsJsonAsync("api/cont` |
| test | `test/OrchardCore.Tests/Apis/Context/BlogPostDeploymentContext.cs` | 89 | `var response = await Client.PostAsync("OrchardCore.Deploymen` |
| test | `test/OrchardCore.Tests/Apis/Context/SiteContext.cs` | 58 | `var createResult = await DefaultTenantClient.PostAsJsonAsync` |
| test | `test/OrchardCore.Tests/Apis/Context/SiteContext.cs` | 79 | `var setupResult = await DefaultTenantClient.PostAsJsonAsync(` |
| test | `test/OrchardCore.Tests/Apis/Context/SiteContext.cs` | 188 | `var content = await Client.PostAsJsonAsync("api/content" + (` |

**Repos:** test

### HttpClient.GetAsync (13 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| test | `test/OrchardCore.Tests/Modules/OrchardCore.Users/AccountControllerTests.cs` | 31 | `var responseFromGet = await context.Client.GetAsync("Registe` |
| test | `test/OrchardCore.Tests/Modules/OrchardCore.Users/AccountControllerTests.cs` | 170 | `var responseFromGet = await context.Client.GetAsync("Registe` |
| test | `test/OrchardCore.Tests/Modules/OrchardCore.Users/AccountControllerTests.cs` | 207 | `var response = await context.Client.GetAsync("Register", Tes` |
| test | `test/OrchardCore.Tests/Modules/OrchardCore.Users/AccountControllerTests.cs` | 220 | `var response = await context.Client.GetAsync("Register", Tes` |
| test | `test/OrchardCore.Tests/Modules/OrchardCore.Users/AccountControllerTests.cs` | 232 | `var responseFromGet = await context.Client.GetAsync("Registe` |
| test | `test/OrchardCore.Tests/Modules/OrchardCore.Users/AccountControllerTests.cs` | 251 | `var responseFromGet2 = await context.Client.GetAsync("Regist` |
| test | `test/OrchardCore.Tests/Modules/OrchardCore.Users/AccountControllerTests.cs` | 277 | `var responseFromGet = await context.Client.GetAsync("Registe` |
| test | `test/OrchardCore.Tests/Modules/OrchardCore.Users/AccountControllerTests.cs` | 295 | `var responseFromGet2 = await context.Client.GetAsync("Regist` |
| test | `test/OrchardCore.Tests/Modules/OrchardCore.Users/AccountControllerTests.cs` | 325 | `var responseFromGet = await context.Client.GetAsync("Registe` |
| test | `test/OrchardCore.Tests/Modules/OrchardCore.Users/AccountControllerTests.cs` | 365 | `var responseFromGet = await context.Client.GetAsync("Registe` |
| test | `test/OrchardCore.Tests/Modules/OrchardCore.OpenId/OpenIdAuthenticationTests.cs` | 92 | `var loginGetRequest = await httpClient.GetAsync("Login", Can` |
| test | `test/OrchardCore.Tests/Modules/OrchardCore.OpenId/OpenIdAuthenticationTests.cs` | 252 | `var loginGetRequest = await httpClient.GetAsync("Login", Can` |
| test | `test/OrchardCore.Tests/Apis/GraphQL/Blog/BlogPostTests.cs` | 210 | `var response = await context.GraphQLClient.Client.GetAsync("` |

**Repos:** test

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

### API.MapPost (5 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.Users/Endpoints/SmsAuthenticator/SendCode.cs` | 22 | `builder.MapPost("TwoFactor-Authenticator/SmsSendCode", Handl` |
| src | `src/OrchardCore.Modules/OrchardCore.Users/Endpoints/EmailAuthenticator/SendCode.cs` | 21 | `builder.MapPost("TwoFactor-Authenticator/EmailSendCode", Han` |
| src | `src/OrchardCore.Modules/OrchardCore.Notifications/Endpoints/Management/MarkAsReadEndpoints.cs` | 22 | `builder.MapPost("Notifications/MarkAsRead", HandleAsync)` |
| src | `src/OrchardCore.Modules/OrchardCore.Contents/Endpoints/Api/CreateEndpoint.cs` | 26 | `builder.MapPost("api/content", HandleAsync)` |
| src | `src/OrchardCore.Modules/OrchardCore.UrlRewriting/Endpoints/Rules/SortRulesEndpoint.cs` | 14 | `builder.MapPost("url-rewriting/resort", HandleAsync)` |

**Repos:** src

### API.MapGet (4 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.Liquid/Endpoints/Scripts/GetIntellisenseEndpoint.cs` | 22 | `builder.MapGet("OrchardCore.Liquid/Scripts/liquid-intellisen` |
| src | `src/OrchardCore.Modules/OrchardCore.Contents/Endpoints/Api/GetEndpoint.cs` | 16 | `builder.MapGet("api/content/{contentItemId}", HandleAsync)` |
| src | `src/OrchardCore.Modules/OrchardCore.Facebook/Endpoints/GetSdkEndpoints.cs` | 19 | `builder.MapGet("/OrchardCore.Facebook/sdk/init.js", GetInitS` |
| src | `src/OrchardCore.Modules/OrchardCore.Facebook/Endpoints/GetSdkEndpoints.cs` | 23 | `builder.MapGet("/OrchardCore.Facebook/sdk/sdk.{culture:lengt` |

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

### API.MapDelete (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.Contents/Endpoints/Api/DeleteEndpoint.cs` | 16 | `builder.MapDelete("api/content/{contentItemId}", HandleAsync` |

**Repos:** src

### HttpClient.DeleteAsync (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| test | `test/OrchardCore.Tests/Apis/Context/SiteContext.cs` | 196 | `return Client.DeleteAsync("api/content/" + contentItemId);` |

**Repos:** test

## Cache

### Redis.Read (234 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.Features/Services/ModuleService.cs` | 104 | `//    DateTime lastWrittenUtc = _cacheManager.Get(extensionD` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Controllers/AdminController.cs` | 106 | `taxonomy = await _contentManager.GetAsync(taxonomyContentIte` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Controllers/AdminController.cs` | 110 | `taxonomy = await _contentManager.GetAsync(taxonomyContentIte` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Controllers/AdminController.cs` | 171 | `var taxonomy = await _contentManager.GetAsync(taxonomyConten` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Controllers/AdminController.cs` | 224 | `taxonomy = await _contentManager.GetAsync(taxonomyContentIte` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Controllers/AdminController.cs` | 228 | `taxonomy = await _contentManager.GetAsync(taxonomyContentIte` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Controllers/AdminController.cs` | 299 | `taxonomy = await _contentManager.GetAsync(taxonomyContentIte` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Controllers/AdminController.cs` | 303 | `taxonomy = await _contentManager.GetAsync(taxonomyContentIte` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Controllers/TagController.cs` | 51 | `var taxonomy = await _contentManager.GetAsync(taxonomyConten` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/GraphQL/TaxonomyFieldQueryObjectType.cs` | 41 | `var taxonomy = await contentManager.GetAsync(x.Source.Taxono` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/GraphQL/TaxonomyFieldQueryObjectType.cs` | 68 | `return await contentManager.GetAsync(context.Source.Taxonomy` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Liquid/InheritedTermsFilter.cs` | 27 | `taxonomy = await _contentManager.GetAsync(firstArg.ToStringV` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Liquid/TaxonomyTermsFilter.cs` | 47 | `var taxonomy = await _contentManager.GetAsync(taxonomyConten` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Indexing/TaxonomyFieldIndexHandler.cs` | 37 | `var taxonomy = await contentManager.GetAsync(field.TaxonomyC` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Helper/TaxonomyOrchardHelperExtensions.cs` | 22 | `var taxonomy = await contentManager.GetAsync(taxonomyContent` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Helper/TaxonomyOrchardHelperExtensions.cs` | 42 | `var taxonomy = await contentManager.GetAsync(taxonomyContent` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Drivers/TaxonomyContentsAdminListDisplayDriver.cs` | 66 | `var taxonomies = await _contentManager.GetAsync(taxonomyCont` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Drivers/TaxonomyFieldTagsDisplayDriver.cs` | 46 | `model.Taxonomy = await _contentManager.GetAsync(settings.Tax` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Drivers/TaxonomyFieldTagsDisplayDriver.cs` | 100 | `var taxonomy = await _contentManager.GetAsync(settings.Taxon` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Drivers/TaxonomyFieldDisplayDriver.cs` | 44 | `model.Taxonomy = await _contentManager.GetAsync(settings.Tax` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/TermShapes.cs` | 67 | `var taxonomyContentItem = await contentManager.GetAsync(taxo` |
| src | `src/OrchardCore.Modules/OrchardCore.XmlRpc/Controllers/MetaWeblogController.cs` | 33 | `XName.Get("options", ManifestUri),` |
| src | `src/OrchardCore.Modules/OrchardCore.XmlRpc/Controllers/MetaWeblogController.cs` | 34 | `new XElement(XName.Get("supportsAutoUpdate", ManifestUri), "` |
| src | `src/OrchardCore.Modules/OrchardCore.XmlRpc/Controllers/MetaWeblogController.cs` | 35 | `new XElement(XName.Get("clientType", ManifestUri), "MetaWebl` |
| src | `src/OrchardCore.Modules/OrchardCore.XmlRpc/Controllers/MetaWeblogController.cs` | 36 | `new XElement(XName.Get("supportsKeywords", ManifestUri), "No` |

*... and 209 more*

**Repos:** src, test

### Redis.Write (121 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.ContentPreview/Controllers/PreviewController.cs` | 53 | `HttpContext.Features.Set(new ContentPreviewFeature());` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Indexing/TaxonomyFieldIndexHandler.cs` | 31 | `context.DocumentIndex.Set(key + ContentIndexingConstants.Ids` |
| src | `src/OrchardCore.Modules/OrchardCore.Taxonomies/Indexing/TaxonomyFieldIndexHandler.cs` | 49 | `context.DocumentIndex.Set(key + ContentIndexingConstants.Inh` |
| src | `src/OrchardCore.Modules/OrchardCore.Flows/Handlers/BagPartDocumentIndexHandler.cs` | 16 | `context.DocumentIndex.Set(context.ContentTypePartDefinition.` |
| src | `src/OrchardCore.Modules/OrchardCore.XmlRpc/Services/XmlRpcWriter.cs` | 51 | `members.Set("faultCode", rpcMethodResponse.Fault.Code);` |
| src | `src/OrchardCore.Modules/OrchardCore.XmlRpc/Services/XmlRpcWriter.cs` | 52 | `members.Set("faultString", rpcMethodResponse.Fault.Message);` |
| src | `src/OrchardCore.Modules/OrchardCore.Users/Controllers/TwoFactorAuthenticationBaseController.cs` | 65 | `await DistributedCache.SetAsync(key, data,` |
| src | `src/OrchardCore.Modules/OrchardCore.Users/Controllers/SmsAuthenticatorController.cs` | 222 | `await DistributedCache.SetAsync(key, data,` |
| src | `src/OrchardCore.Modules/OrchardCore.DynamicCache/Services/DefaultDynamicCache.cs` | 26 | `return _distributedCache.SetAsync(key, value, options);` |
| src | `src/OrchardCore.Modules/OrchardCore.DynamicCache/Services/DefaultDynamicCacheService.cs` | 118 | `await _dynamicCache.SetAsync(cacheKey, bytes, options);` |
| src | `src/OrchardCore.Modules/OrchardCore.DynamicCache/Services/DefaultDynamicCacheService.cs` | 124 | `_memoryCache.Set(FailoverKey, true, new MemoryCacheEntryOpti` |
| src | `src/OrchardCore.Modules/OrchardCore.DynamicCache/Services/DefaultDynamicCacheService.cs` | 184 | `_memoryCache.Set(FailoverKey, true, new MemoryCacheEntryOpti` |
| src | `src/OrchardCore.Modules/OrchardCore.ContentFields/Indexing/TimeFieldIndexHandler.cs` | 20 | `context.DocumentIndex.Set(key, indexedValue, options);` |
| src | `src/OrchardCore.Modules/OrchardCore.ContentFields/Indexing/UserPickerFieldIndexHandler.cs` | 19 | `context.DocumentIndex.Set(key, userId, options);` |
| src | `src/OrchardCore.Modules/OrchardCore.ContentFields/Indexing/UserPickerFieldIndexHandler.cs` | 28 | `context.DocumentIndex.Set(key, userName, options);` |
| src | `src/OrchardCore.Modules/OrchardCore.ContentFields/Indexing/UserPickerFieldIndexHandler.cs` | 36 | `context.DocumentIndex.Set(key, ContentIndexingConstants.Null` |
| src | `src/OrchardCore.Modules/OrchardCore.ContentFields/Indexing/DateFieldIndexHandler.cs` | 14 | `context.DocumentIndex.Set(key, field.Value, options);` |
| src | `src/OrchardCore.Modules/OrchardCore.ContentFields/Indexing/LocalizationSetContentPickerFieldIndexHandler.cs` | 21 | `context.DocumentIndex.Set(key, localizationSet, options);` |
| src | `src/OrchardCore.Modules/OrchardCore.ContentFields/Indexing/LocalizationSetContentPickerFieldIndexHandler.cs` | 29 | `context.DocumentIndex.Set(key, ContentIndexingConstants.Null` |
| src | `src/OrchardCore.Modules/OrchardCore.ContentFields/Indexing/BooleanFieldIndexHandler.cs` | 14 | `context.DocumentIndex.Set(key, field.Value, options);` |
| src | `src/OrchardCore.Modules/OrchardCore.ContentFields/Indexing/NumericFieldIndexHandler.cs` | 20 | `context.DocumentIndex.Set(key, (int?)field.Value, options);` |
| src | `src/OrchardCore.Modules/OrchardCore.ContentFields/Indexing/NumericFieldIndexHandler.cs` | 25 | `context.DocumentIndex.Set(key, field.Value, options);` |
| src | `src/OrchardCore.Modules/OrchardCore.ContentFields/Indexing/DateTimeFieldIndexHandler.cs` | 14 | `context.DocumentIndex.Set(key, field.Value, options);` |
| src | `src/OrchardCore.Modules/OrchardCore.ContentFields/Indexing/LinkFieldIndexHandler.cs` | 14 | `context.DocumentIndex.Set(key, field.Url, options);` |
| src | `src/OrchardCore.Modules/OrchardCore.ContentFields/Indexing/LinkFieldIndexHandler.cs` | 15 | `context.DocumentIndex.Set(key, field.Text, options);` |

*... and 96 more*

**Repos:** src, test

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

## Storage

### File.Write (15 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.Deployment/Controllers/ImportController.cs` | 160 | `System.IO.File.WriteAllText(Path.Combine(tempArchiveFolder, ` |
| src | `src/OrchardCore.Modules/OrchardCore.OpenId/Services/OpenIdServerService.cs` | 655 | `await File.WriteAllBytesAsync(Path.ChangeExtension(path, ".p` |
| src | `src/OrchardCore.Modules/OrchardCore.OpenId/Services/OpenIdServerService.cs` | 656 | `await File.WriteAllTextAsync(Path.ChangeExtension(path, ".pw` |
| src | `src/OrchardCore.Modules/OrchardCore.Deployment.Remote/Controllers/ImportRemoteInstanceController.cs` | 79 | `using (var fs = System.IO.File.Create(tempArchiveName))` |
| src | `src/OrchardCore.Modules/OrchardCore.Media/Services/ChunkFileUploadService.cs` | 186 | `var stream = File.Create(tempPath);` |
| src | `src/OrchardCore.Modules/OrchardCore.Sitemaps/Cache/DefaultSitemapCacheProvider.cs` | 51 | `using var fileStream = File.Create(cachePath);` |
| src | `src/OrchardCore.Modules/OrchardCore.Tenants/Controllers/TenantApiController.cs` | 399 | `await System.IO.File.WriteAllTextAsync(tempFilename, model.R` |
| src | `src/OrchardCore/OrchardCore.Data/Documents/FileDocumentStore.cs` | 122 | `using var stream = File.Create(filename);` |
| src | `src/OrchardCore/OrchardCore.Search.Lucene.Core/Services/LuceneIndexingState.cs` | 59 | `await File.WriteAllTextAsync(_stateFileName, _stateDocument.` |
| src | `src/OrchardCore/OrchardCore.Search.Lucene.Core/Services/LuceneIndexingState.cs` | 87 | `await File.WriteAllTextAsync(_stateFileName, new JsonObject(` |
| src | `src/OrchardCore/OrchardCore.Media.Core/DefaultMediaFileStoreCacheFileProvider.cs` | 64 | `using var fileStream = File.Create(cachePath);` |
| src | `src/OrchardCore/OrchardCore/Shell/Configuration/ShellsSettingsSources.cs` | 53 | `using var streamWriter = File.Create(_tenants);` |
| src | `src/OrchardCore/OrchardCore/Shell/Configuration/ShellsSettingsSources.cs` | 69 | `using var streamWriter = File.Create(_tenants);` |
| src | `src/OrchardCore/OrchardCore/Shell/Configuration/ShellConfigurationSources.cs` | 61 | `using var streamWriter = File.Create(appsettings);` |
| src | `src/OrchardCore/OrchardCore.Deployment.Core/Services/TemporaryFileBuilder.cs` | 42 | `using var fs = File.Create(fullname, 4 * 1024, FileOptions.N` |

**Repos:** src

### File.Read (14 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore.Modules/OrchardCore.Media/Services/ChunkFileUploadService.cs` | 166 | `return new(File.OpenRead(tempFilePath))` |
| src | `src/OrchardCore/OrchardCore.Data/Documents/FileDocumentStore.cs` | 98 | `using var stream = File.OpenRead(filename);` |
| src | `src/OrchardCore/OrchardCore.FileStorage.FileSystem/FileSystemStore.cs` | 247 | `var stream = File.OpenRead(physicalPath);` |
| src | `src/OrchardCore/OrchardCore.FileStorage.FileSystem/FileSystemStore.cs` | 271 | `var stream = File.OpenRead(physicalPath);` |
| src | `src/OrchardCore/OrchardCore.Search.Lucene.Core/Services/LuceneIndexingState.cs` | 90 | `_stateDocument = JObject.Parse(await File.ReadAllTextAsync(_` |
| src | `src/OrchardCore/OrchardCore.Shells.Azure/Configuration/BlobShellsConfigurationSources.cs` | 80 | `using var file = File.OpenRead(fileSystemPath);` |
| src | `src/OrchardCore/OrchardCore.Shells.Azure/Configuration/BlobShellsSettingsSources.cs` | 118 | `using var file = File.OpenRead(_tenantsFileSystemName);` |
| src | `src/OrchardCore/OrchardCore.Shells.Azure/Configuration/BlobShellConfigurationSources.cs` | 111 | `using var file = File.OpenRead(tenantFile);` |
| src | `src/OrchardCore/OrchardCore.Infrastructure/Shells.Database/Configuration/DatabaseShellsSettingsSources.cs` | 149 | `using var fileStream = File.OpenRead(_tenants);` |
| src | `src/OrchardCore/OrchardCore.Infrastructure/Shells.Database/Configuration/DatabaseShellConfigurationSources.cs` | 147 | `using var stream = File.OpenRead(appsettings);` |
| src | `src/OrchardCore/OrchardCore/Shell/Configuration/ShellsSettingsSources.cs` | 30 | `using var streamReader = File.OpenRead(_tenants);` |
| src | `src/OrchardCore/OrchardCore/Shell/Configuration/ShellsSettingsSources.cs` | 62 | `using (var streamReader = File.OpenRead(_tenants))` |
| src | `src/OrchardCore/OrchardCore/Shell/Configuration/ShellConfigurationSources.cs` | 39 | `using var streamReader = File.OpenRead(appsettings);` |
| test | `test/OrchardCore.Tests/Email/EmailTests.cs` | 271 | `var content = File.ReadAllText(file.FullName);` |

**Repos:** src, test

## Messaging

### Kafka.Topic (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/OrchardCore/OrchardCore/Caching/Distributed/DistributedSignal.cs` | 23 | `public override Task ActivatedAsync() => _messageBus.Subscri` |

**Repos:** src


---

*[Back to Index](../index.md)*
