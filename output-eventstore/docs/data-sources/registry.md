# Data Source Registry

## Summary

| Type | Occurrences |
|------|-------------|
| api | 155 |
| storage | 75 |
| database | 66 |
| config | 61 |
| messaging | 13 |
| connector | 4 |

## Api

### gRPC (130 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Tests/Integration/when_node_becomes_leader_with_unindexed_data.cs` | 15 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Integration/when_node_becomes_leader_with_unindexed_data.cs` | 16 | `using Grpc.Net.Client;` |
| src | `src/KurrentDB.Core.Tests/Integration/authenticated_requests_made_from_a_follower.cs` | 16 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Integration/authenticated_requests_made_from_a_follower.cs` | 17 | `using Grpc.Net.Client;` |
| src | `src/KurrentDB.Core.Tests/Integration/authenticated_requests_made_from_a_follower.cs` | 21 | `using StatusCode = Grpc.Core.StatusCode;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/ReadIndexForwardsTests.cs` | 8 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/DeleteTests.cs` | 10 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/ReadAllBackwardsTests.cs` | 9 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/GrpcSpecification.cs` | 14 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/GrpcSpecification.cs` | 15 | `using Grpc.Net.Client;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/SubscribeToAllTests.cs` | 9 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/ReadAllForwardsTests.cs` | 9 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/ReadStreamsForwardTests.cs` | 11 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/SubscribeToAllFilteredTests.cs` | 13 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/ReadAllForwardsFilteredTests.cs` | 9 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/SubscribeToStreamTests.cs` | 8 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/ReadAllBackwardsFilteredTests.cs` | 9 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/ReadIndexBackwardsTests.cs` | 8 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/ReadStreamsBackwardTests.cs` | 10 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/TombstoneTests.cs` | 9 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/PersistentSubscriptionTests/ReplayParkedTests.cs` | 12 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/PersistentSubscriptionTests/GetInfoTests.cs` | 11 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/MonitoringTests/StatsTests.cs` | 10 | `using Grpc.Net.Client;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/ServerFeaturesTests/ServerFeaturesTest.cs` | 16 | `using Grpc.Net.Client;` |
| src | `src/KurrentDB.Api.V2.Tests/Fixtures/ClusterVNodeTestContext.Helpers.cs` | 11 | `using Grpc.Core;` |

*... and 105 more*

**Repos:** src

### HttpClient.New (25 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Tests/Integration/when_node_becomes_leader_with_unindexed_data.cs` | 49 | `_httpClient = new HttpClient(new SocketsHttpHandler {` |
| src | `src/KurrentDB.Core.Tests/Integration/authenticated_requests_made_from_a_follower.cs` | 42 | `using var httpClient = new HttpClient(new SocketsHttpHandler` |
| src | `src/KurrentDB.Core.Tests/Integration/authenticated_requests_made_from_a_follower.cs` | 88 | `HttpClient = new HttpClient(new SocketsHttpHandler {` |
| src | `src/KurrentDB.Core.Tests/Http/HttpProtocols/clear_text_http_multiplexing_middleware.cs` | 63 | `using var client = new HttpClient();` |
| src | `src/KurrentDB.Core.Tests/Http/HttpProtocols/clear_text_http_multiplexing_middleware.cs` | 72 | `using var client = new HttpClient();` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/MonitoringTests/StatsTests.cs` | 35 | `HttpClient = new HttpClient(new SocketsHttpHandler {` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/ServerFeaturesTests/ServerFeaturesTest.cs` | 67 | `HttpClient = new HttpClient(new SocketsHttpHandler {` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Http/Authorization/authorization_tests.cs` | 28 | `var client = new HttpClient(new HttpClientHandler {` |
| src | `src/KurrentDB.Core.Testing/Helpers/MiniClusterNode.cs` | 277 | `var httpClient = new HttpClient(new SocketsHttpHandler {` |
| src | `src/KurrentDB.Core.Testing/Helpers/MiniNode.cs` | 277 | `HttpClient = new HttpClient(HttpMessageHandler) {` |
| src | `src/KurrentDB.Licensing.Tests/LicensingPluginTests.cs` | 153 | `_authenticatedClient = new HttpClient() {` |
| src | `src/KurrentDB.Licensing.Tests/LicensingPluginTests.cs` | 162 | `_unauthenticatedClient = new HttpClient() {` |
| src | `src/KurrentDB.Auth.UserCertificates.Tests/UserCertificatesPluginTests.cs` | 183 | `var client = new HttpClient(handler, disposeHandler: true) {` |
| src | `src/KurrentDB.Projections.Core.Tests/Services/http_service/authorization_tests.cs` | 28 | `var client = new HttpClient(new HttpClientHandler {` |
| src | `src/KurrentDB.Auth.OAuth/OAuthAuthenticationPlugin.cs` | 113 | `_httpClient = new HttpClient(new SocketsHttpHandler {` |
| src | `src/KurrentDB.Auth.OAuth/OAuthAuthenticationPlugin.cs` | 130 | `using var httpClient = new HttpClient(new SocketsHttpHandler` |
| src | `src/KurrentDB.Diagnostics.LogsEndpointPlugin.Tests/LogsEndpointPluginTests.cs` | 158 | `_authenticatedClient = new HttpClient() {` |
| src | `src/KurrentDB.Diagnostics.LogsEndpointPlugin.Tests/LogsEndpointPluginTests.cs` | 166 | `_unauthenticatedClient = new HttpClient() {` |
| src | `src/KurrentDB.TestClient/PortsHelper.cs` | 62 | `var client = new HttpClient();` |
| src | `src/KurrentDB.Auth.OAuth.Tests/Fixture.cs` | 90 | `using var client = new HttpClient(new SocketsHttpHandler {` |
| src | `src/KurrentDB.Auth.OAuth.Tests/IdpFixture.cs` | 56 | `HttpClient = new HttpClient(new SocketsHttpHandler {` |
| src | `src/KurrentDB.Auth.OAuth.Tests/OAuthAuthenticationHttpIntegrationTests.cs` | 74 | `return new HttpClient(socketsHttpHandler) {` |
| src | `src/KurrentDB.Core/Telemetry/TelemetrySink.cs` | 33 | `_httpClient = new HttpClient();` |
| src | `src/KurrentDB.Core/Services/HttpSendService.cs` | 52 | `_forwardClient = new HttpClient(socketsHttpHandler);` |
| src | `src/KurrentDB.Core/Services/Transport/Http/NodeHttpClientFactory/NodeHttpClientFactory.cs` | 44 | `return new HttpClient(httpMessageHandler);` |

**Repos:** src

## Storage

### FileStorage (75 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Tests/DataStructures/persistent_stream_bloom_filter.cs` | 130 | `using var fileStream = File.Open(_path, FileMode.Open);` |
| src | `src/KurrentDB.Core.Tests/Configuration/ClusterNodeOptionsTests/when_building/with_secure_tcp.cs` | 48 | `using var fileStream = File.Create(filePath);` |
| src | `src/KurrentDB.Core.Tests/Index/IndexV1/corrupt_index_should.cs` | 32 | `using var stream = File.Open(bloomFilterFile, FileMode.Open)` |
| src | `src/KurrentDB.Core.Tests/Index/IndexV1/corrupt_index_should.cs` | 64 | `using (FileStream stream = File.Open(ptableFile, FileMode.Op` |
| src | `src/KurrentDB.Core.Tests/Index/IndexV1/table_index_with_corrupt_index_entries_should.cs` | 115 | `using (FileStream stream = File.Open(ptableFile, FileMode.Op` |
| src | `src/KurrentDB.Core.Tests/Index/IndexV1/index_map_should_detect_corruption.cs` | 103 | `using (var fs = File.Open(_indexMapFileName, FileMode.Open))` |
| src | `src/KurrentDB.Core.Tests/Index/IndexV1/index_map_should_detect_corruption.cs` | 144 | `using (var fs = File.Open(_indexMapFileName, FileMode.Open))` |
| src | `src/KurrentDB.Core.Tests/Index/IndexV1/index_map_should_detect_corruption.cs` | 160 | `using (var fs = File.Open(_ptableFileName, FileMode.Open)) {` |
| src | `src/KurrentDB.Core.Tests/Index/IndexV1/index_map_should_detect_corruption.cs` | 177 | `using (var fs = File.Open(_ptableFileName, FileMode.Open)) {` |
| src | `src/KurrentDB.Core.Tests/Index/IndexV1/index_map_should_detect_corruption.cs` | 191 | `using (var fs = File.Open(_ptableFileName, FileMode.Open)) {` |
| src | `src/KurrentDB.Core.Tests/Index/IndexV1/index_map_should_detect_corruption.cs` | 208 | `using (var fs = File.Open(_ptableFileName, FileMode.Open)) {` |
| src | `src/KurrentDB.Core.Tests/Index/IndexV4/when_merging_ptables_vx_to_v4.cs` | 98 | `using (var filestream = File.Open(newTableFileCopy, FileMode` |
| src | `src/KurrentDB.Core.Tests/Index/IndexV4/when_merging_ptables_vx_to_v4.cs` | 217 | `using (var filestream = File.Open(newTableFileCopy, FileMode` |
| src | `src/KurrentDB.Core.Tests/mono_filestream_bug.cs` | 47 | `using (var filestream = File.Open(filename, FileMode.Open, F` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/Unbuffered/UnbufferedTests.cs` | 686 | `using (var fs = File.Open(filename, FileMode.Open, FileAcces` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/when_chasing_a_chunked_transaction_log.cs` | 287 | `File.Create(fileName).Close();` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/when_writing_an_existing_chunked_transaction_file_with_checksum_and_data_bigger_than_buffer.cs` | 71 | `await using var filestream = File.Open(filename,` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/when_writing_a_new_chunked_transaction_file.cs` | 55 | `await using var filestream = File.Open(GetFilePathFor("chunk` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/when_writing_an_existing_chunked_transaction_file_with_checksum.cs` | 66 | `await using var filestream = File.Open(filename, new FileStr` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/Validation/when_validating_tfchunk_db.cs` | 296 | `File.Create(GetFilePathFor("foo")).Close();` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/Validation/when_validating_tfchunk_db.cs` | 297 | `File.Create(GetFilePathFor("bla")).Close();` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/Validation/when_validating_tfchunk_db.cs` | 507 | `File.Create(GetFilePathFor("bla")).Close();` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/Validation/when_validating_tfchunk_db.cs` | 508 | `File.Create(GetFilePathFor("bla.scavenge.tmp")).Close();` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/Validation/when_validating_tfchunk_db.cs` | 509 | `File.Create(GetFilePathFor("bla.tmp")).Close();` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/Validation/when_validating_tfchunk_db.cs` | 544 | `using (Stream stream = File.Open(GetFilePathFor("chunk-00000` |

*... and 50 more*

**Repos:** src

## Database

### Dapper (66 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Testing/Bus/Helpers/WaitingConsumer.cs` | 34 | `((Action<DeferredExecutionTestMessage>)(deffered => deffered` |
| src | `src/KurrentDB.Core.Testing/Bus/Helpers/WaitingConsumer.cs` | 38 | `((Action<ExecutableTestMessage>)(deffered => deffered.Execut` |
| src | `src/KurrentDB.Api.V2/Modules/Streams/StreamsService.cs` | 56 | `return await command.Execute(context);` |
| src | `src/KurrentDB.Surge/Producers/SystemProducer.cs` | 112 | `await callback.Execute(result);` |
| src | `src/KurrentDB.Projections.Core/Services/Interpreted/JintProjectionStateHandler.cs` | 69 | `_engine.Execute(source);` |
| src | `src/KurrentDB.Projections.Core.Javascript.Tests/SpecRunner.cs` | 456 | `return def.Execute(_output).AsTask();` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaDbSchema.cs` | 37 | `connection.Execute(createTablesAndIndexesSql);` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaProjections.cs` | 50 | `connection.Execute(insertSchemaVersionSql,` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaProjections.cs` | 61 | `connection.Execute(insertSchemaSql,` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaProjections.cs` | 104 | `connection.Execute(` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaProjections.cs` | 117 | `connection.Execute(` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaProjections.cs` | 141 | `connection.Execute(` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaProjections.cs` | 162 | `connection.Execute(` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaProjections.cs` | 183 | `connection.Execute(` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaProjections.cs` | 216 | `connection.Execute(deleteSelectedSchemaVersionsSql, new {` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaProjections.cs` | 221 | `connection.Execute(updateSchemaLatestVersionSql, new {` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaProjections.cs` | 249 | `connection.Execute(deleteSchemaVersionsSql, new { schema_nam` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaProjections.cs` | 250 | `connection.Execute(deleteSchemasSql, new { schema_name = msg` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Planes/Storage/DuckDBQueryExtensions.cs` | 20 | `foreach (var record in connection.Query(sql, param))` |
| src | `src/KurrentDB.SecondaryIndexing.LoadTesting/Assertions/DuckDb/DuckDbIndexingSummaryAssertion.cs` | 18 | `var categories = connection.Query<string>("select distinct c` |
| src | `src/KurrentDB.SecondaryIndexing.LoadTesting/Assertions/DuckDb/DuckDbIndexingSummaryAssertion.cs` | 27 | `var eventTypes = connection.Query<string>("select distinct e` |
| src | `src/KurrentDB.TestClient/CommandsProcessor.cs` | 47 | `_regCommandsProcessor.Execute(context, new string[0]);` |
| src | `src/KurrentDB.TestClient/CommandsProcessor.cs` | 57 | `var syntaxOk = commandProcessor.Execute(context, commandArgs` |
| src | `src/KurrentDB.Core.XUnit.Tests/Scavenge/Infrastructure/TracingIndexExecutor.cs` | 29 | `await _wrapped.Execute(scavengePoint, state, scavengerLogger` |
| src | `src/KurrentDB.Core.XUnit.Tests/Scavenge/Infrastructure/TracingIndexExecutor.cs` | 45 | `await _wrapped.Execute(checkpoint, state, scavengerLogger, c` |

*... and 41 more*

**Repos:** src

## Config

### ConnectionString (61 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_with_connection_string.cs` | 34 | `string connectionString = string.Format("ConnectTo=tcp://{0}` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_with_connection_string.cs` | 35 | `using (var connection = EventStoreConnection.Create(connecti` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_with_connection_string.cs` | 43 | `string connectionString = string.Format("GossipSeeds={0};", ` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_with_connection_string.cs` | 46 | `Assert.DoesNotThrow(() => connection = EventStoreConnection.` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_with_connection_string.cs` | 54 | `string connectionString = string.Format("ConnectTo=tcp://{0}` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_with_connection_string.cs` | 56 | `Assert.Throws<NotSupportedException>(() => EventStoreConnect` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_with_connection_string.cs` | 61 | `string connectionString = string.Format("HeartBeatTimeout=20` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_with_connection_string.cs` | 62 | `Assert.Throws<Exception>(() => EventStoreConnection.Create(c` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connection_string.cs` | 13 | `var settings = ConnectionString.GetConnectionSettings("verbo` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connection_string.cs` | 19 | `var settings = ConnectionString.GetConnectionSettings("Verbo` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connection_string.cs` | 26 | `var settings = ConnectionString.GetConnectionSettings("maxre` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connection_string.cs` | 32 | `var settings = ConnectionString.GetConnectionSettings("heart` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connection_string.cs` | 38 | `var settings = ConnectionString.GetConnectionSettings("heart` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connection_string.cs` | 45 | `var settings = ConnectionString.GetConnectionSettings("heArt` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connection_string.cs` | 52 | `ConnectionString.GetConnectionSettings(` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connection_string.cs` | 59 | `var settings = ConnectionString.GetConnectionSettings("Defau` |
| src | `src/KurrentDB.SecondaryIndexing.LoadTesting/Program.cs` | 18 | `?? new LoadTestConfig { DuckDbConnectionString = "DUMMY", Ku` |
| src | `src/KurrentDB.SecondaryIndexing.LoadTesting/Environments/gRPC/gRPCClientEnvironment.cs` | 15 | `public gRPCClientEnvironment(string dbConnectionString) {` |
| src | `src/KurrentDB.SecondaryIndexing.LoadTesting/Environments/gRPC/gRPCClientEnvironment.cs` | 16 | `_client = new(KurrentDBClientSettings.Create(dbConnectionStr` |
| src | `src/KurrentDB.SecondaryIndexing.LoadTesting/Environments/LoadTestEnvironment.cs` | 33 | `LoadTestEnvironmentType.gRPC => new gRPCClientEnvironment(co` |
| src | `src/KurrentDB.SecondaryIndexing.LoadTesting/LoadTestConfig.cs` | 20 | `public required string KurrentDBConnectionString { get; set;` |
| src | `src/KurrentDB.SecondaryIndexing.LoadTesting/LoadTestConfig.cs` | 21 | `public required string DuckDbConnectionString { get; set; } ` |
| src | `src/KurrentDB.TestClient/Program.cs` | 43 | `/// <param name="connectionString">The connection string to ` |
| src | `src/KurrentDB.TestClient/Program.cs` | 49 | `bool reconnect = true, bool useTls = false, bool tlsValidate` |
| src | `src/KurrentDB.TestClient/Program.cs` | 78 | `ConnectionString = connectionString,` |

*... and 36 more*

**Repos:** src

## Messaging

### Kafka (10 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Surge.Testing/Fixtures/SystemComponentsAssemblyFixture.cs` | 58 | `public IProducer Producer { get; private set; } = null!;` |
| src | `src/KurrentDB.Surge/Producers/SystemProducerProvider.cs` | 9 | `public class SystemProducerProvider(Func<SystemProducerBuild` |
| src | `src/KurrentDB.Surge/Producers/SystemProducerProvider.cs` | 10 | `public IProducer GetProducer(Func<ProducerOptions, ProducerO` |
| src | `src/KurrentDB.Surge/Producers/SystemProducer.cs` | 18 | `public class SystemProducer : IProducer {` |
| src | `src/KurrentDB.Surge/SurgeExtensions.cs` | 48 | `services.AddSingleton<IProducerBuilder, SystemProducerBuilde` |
| src | `src/KurrentDB.Surge/Eventuous/SystemEventStore.cs` | 18 | `public class SystemEventStore(IReader reader, IProducer prod` |
| src | `src/KurrentDB.Surge/Eventuous/SystemEventStore.cs` | 20 | `IProducer Producer { get; } = producer;` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/SchemaRegistryWireUp.cs` | 57 | `var producer = ctx.GetRequiredService<IProducerBuilder>()` |
| src | `src/Connectors/KurrentDB.Connectors/Infrastructure/Connect/SurgeExtensions.cs` | 104 | `services.AddSingleton<IProducerProvider, SystemProducerProvi` |
| src | `src/Connectors/KurrentDB.Connectors/Infrastructure/Connect/SurgeExtensions.cs` | 198 | `builder.Services.AddSingleton<IProducer>(ctx => {` |

**Repos:** src

### RabbitMQ (3 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/Connectors/KurrentDB.Connectors.Tests/Planes/Management/ConnectorsLicenseServiceTests.cs` | 9 | `using Kurrent.Connectors.RabbitMQ;` |
| src | `src/Connectors/KurrentDB.Connectors/Infrastructure/Connect/Components/Connectors/ConnectorCatalogue.cs` | 10 | `using Kurrent.Connectors.RabbitMQ;` |
| src | `src/Connectors/KurrentDB.Connectors/Infrastructure/Connect/Components/Connectors/ConnectorDataProtectors.cs` | 8 | `using Kurrent.Connectors.RabbitMQ;` |

**Repos:** src

## Connector

### IMessageAdapter (4 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Transport.Http/EntityManagement/CoreHttpRequestAdapter.cs` | 13 | `public class CoreHttpRequestAdapter : IHttpRequest {` |
| src | `src/KurrentDB.Transport.Http/EntityManagement/HttpListenerRequestAdapter.cs` | 12 | `public class HttpListenerRequestAdapter : IHttpRequest {` |
| src | `src/KurrentDB.Transport.Http/EntityManagement/CoreHttpResponseAdapter.cs` | 10 | `public class CoreHttpResponseAdapter : IHttpResponse {` |
| src | `src/KurrentDB.Transport.Http/EntityManagement/HttpListenerResponseAdapter.cs` | 10 | `public class HttpListenerResponseAdapter : IHttpResponse {` |

**Repos:** src


---

*[Back to Index](../index.md)*
