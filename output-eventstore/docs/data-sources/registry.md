# Data Source Registry

## Summary

| Type | Occurrences |
|------|-------------|
| api | 517 |
| messaging | 413 |
| cache | 284 |
| database | 190 |
| storage | 147 |
| config | 61 |
| connector | 4 |
| ui | 2 |

## Api

### gRPC (273 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Tests/Integration/when_node_becomes_leader_with_unindexed_data.cs` | 14 | `using Google.Protobuf;` |
| src | `src/KurrentDB.Core.Tests/Integration/when_node_becomes_leader_with_unindexed_data.cs` | 15 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Integration/when_node_becomes_leader_with_unindexed_data.cs` | 16 | `using Grpc.Net.Client;` |
| src | `src/KurrentDB.Core.Tests/Integration/authenticated_requests_made_from_a_follower.cs` | 15 | `using Google.Protobuf;` |
| src | `src/KurrentDB.Core.Tests/Integration/authenticated_requests_made_from_a_follower.cs` | 16 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Integration/authenticated_requests_made_from_a_follower.cs` | 17 | `using Grpc.Net.Client;` |
| src | `src/KurrentDB.Core.Tests/Integration/authenticated_requests_made_from_a_follower.cs` | 21 | `using StatusCode = Grpc.Core.StatusCode;` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/when_writing_prepare_record_with_properties_to_file.cs` | 7 | `using Google.Protobuf;` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/when_writing_prepare_record_with_properties_to_file.cs` | 8 | `using Google.Protobuf.WellKnownTypes;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/ReadIndexForwardsTests.cs` | 8 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/DeleteTests.cs` | 9 | `using Google.Protobuf;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/DeleteTests.cs` | 10 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/ReadAllBackwardsTests.cs` | 8 | `using Google.Protobuf;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/ReadAllBackwardsTests.cs` | 9 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/GrpcSpecification.cs` | 13 | `using Google.Protobuf;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/GrpcSpecification.cs` | 14 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/GrpcSpecification.cs` | 15 | `using Grpc.Net.Client;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/SubscribeToAllTests.cs` | 8 | `using Google.Protobuf;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/SubscribeToAllTests.cs` | 9 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/AppendBatchToStreamTests.cs` | 8 | `using Google.Protobuf;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/AppendBatchToStreamTests.cs` | 9 | `using Google.Protobuf.WellKnownTypes;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/ReadAllForwardsTests.cs` | 8 | `using Google.Protobuf;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/ReadAllForwardsTests.cs` | 9 | `using Grpc.Core;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/ReadStreamsForwardTests.cs` | 10 | `using Google.Protobuf;` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/ReadStreamsForwardTests.cs` | 11 | `using Grpc.Core;` |

*... and 248 more*

**Repos:** src

### gRPC.Server (168 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Plugins.Api.V2/ApiV2Plugin.cs` | 62 | `endpoints.MapGrpcService<IndexesService>()` |
| src | `src/KurrentDB.Plugins.Api.V2/ApiV2Plugin.cs` | 64 | `endpoints.MapGrpcService<StreamsService>()` |
| src | `src/KurrentDB.Api.V2/Infrastructure/ServerCallContextExtensions.cs` | 14 | `static class ServerCallContextExtensions {` |
| src | `src/KurrentDB.Api.V2/Infrastructure/ServerCallContextExtensions.cs` | 15 | `public static ILogger<T> GetLogger<T>(this ServerCallContext` |
| src | `src/KurrentDB.Api.V2/Infrastructure/ServerCallContextExtensions.cs` | 18 | `public static ILoggerFactory GetLoggerFactory(this ServerCal` |
| src | `src/KurrentDB.Api.V2/Infrastructure/ServerCallContextExtensions.cs` | 21 | `public static TimeProvider GetTimeProvider(this ServerCallCo` |
| src | `src/KurrentDB.Api.V2/Infrastructure/ServerCallContextExtensions.cs` | 24 | `public static GrpcServiceOptions GetGrpcServiceOptions(this ` |
| src | `src/KurrentDB.Api.V2/Infrastructure/ServerCallContextExtensions.cs` | 28 | `public static ClaimsPrincipal GetUser(this ServerCallContext` |
| src | `src/KurrentDB.Api.V2/Infrastructure/ServerCallContextExtensions.cs` | 31 | `public static string GetFriendlyOperationName(this ServerCal` |
| src | `src/KurrentDB.Api.V2/Infrastructure/ApiCommand.cs` | 60 | `protected abstract Message BuildMessage(IEnvelope callback, ` |
| src | `src/KurrentDB.Api.V2/Infrastructure/ApiCommand.cs` | 91 | `public async ValueTask<TResult> Execute(ServerCallContext co` |
| src | `src/KurrentDB.Api.V2/Infrastructure/Authorization/AuthorizationExtensions.cs` | 20 | `public static Task AuthorizeOperation(this IAuthorizationPro` |
| src | `src/KurrentDB.Api.V2/Infrastructure/Authorization/AuthorizationExtensions.cs` | 26 | `public static Task AuthorizeOperation(this IAuthorizationPro` |
| src | `src/KurrentDB.Api.V2/Infrastructure/Grpc/Validation/RequestValidationInterceptor.cs` | 10 | `protected override TRequest InterceptRequest<TRequest>(TRequ` |
| src | `src/KurrentDB.Api.V2/Infrastructure/Grpc/Interceptors/InterceptingStreamReader.cs` | 11 | `public delegate ValueTask<T> InterceptRequestAsync<T>(T requ` |
| src | `src/KurrentDB.Api.V2/Infrastructure/Grpc/Interceptors/InterceptingStreamReader.cs` | 12 | `public delegate T            InterceptRequest<T>(T request, ` |
| src | `src/KurrentDB.Api.V2/Infrastructure/Grpc/Interceptors/InterceptingStreamReader.cs` | 13 | `public delegate ValueTask<T> InterceptRequestAsync<T, in TSt` |
| src | `src/KurrentDB.Api.V2/Infrastructure/Grpc/Interceptors/InterceptingStreamReader.cs` | 14 | `public delegate T            InterceptRequest<T, in TState>(` |
| src | `src/KurrentDB.Api.V2/Infrastructure/Grpc/Interceptors/InterceptingStreamReader.cs` | 16 | `public sealed class InterceptingStreamReader<T>(IAsyncStream` |
| src | `src/KurrentDB.Api.V2/Infrastructure/Grpc/Interceptors/InterceptingStreamReader.cs` | 35 | `public sealed class InterceptingStreamReader<T, TState>(IAsy` |
| src | `src/KurrentDB.Api.V2/Infrastructure/Grpc/Interceptors/InterceptingStreamReader.cs` | 55 | `public static IAsyncStreamReader<T> Intercept<T>(this IAsync` |
| src | `src/KurrentDB.Api.V2/Infrastructure/Grpc/Interceptors/InterceptingStreamReader.cs` | 58 | `public static IAsyncStreamReader<T> Intercept<T>(this IAsync` |
| src | `src/KurrentDB.Api.V2/Infrastructure/Grpc/Interceptors/InterceptingStreamReader.cs` | 61 | `public static IAsyncStreamReader<T> Intercept<T, TState>(thi` |
| src | `src/KurrentDB.Api.V2/Infrastructure/Grpc/Interceptors/InterceptingStreamReader.cs` | 64 | `public static IAsyncStreamReader<T> Intercept<T, TState>(thi` |
| src | `src/KurrentDB.Api.V2/Infrastructure/Grpc/Interceptors/InterceptingStreamReader.cs` | 69 | `public ValueTask<T> InvokeAsync(T request, ServerCallContext` |

*... and 143 more*

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

### HttpClient.GetAsync (19 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Tests/Services/Transport/Http/http_service_should.cs` | 63 | `var result = await node.HttpClient.GetAsync("/ping^\"");` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Http/ping_controller_should.cs` | 33 | `var result = await _node.HttpClient.GetAsync("/ping?format=j` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Http/ping_controller_should.cs` | 43 | `var result = await _node.HttpClient.GetAsync("/ping?format=j` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Http/ping_controller_should.cs` | 50 | `var result = await _node.HttpClient.GetAsync("/ping?format=x` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Http/ping_controller_should.cs` | 57 | `var result = await _node.HttpClient.GetAsync("/ping?format=t` |
| src | `src/KurrentDB.Licensing.Tests/LicensingPluginTests.cs` | 71 | `var result = await _server.AuthenticatedClient.GetAsync("/li` |
| src | `src/KurrentDB.Licensing.Tests/LicensingPluginTests.cs` | 101 | `var result = await _server.AuthenticatedClient.GetAsync("/li` |
| src | `src/KurrentDB.Licensing.Tests/LicensingPluginTests.cs` | 118 | `var result = await _server.UnauthenticatedClient.GetAsync("/` |
| src | `src/KurrentDB.Auth.UserCertificates.Tests/UserCertificatesPluginTests.cs` | 49 | `var result = await client.GetAsync("/test");` |
| src | `src/KurrentDB.Auth.UserCertificates.Tests/UserCertificatesPluginTests.cs` | 62 | `var result = await client.GetAsync("/test");` |
| src | `src/KurrentDB.Auth.UserCertificates.Tests/UserCertificatesPluginTests.cs` | 77 | `var result = await client.GetAsync("/test");` |
| src | `src/KurrentDB.Auth.UserCertificates.Tests/UserCertificatesPluginTests.cs` | 96 | `var result = await client.GetAsync("/test");` |
| src | `src/KurrentDB.Auth.UserCertificates.Tests/UserCertificatesPluginTests.cs` | 115 | `var result = await client.GetAsync("/test");` |
| src | `src/KurrentDB.AutoScavenge.Tests/PluginTests.cs` | 34 | `var resp = await _client.GetAsync("/auto-scavenge/enabled");` |
| src | `src/KurrentDB.AutoScavenge.Tests/PluginTests.cs` | 40 | `var resp = await _client.GetAsync("/auto-scavenge/status");` |
| src | `src/KurrentDB.Core.XUnit.Tests/Metrics/MetricsEndpointTests.cs` | 91 | `var result = await sut.HttpClient.GetAsync("/metrics");` |
| src | `src/KurrentDB.Auth.OAuth.Tests/Fixture.cs` | 95 | `using var response = await client.GetAsync("https://localhos` |
| src | `src/KurrentDB.Auth.OAuth.Tests/OAuthAuthenticationHttpIntegrationTests.cs` | 45 | `using var readResponse = await client.GetAsync("/streams/$al` |
| src | `src/KurrentDB.Auth.OAuth.Tests/OAuthAuthenticationHttpIntegrationTests.cs` | 62 | `using var readResponse = await client.GetAsync("/streams/$al` |

**Repos:** src

### gRPC.Client (11 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Tests/Integration/when_node_becomes_leader_with_unindexed_data.cs` | 67 | `using var channel = GrpcChannel.ForAddress(new Uri($"https:/` |
| src | `src/KurrentDB.Core.Tests/Integration/when_node_becomes_leader_with_unindexed_data.cs` | 120 | `using var channel = GrpcChannel.ForAddress(new Uri($"https:/` |
| src | `src/KurrentDB.Core.Tests/Integration/authenticated_requests_made_from_a_follower.cs` | 86 | `using var channel = GrpcChannel.ForAddress(new Uri($"https:/` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/StreamsTests/GrpcSpecification.cs` | 54 | `Channel = GrpcChannel.ForAddress(` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/MonitoringTests/StatsTests.cs` | 33 | `using var channel = GrpcChannel.ForAddress(new Uri($"https:/` |
| src | `src/KurrentDB.Core.Tests/Services/Transport/Grpc/ServerFeaturesTests/ServerFeaturesTest.cs` | 65 | `using var channel = GrpcChannel.ForAddress(new Uri($"https:/` |
| src | `src/KurrentDB.Projections.Core.Tests/Services/grpc_service/ServerFeaturesTests.cs` | 34 | `using var channel = GrpcChannel.ForAddress(` |
| src | `src/KurrentDB.Projections.Core.Tests/Services/grpc_service/ProjectionsStatisticsTests.cs` | 26 | `_channel = GrpcChannel.ForAddress(` |
| src | `src/KurrentDB.Testing.ClusterVNodeApp/GrpcChannelShim.cs` | 19 | `GrpcChannel = GrpcChannel.ForAddress(NodeShim.Node.Uri);` |
| src | `src/KurrentDB.Testing.ClusterVNodeApp/GrpcChannelShim.cs` | 38 | `GrpcChannel = GrpcChannel.ForAddress(NodeShim.Node.Uri, chan` |
| src | `src/KurrentDB.Core/Cluster/EventStoreClusterClient.cs` | 47 | `_channel = GrpcChannel.ForAddress(address, new GrpcChannelOp` |

**Repos:** src

### API.MapGet (5 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Tests/Http/HttpProtocols/clear_text_http_multiplexing_middleware.cs` | 27 | `router.MapGet("/test", async context => {` |
| src | `src/KurrentDB.Auth.UserCertificates.Tests/UserCertificatesPluginTests.cs` | 152 | `app.MapGet("/test", () => "Hello World!").RequireAuthorizati` |
| src | `src/KurrentDB.Licensing/LicensingPlugin.cs` | 48 | `.MapGet("/license", (HttpContext _) => {` |
| src | `src/KurrentDB.AutoScavenge/AutoScavengePlugin.cs` | 121 | `anyUserGroup.MapGet("/enabled", OnGetEnabled);` |
| src | `src/KurrentDB.AutoScavenge/AutoScavengePlugin.cs` | 122 | `anyUserGroup.MapGet("/status", (Delegate)OnGetStatus);` |

**Repos:** src

### HttpClient.PostAsync (4 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Auth.OAuth.Tests/OAuthAuthenticationHttpIntegrationTests.cs` | 39 | `using var writeResponse = await client.PostAsync("/streams/a` |
| src | `src/KurrentDB.Auth.OAuth.Tests/OAuthAuthenticationHttpIntegrationTests.cs` | 42 | `using var writeSystemResponse = await client.PostAsync("/str` |
| src | `src/KurrentDB.Auth.OAuth.Tests/OAuthAuthenticationHttpIntegrationTests.cs` | 56 | `using var writeResponse = await client.PostAsync("/streams/a` |
| src | `src/KurrentDB.Auth.OAuth.Tests/OAuthAuthenticationHttpIntegrationTests.cs` | 59 | `using var writeSystemResponse = await client.PostAsync("/str` |

**Repos:** src

### API.Route (3 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Tests/Services/VNode/http_pipeline_should.cs` | 112 | `[Route("/my-controller")]` |
| src | `src/KurrentDB.Core.Tests/Services/VNode/http_pipeline_should.cs` | 116 | `[Route("protected")]` |
| src | `src/KurrentDB.Core.Tests/Services/VNode/http_pipeline_should.cs` | 120 | `[Route("unprotected")]` |

**Repos:** src

### API.MapPost (3 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.AutoScavenge/AutoScavengePlugin.cs` | 126 | `opsGroup.MapPost("/resume", (Delegate)OnPostResume);` |
| src | `src/KurrentDB.AutoScavenge/AutoScavengePlugin.cs` | 127 | `opsGroup.MapPost("/pause", (Delegate)OnPostPause);` |
| src | `src/KurrentDB.AutoScavenge/AutoScavengePlugin.cs` | 128 | `opsGroup.MapPost("/configure", (Delegate)OnPostConfigure);` |

**Repos:** src

### API.MapGroup (3 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.AutoScavenge/AutoScavengePlugin.cs` | 120 | `var anyUserGroup = endpoints.MapGroup("/auto-scavenge");` |
| src | `src/KurrentDB.AutoScavenge/AutoScavengePlugin.cs` | 125 | `var opsGroup = endpoints.MapGroup("/auto-scavenge");` |
| src | `src/KurrentDB.Core/ClusterVNodeStartup.cs` | 119 | `_statusCheck.MapLiveness(app.MapGroup("/health"));` |

**Repos:** src

### API.HttpGet (2 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Tests/Services/VNode/http_pipeline_should.cs` | 114 | `[HttpGet]` |
| src | `src/KurrentDB.Core.Tests/Services/VNode/http_pipeline_should.cs` | 119 | `[HttpGet]` |

**Repos:** src

### API.Controller (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Tests/Services/VNode/http_pipeline_should.cs` | 113 | `public class FakeController : ControllerBase {` |

**Repos:** src

## Messaging

### Kafka.Consumer (350 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Tests/ClientOperations/specification_with_bare_vnode.cs` | 53 | `_node.MainBus.Subscribe(handler);` |
| src | `src/KurrentDB.Core.Tests/ClientOperations/specification_with_bare_vnode.cs` | 74 | `_source.Subscribe(this);` |
| src | `src/KurrentDB.Core.Tests/AwakeService/when_subscribing_before_last_position_with_already_committed_events.cs` | 54 | `_publisher.Subscribe(_handler);` |
| src | `src/KurrentDB.Core.Tests/AwakeService/when_handling_committed_event_after_unsybscribe.cs` | 61 | `_publisher.Subscribe(_handler);` |
| src | `src/KurrentDB.Core.Tests/AwakeService/when_handling_committed_event_with_subscribers.cs` | 56 | `_publisher.Subscribe(_handler);` |
| src | `src/KurrentDB.Core.Tests/Integration/when_a_leader_is_shutdown.cs` | 27 | `x.Node.MainBus.Subscribe(new AdHocHandler<SystemMessage.Beco` |
| src | `src/KurrentDB.Core.Tests/Integration/when_a_leader_is_shutdown.cs` | 28 | `x.Node.MainBus.Subscribe(new AdHocHandler<SystemMessage.Beco` |
| src | `src/KurrentDB.Core.Tests/Integration/when_a_leader_is_shutdown.cs` | 29 | `x.Node.MainBus.Subscribe(new AdHocHandler<SystemMessage.Epoc` |
| src | `src/KurrentDB.Core.Tests/Integration/when_a_single_node_is_restarted_multiple_times.cs` | 26 | `_node.Node.MainBus.Subscribe(new AdHocHandler<SystemMessage.` |
| src | `src/KurrentDB.Core.Tests/Bus/FSMSpeedTest.cs` | 38 | `bus.Subscribe(new AdHocHandler<StorageMessage.WriteCommit>(x` |
| src | `src/KurrentDB.Core.Tests/Bus/FSMSpeedTest.cs` | 39 | `bus.Subscribe(new AdHocHandler<Message>(x => { }));` |
| src | `src/KurrentDB.Core.Tests/Bus/when_subscribing_to_memory_bus.cs` | 45 | `_bus.Subscribe(handler);` |
| src | `src/KurrentDB.Core.Tests/Bus/when_subscribing_to_memory_bus.cs` | 88 | `_bus.Subscribe(handler1);` |
| src | `src/KurrentDB.Core.Tests/Bus/when_subscribing_to_memory_bus.cs` | 89 | `_bus.Subscribe(handler2);` |
| src | `src/KurrentDB.Core.Tests/Bus/when_subscribing_to_memory_bus.cs` | 160 | `_bus.Subscribe(handler);` |
| src | `src/KurrentDB.Core.Tests/Bus/when_subscribing_to_memory_bus.cs` | 161 | `_bus.Subscribe(handler);` |
| src | `src/KurrentDB.Core.Tests/Bus/when_subscribing_to_memory_bus.cs` | 162 | `_bus.Subscribe(handler);` |
| src | `src/KurrentDB.Core.Tests/Bus/when_publishing_into_memory_bus.cs` | 52 | `_bus.Subscribe(handler1);` |
| src | `src/KurrentDB.Core.Tests/Bus/when_publishing_into_memory_bus.cs` | 53 | `_bus.Subscribe(handler2);` |
| src | `src/KurrentDB.Core.Tests/Bus/when_publishing_into_memory_bus.cs` | 65 | `_bus.Subscribe(handler);` |
| src | `src/KurrentDB.Core.Tests/Bus/when_publishing_into_memory_bus.cs` | 81 | `_bus.Subscribe(handler);` |
| src | `src/KurrentDB.Core.Tests/Bus/when_publishing_into_memory_bus.cs` | 95 | `_bus.Subscribe(parentHandler);` |
| src | `src/KurrentDB.Core.Tests/Bus/when_publishing_into_memory_bus.cs` | 105 | `_bus.Subscribe(childHandler);` |
| src | `src/KurrentDB.Core.Tests/Bus/when_publishing_into_memory_bus.cs` | 117 | `_bus.Subscribe(parentHandler);` |
| src | `src/KurrentDB.Core.Tests/Bus/when_publishing_into_memory_bus.cs` | 118 | `_bus.Subscribe(childHandler);` |

*... and 325 more*

**Repos:** src

### Kafka.Producer (32 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Surge.Testing/Fixtures/SystemComponentsAssemblyFixture.cs` | 58 | `public IProducer Producer { get; private set; } = null!;` |
| src | `src/KurrentDB.Surge.Testing/Fixtures/SystemComponentsAssemblyFixture.cs` | 63 | `public SystemProducerBuilder NewProducer() => SystemProducer` |
| src | `src/KurrentDB.Surge.Testing/Fixtures/SystemComponentsAssemblyFixture.Helper.cs` | 62 | `results.Add(await Producer.Produce(request));` |
| src | `src/KurrentDB.Surge/Producers/SystemProducerProvider.cs` | 9 | `public class SystemProducerProvider(Func<SystemProducerBuild` |
| src | `src/KurrentDB.Surge/Producers/SystemProducerProvider.cs` | 10 | `public IProducer GetProducer(Func<ProducerOptions, ProducerO` |
| src | `src/KurrentDB.Surge/Producers/SystemProducer.cs` | 18 | `public class SystemProducer : IProducer {` |
| src | `src/KurrentDB.Surge/Producers/SystemProducer.cs` | 19 | `public static SystemProducerBuilder Builder => new();` |
| src | `src/KurrentDB.Surge/Producers/SystemProducerBuilder.cs` | 11 | `public record SystemProducerBuilder : ProducerBuilder<System` |
| src | `src/KurrentDB.Surge/Producers/SystemProducerBuilder.cs` | 12 | `public SystemProducerBuilder Client(ISystemClient client) {` |
| src | `src/KurrentDB.Surge/SurgeExtensions.cs` | 48 | `services.AddSingleton<IProducerBuilder, SystemProducerBuilde` |
| src | `src/KurrentDB.Surge/Eventuous/SystemEventStore.cs` | 18 | `public class SystemEventStore(IReader reader, IProducer prod` |
| src | `src/KurrentDB.Surge/Eventuous/SystemEventStore.cs` | 20 | `IProducer Producer { get; } = producer;` |
| src | `src/KurrentDB.Surge/Eventuous/SystemEventStore.cs` | 86 | `var result = await Producer.Produce(request);` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/SchemaRegistryWireUp.cs` | 57 | `var producer = ctx.GetRequiredService<IProducerBuilder>()` |
| src | `src/KurrentDB.Surge.Tests/Components/Producers/SystemProducerTests.cs` | 35 | `results.Add(await producer.Produce(request));` |
| src | `src/KurrentDB.Core/TransactionLog/Chunks/TFChunk/WriterWorkItem.cs` | 94 | `_cachedWriter.Produce(length);` |
| src | `src/Connectors/KurrentDB.Connectors.Tests/Planes/Control/ConnectorsControlRegistryTests.cs` | 69 | `var result  = await Fixture.Producer.Produce(request);` |
| src | `src/Connectors/KurrentDB.Connectors.Tests/Planes/Control/ConnectorsControlRegistryTests.cs` | 79 | `var result  = await Fixture.Producer.Produce(request);` |
| src | `src/Connectors/KurrentDB.Connectors/Infrastructure/SnapshotProjections/SnapshotProjectionsStore.cs` | 22 | `Func<SystemProducerBuilder> getProducerBuilder` |
| src | `src/Connectors/KurrentDB.Connectors/Infrastructure/SnapshotProjections/SnapshotProjectionsStore.cs` | 25 | `SystemProducer Producer { get; } = getProducerBuilder().Prod` |
| src | `src/Connectors/KurrentDB.Connectors/Infrastructure/SnapshotProjections/SnapshotProjectionsStore.cs` | 51 | `await Producer.Produce(produceRequest, throwOnError: true);` |
| src | `src/Connectors/KurrentDB.Connectors/Infrastructure/Connect/SurgeExtensions.cs` | 69 | `services.AddSingleton<Func<SystemProducerBuilder>>(ctx => {` |
| src | `src/Connectors/KurrentDB.Connectors/Infrastructure/Connect/SurgeExtensions.cs` | 106 | `services.AddSingleton<Func<GrpcProducerBuilder>>(ctx => {` |
| src | `src/Connectors/KurrentDB.Connectors/Infrastructure/Connect/SurgeExtensions.cs` | 198 | `builder.Services.AddSingleton<IProducer>(ctx => {` |
| src | `src/Connectors/KurrentDB.Connectors/Infrastructure/Connect/SurgeExtensions.cs` | 199 | `var factory = ctx.GetRequiredService<Func<SystemProducerBuil` |

*... and 7 more*

**Repos:** src

### Kafka.Topic (31 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_all_security.cs` | 16 | `await AssertEx.ThrowsAsync<NotAuthenticatedException>(() => ` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_all_security.cs` | 26 | `await AssertEx.ThrowsAsync<AccessDeniedException>(() => Subs` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_all_security.cs` | 31 | `await SubscribeToAll("user1", "pa$$1");` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_all_security.cs` | 36 | `await SubscribeToAll("adm", "admpa$$");` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/authorized_default_credentials_security.cs` | 40 | `await SubscribeToStream("read-stream", null, null);` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/authorized_default_credentials_security.cs` | 66 | `await AssertEx.ThrowsAsync<NotAuthenticatedException>(() => ` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/authorized_default_credentials_security.cs` | 67 | `await AssertEx.ThrowsAsync<NotAuthenticatedException>(() => ` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/authorized_default_credentials_security.cs` | 92 | `await AssertEx.ThrowsAsync<AccessDeniedException>(() => Subs` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/authorized_default_credentials_security.cs` | 93 | `await AssertEx.ThrowsAsync<AccessDeniedException>(() => Subs` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_stream_security.cs` | 16 | `await AssertEx.ThrowsAsync<NotAuthenticatedException>(() => ` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_stream_security.cs` | 21 | `await AssertEx.ThrowsAsync<AccessDeniedException>(() => Subs` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_stream_security.cs` | 26 | `await AssertEx.ThrowsAsync<AccessDeniedException>(() => Subs` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_stream_security.cs` | 31 | `await SubscribeToStream("read-stream", "user1", "pa$$1");` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_stream_security.cs` | 36 | `await SubscribeToStream("read-stream", "adm", "admpa$$");` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_stream_security.cs` | 42 | `await SubscribeToStream("noacl-stream", null, null);` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_stream_security.cs` | 47 | `await AssertEx.ThrowsAsync<NotAuthenticatedException>(() => ` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_stream_security.cs` | 52 | `await SubscribeToStream("noacl-stream", "user1", "pa$$1");` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_stream_security.cs` | 53 | `await SubscribeToStream("noacl-stream", "user2", "pa$$2");` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_stream_security.cs` | 58 | `await SubscribeToStream("noacl-stream", "adm", "admpa$$");` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_stream_security.cs` | 64 | `await SubscribeToStream("normal-all", null, null);` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_stream_security.cs` | 70 | `await AssertEx.ThrowsAsync<NotAuthenticatedException>(() => ` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_stream_security.cs` | 75 | `await SubscribeToStream("normal-all", "user1", "pa$$1");` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_stream_security.cs` | 76 | `await SubscribeToStream("normal-all", "user2", "pa$$2");` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/Security/subscribe_to_stream_security.cs` | 81 | `await SubscribeToStream("normal-all", "adm", "admpa$$");` |
| src | `src/KurrentDB.Surge.Testing/Fixtures/SystemComponentsAssemblyFixture.cs` | 35 | `.ProducerId("test-pdx")` |

*... and 6 more*

**Repos:** src

## Cache

### Redis.Write (163 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Tests/Integration/when_a_single_node_is_restarted_multiple_times.cs` | 43 | `_waitForStart.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/update_persistent_subscription.cs` | 60 | `_dropped.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/deleting_persistent_subscription.cs` | 51 | `(s, r, e) => _called.Set(), DefaultData.AdminCredentials);` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/persistent_connect_integration_tests.cs` | 43 | `_eventsReceived.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/persistent_connect_integration_tests.cs` | 91 | `_eventsReceived.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/persistent_connect_integration_tests.cs` | 145 | `_eventsReceived.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/persistent_connect_integration_tests.cs` | 196 | `_eventsReceived.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/persistent_connect_integration_tests.cs` | 245 | `_eventsReceived.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/persistent_connect_integration_tests.cs` | 298 | `_eventsReceived.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/persistent_connect_integration_tests.cs` | 348 | `_eventsReceived.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/subscribe_to_all_catching_up_should.cs` | 99 | `appeared.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/catchup_subscription_handles_small_batch_sizes.cs` | 73 | `}, (sub) => { mre.Set(); }, null, new UserCredentials("admin` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/catchup_subscription_handles_small_batch_sizes.cs` | 88 | `}, (sub) => { mre.Set(); }, null, new UserCredentials("admin` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_to_a_persistent_subscription.cs` | 323 | `_resetEvent.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_to_a_persistent_subscription.cs` | 379 | `_resetEvent.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_to_a_persistent_subscription.cs` | 435 | `_resetEvent.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_to_a_persistent_subscription.cs` | 495 | `_resetEvent.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_to_a_persistent_subscription.cs` | 539 | `_resetEvent.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_to_a_persistent_subscription.cs` | 609 | `_resetEvent.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_to_a_persistent_subscription.cs` | 674 | `_resetEvent.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_to_a_persistent_subscription.cs` | 737 | `_resetEvent.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_to_a_persistent_subscription.cs` | 787 | `_resetEvent.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/isjson_flag_on_event.cs` | 86 | `done.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/catch_up_subscription_handles_errors.cs` | 290 | `finalEvent.Set();` |
| src | `src/KurrentDB.Core.Tests/ClientAPI/connecting_to_a_persistent_subscription_async.cs` | 197 | `_resetEvent.Set();` |

*... and 138 more*

**Repos:** src

### Redis.Read (121 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Tests/Cluster/EventStoreClientCacheTests.cs` | 49 | `var client = sut.Get(new IPEndPoint(IPAddress.Loopback, 1113` |
| src | `src/KurrentDB.Core.Tests/Cluster/EventStoreClientCacheTests.cs` | 51 | `Assert.AreEqual(client, sut.Get(new IPEndPoint(IPAddress.Loo` |
| src | `src/KurrentDB.Core.Tests/Cluster/EventStoreClientCacheTests.cs` | 60 | `var oldClient = sut.Get(new IPEndPoint(IPAddress.Loopback, 1` |
| src | `src/KurrentDB.Core.Tests/Cluster/EventStoreClientCacheTests.cs` | 65 | `var newClient = sut.Get(new IPEndPoint(IPAddress.Loopback, 1` |
| src | `src/KurrentDB.Core.Tests/Cluster/EventStoreClientCacheTests.cs` | 66 | `newClient = sut.Get(new IPEndPoint(IPAddress.Loopback, 1113)` |
| src | `src/KurrentDB.Core.Tests/Cluster/EventStoreClientCacheTests.cs` | 87 | `var client = sut.Get(new IPEndPoint(IPAddress.Loopback, 1113` |
| src | `src/KurrentDB.Core.Tests/Integration/when_node_becomes_leader_with_unindexed_data.cs` | 152 | `var response = await _httpClient.GetAsync($"https://{httpEnd` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 119 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 163 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 198 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 254 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 269 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 313 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 327 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 377 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 413 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 444 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 481 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 514 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 547 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 580 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 611 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 649 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 777 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |
| src | `src/KurrentDB.Core.Tests/Services/UserManagementService/user_management_service.cs` | 845 | `_users.Handle(new UserManagementMessage.Get(Envelope, System` |

*... and 96 more*

**Repos:** src

## Database

### Dapper.Execute (85 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Testing/Bus/Helpers/WaitingConsumer.cs` | 34 | `((Action<DeferredExecutionTestMessage>)(deffered => deffered` |
| src | `src/KurrentDB.Core.Testing/Bus/Helpers/WaitingConsumer.cs` | 38 | `((Action<ExecutableTestMessage>)(deffered => deffered.Execut` |
| src | `src/KurrentDB.Api.V2.Tests/Modules/Indexes/StreamsClientExtensions.cs` | 77 | `ResiliencePipelines.RetrySlow.ExecuteAsync(` |
| src | `src/KurrentDB.Projections.Core.Tests/ClientAPI/when_executing_query/with_long_from_all_query/when_getting_result.cs` | 40 | `.ExecuteAsync("query", query, TimeSpan.FromMilliseconds(100)` |
| src | `src/KurrentDB.Projections.Core.Tests/ClientAPI/when_executing_query/with_long_from_all_query/when_getting_result_and_timeout_exceeded.cs` | 39 | `await ThrowsAsync<OperationTimedOutException>(() => _queryMa` |
| src | `src/KurrentDB.Api.V2/Modules/Streams/StreamsService.cs` | 56 | `return await command.Execute(context);` |
| src | `src/KurrentDB.Api.V2/Modules/Indexes/IndexesService.cs` | 58 | `var result = await _resilience.ExecuteAsync(` |
| src | `src/KurrentDB.Surge/Producers/SystemProducer.cs` | 112 | `await callback.Execute(result);` |
| src | `src/KurrentDB.Surge/Producers/SystemProducer.cs` | 123 | `return await resiliencePipeline.ExecuteAsync(` |
| src | `src/KurrentDB.Projections.Core/Services/Interpreted/JintProjectionStateHandler.cs` | 69 | `_engine.Execute(source);` |
| src | `src/KurrentDB.Licensing/Keygen/KeygenClient.cs` | 87 | `var response = await _client.ExecuteAsync<Models.ActivateMac` |
| src | `src/KurrentDB.Licensing/Keygen/KeygenClient.cs` | 102 | `var response = await _client.ExecuteAsync<Models.GetMachineR` |
| src | `src/KurrentDB.Licensing/Keygen/KeygenClient.cs` | 110 | `var response = await _client.ExecuteAsync<Models.HeartbeatRe` |
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

*... and 60 more*

**Repos:** src

### MongoDB.Read (46 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Api.V2.Tests/Fixtures/HomeAutomationTestData.cs` | 34 | `var records = events.Aggregate(` |
| src | `src/KurrentDB.Projections.Core.Tests/ClientAPI/Cluster/specification_with_standard_projections_runnning.cs` | 266 | `var expected = events.Aggregate("", (a, v) => a + ", " + v);` |
| src | `src/KurrentDB.Projections.Core.Tests/ClientAPI/Cluster/specification_with_standard_projections_runnning.cs` | 267 | `var actual = resultEvents.Aggregate(` |
| src | `src/KurrentDB.Projections.Core.Tests/ClientAPI/Cluster/specification_with_standard_projections_runnning.cs` | 270 | `var actualMeta = resultEvents.Aggregate(` |
| src | `src/KurrentDB.Projections.Core.Tests/ClientAPI/Cluster/specification_with_standard_projections_runnning.cs` | 281 | `var actual = resultEvents.Aggregate(` |
| src | `src/KurrentDB.Projections.Core.Tests/ClientAPI/Cluster/specification_with_standard_projections_runnning.cs` | 284 | `var actualMeta = resultEvents.Aggregate(` |
| src | `src/KurrentDB.Projections.Core.Tests/ClientAPI/specification_with_standard_projections_runnning.cs` | 222 | `var expected = events.Aggregate("", (a, v) => a + ", " + v);` |
| src | `src/KurrentDB.Projections.Core.Tests/ClientAPI/specification_with_standard_projections_runnning.cs` | 223 | `var actual = resultEvents.Aggregate(` |
| src | `src/KurrentDB.Projections.Core.Tests/ClientAPI/specification_with_standard_projections_runnning.cs` | 226 | `var actualMeta = resultEvents.Aggregate(` |
| src | `src/KurrentDB.Projections.Core.Tests/ClientAPI/specification_with_standard_projections_runnning.cs` | 237 | `var actual = resultEvents.Aggregate(` |
| src | `src/KurrentDB.Projections.Core.Tests/ClientAPI/specification_with_standard_projections_runnning.cs` | 240 | `var actualMeta = resultEvents.Aggregate(` |
| src | `src/KurrentDB.Api.V2/Modules/ApiErrors.cs` | 144 | `message = validationResult.Errors.Aggregate(` |
| src | `src/KurrentDB.Api.V2/Modules/Streams/StreamsService.cs` | 47 | `.AggregateAsync(` |
| src | `src/KurrentDB.Core.Testing.NUnit/Helpers/TestFixtureWithExistingEvents.cs` | 753 | `"{0} does end with: {1} the tail is: {2}", streamId, data.Ag` |
| src | `src/KurrentDB.Core.Testing.NUnit/Helpers/TestFixtureWithExistingEvents.cs` | 754 | `eventsText.Aggregate("", (a, v) => a + " " + v)));` |
| src | `src/KurrentDB.Core.Testing.NUnit/Helpers/TestFixtureWithExistingEvents.cs` | 776 | `"{0} does not end with: {1}. the tail is: {2}", streamId, da` |
| src | `src/KurrentDB.Core.Testing.NUnit/Helpers/TestFixtureWithExistingEvents.cs` | 777 | `eventsText.Aggregate("", (a, v) => a + " " + v)));` |
| src | `src/KurrentDB.Core.Testing.NUnit/Helpers/TestFixtureWithExistingEvents.cs` | 800 | `string.Format("{0} does not contain: {1}", streamId, missing` |
| src | `src/KurrentDB.NETCore.Compatibility/System.UriTemplate/UriTemplateTrieNode.cs` | 443 | `UriTemplatePathPartiallyEquivalentSet pes = this.finalCompou` |
| src | `src/KurrentDB.NETCore.Compatibility/System.UriTemplate/UriTemplateTrieNode.cs` | 468 | `UriTemplateTrieLocation nextLocation = this.nextCompoundSegm` |
| src | `src/KurrentDB.NETCore.Compatibility/System.UriTemplate/UriTemplateTrieNode.cs` | 617 | `results = collection.Find(wireData);` |
| src | `src/KurrentDB.AutoScavenge/Domain/AutoScavengeProcessManager.cs` | 430 | `var targetWriterCheckpoint = _gossip.Find(m => m.ToNodeId() ` |
| src | `src/KurrentDB.Common/DevCertificates/WindowsCertificateManager.cs` | 80 | `var existing = store.Certificates.Find(X509FindType.FindByTh` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Infrastructure/Grpc/RpcExceptions.cs` | 44 | `Description = failure.Value.Aggregate((a, b) => $"{a}, {b}")` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Infrastructure/Grpc/RpcExceptions.cs` | 59 | `Description = failure.Value.Aggregate((a, b) => $"{a}, {b}")` |

*... and 21 more*

**Repos:** src

### SQL.Select (31 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaQueries.cs` | 28 | `SELECT * FROM schemas` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaQueries.cs` | 45 | `SELECT schema_name FROM schema_versions` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaQueries.cs` | 130 | `SELECT * FROM schemas` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaQueries.cs` | 303 | `SELECT schema_name FROM schema_versions` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaQueries.cs` | 348 | `SELECT schema_name FROM schema_versions` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry.Tests/Fixtures/ClusterVNodeTestContext.Helpers.cs` | 105 | `// 			SELECT (SELECT EXISTS (FROM schemas WHERE checkpoint >` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry.Tests/Fixtures/ClusterVNodeTestContext.Helpers.cs` | 106 | `// 			    OR (SELECT EXISTS (FROM schema_versions WHERE chec` |
| src | `src/KurrentDB.SecondaryIndexing.LoadTesting/Assertions/DuckDb/DuckDbIndexingSummaryAssertion.cs` | 18 | `var categories = connection.Query<string>("select distinct c` |
| src | `src/KurrentDB.SecondaryIndexing.LoadTesting/Assertions/DuckDb/DuckDbIndexingSummaryAssertion.cs` | 27 | `var eventTypes = connection.Query<string>("select distinct e` |
| src | `src/KurrentDB.SecondaryIndexing/Indexes/EventType/EventTypeSql.cs` | 25 | `=> "select log_position, commit_position, event_number from ` |
| src | `src/KurrentDB.SecondaryIndexing/Indexes/EventType/EventTypeSql.cs` | 43 | `=> "select log_position, commit_position, event_number from ` |
| src | `src/KurrentDB.SecondaryIndexing/Indexes/EventType/EventTypeSql.cs` | 60 | `=> "select log_position, commit_position, event_number from ` |
| src | `src/KurrentDB.SecondaryIndexing/Indexes/EventType/EventTypeSql.cs` | 77 | `=> "select log_position, commit_position, event_number from ` |
| src | `src/KurrentDB.SecondaryIndexing/Indexes/Default/DefaultSql.cs` | 20 | `"select log_position, commit_position, event_number from idx` |
| src | `src/KurrentDB.SecondaryIndexing/Indexes/Default/DefaultSql.cs` | 33 | `"select log_position, commit_position, event_number from idx` |
| src | `src/KurrentDB.SecondaryIndexing/Indexes/Default/DefaultSql.cs` | 46 | `"select log_position, commit_position, event_number from idx` |
| src | `src/KurrentDB.SecondaryIndexing/Indexes/Default/DefaultSql.cs` | 59 | `"select log_position, commit_position, event_number from idx` |
| src | `src/KurrentDB.SecondaryIndexing/Indexes/Default/DefaultSql.cs` | 70 | `public static ReadOnlySpan<byte> CommandText => "select log_` |
| src | `src/KurrentDB.SecondaryIndexing/Indexes/Category/CategorySql.cs` | 23 | `"select log_position, commit_position, event_number from idx` |
| src | `src/KurrentDB.SecondaryIndexing/Indexes/Category/CategorySql.cs` | 41 | `"select log_position, commit_position, event_number from idx` |
| src | `src/KurrentDB.SecondaryIndexing/Indexes/Category/CategorySql.cs` | 58 | `"select log_position, commit_position, event_number from idx` |
| src | `src/KurrentDB.SecondaryIndexing/Indexes/Category/CategorySql.cs` | 75 | `"select log_position, commit_position, event_number from idx` |
| src | `src/KurrentDB.SecondaryIndexing/Stats/StatsSql.cs` | 12 | `public static ReadOnlySpan<byte> CommandText => "select dist` |
| src | `src/KurrentDB.SecondaryIndexing/Stats/StatsSql.cs` | 24 | `public static ReadOnlySpan<byte> CommandText => "select coun` |
| src | `src/KurrentDB.SecondaryIndexing/Stats/StatsSql.cs` | 36 | `public static ReadOnlySpan<byte> CommandText => "select coun` |

*... and 6 more*

**Repos:** src

### SQL.CreateTable (10 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaDbSchema.cs` | 15 | `CREATE TABLE IF NOT EXISTS schema_versions (` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaDbSchema.cs` | 24 | `CREATE TABLE IF NOT EXISTS schemas (` |
| src | `src/KurrentDB.SecondaryIndexing/Indexes/User/UserIndexSql.cs` | 91 | `create table if not exists "{0}"` |
| src | `src/KurrentDB.Core/TransactionLog/Scavenging/Sqlite/SqliteCollisionScavengeMap.cs` | 22 | `CREATE TABLE IF NOT EXISTS {TableName} (` |
| src | `src/KurrentDB.Core/TransactionLog/Scavenging/Sqlite/SqliteOriginalStreamScavengeMap.cs` | 60 | `CREATE TABLE IF NOT EXISTS {TableName} (` |
| src | `src/KurrentDB.Core/TransactionLog/Scavenging/Sqlite/SqliteScavengeMap.cs` | 56 | `CREATE TABLE IF NOT EXISTS {TableName} (` |
| src | `src/KurrentDB.Core/TransactionLog/Scavenging/Sqlite/SqliteChunkTimeStampRangeScavengeMap.cs` | 31 | `CREATE TABLE IF NOT EXISTS {TableName} (` |
| src | `src/KurrentDB.Core/TransactionLog/Scavenging/Sqlite/SqliteScavengeCheckpointMap.cs` | 21 | `CREATE TABLE IF NOT EXISTS {TableName} (` |
| src | `src/KurrentDB.Core/TransactionLog/Scavenging/Sqlite/SqliteMetastreamScavengeMap.cs` | 44 | `CREATE TABLE IF NOT EXISTS {TableName} (` |
| src | `src/KurrentDB.Core/TransactionLog/Scavenging/Sqlite/SqliteScavengeBackend.cs` | 150 | `cmd.CommandText = $"CREATE TABLE IF NOT EXISTS {tableName} (` |

**Repos:** src

### Dapper.Query (6 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Planes/Storage/DuckDBQueryExtensions.cs` | 20 | `foreach (var record in connection.Query(sql, param))` |
| src | `src/KurrentDB.SecondaryIndexing.LoadTesting/Assertions/DuckDb/DuckDbIndexingSummaryAssertion.cs` | 18 | `var categories = connection.Query<string>("select distinct c` |
| src | `src/KurrentDB.SecondaryIndexing.LoadTesting/Assertions/DuckDb/DuckDbIndexingSummaryAssertion.cs` | 27 | `var eventTypes = connection.Query<string>("select distinct e` |
| src | `src/KurrentDB.SecondaryIndexing.Tests/Indexes/DefaultIndexProcessorTests.cs` | 134 | `var records = connection.Query<string>("select distinct cate` |
| src | `src/KurrentDB.SecondaryIndexing.Tests/Indexes/DefaultIndexProcessorTests.cs` | 148 | `var records = connection.Query<string>("select distinct even` |
| src | `src/KurrentDB/Components/Query/QueryService.cs` | 80 | `var items = (IEnumerable<IDictionary<string, object>>)connec` |

**Repos:** src

### MongoDB.Write (6 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.XUnit.Tests/Scavenge/Infrastructure/TracingOriginalStreamScavengeMap.cs` | 26 | `_wrapped.DeleteMany(deleteArchived);` |
| src | `src/KurrentDB.Core.XUnit.Tests/Scavenge/Sqlite/SqliteOriginalStreamScavengeMapTests.cs` | 437 | `sut.DeleteMany(deleteArchived: false);` |
| src | `src/KurrentDB.Core.XUnit.Tests/Scavenge/Sqlite/SqliteOriginalStreamScavengeMapTests.cs` | 464 | `sut.DeleteMany(deleteArchived: true);` |
| src | `src/KurrentDB.Core/TransactionLog/Scavenging/ScavengeState.cs` | 322 | `_originalStreamDatas.DeleteMany(deleteArchived: deleteArchiv` |
| src | `src/KurrentDB.Core/TransactionLog/Scavenging/CollisionManagement/OriginalStreamCollisionMap.cs` | 82 | `_collisions.DeleteMany(deleteArchived: deleteArchived);` |
| src | `src/KurrentDB.Core/TransactionLog/Scavenging/CollisionManagement/OriginalStreamCollisionMap.cs` | 83 | `_nonCollisions.DeleteMany(deleteArchived: deleteArchived);` |

**Repos:** src

### SQL.Insert (3 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaProjections.cs` | 21 | `INSERT INTO schema_versions` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaProjections.cs` | 35 | `INSERT INTO schemas` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaProjections.cs` | 84 | `INSERT INTO schema_versions VALUES (` |

**Repos:** src

### SQL.Delete (3 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaProjections.cs` | 202 | `DELETE FROM schema_versions` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaProjections.cs` | 239 | `DELETE FROM schema_versions` |
| src | `src/SchemaRegistry/KurrentDB.SchemaRegistry/Modules/Schemas/Data/SchemaProjections.cs` | 245 | `DELETE FROM schemas` |

**Repos:** src

## Storage

### File.Write (114 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Tests/Configuration/ClusterNodeOptionsTests/when_building/with_secure_tcp.cs` | 48 | `using var fileStream = File.Create(filePath);` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 23 | `File.WriteAllBytes(_certPath, _leaf.Export(X509ContentType.C` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 24 | `File.WriteAllText(_keyPath, _leaf.PemPrivateKey());` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 45 | `File.WriteAllBytes(_certPath, _leaf.Export(X509ContentType.C` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 46 | `File.WriteAllText(_keyPath, wrongKey.ExportRSAPrivateKey().P` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 64 | `File.WriteAllText(_certPath, _leaf.Export(X509ContentType.Ce` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 65 | `File.WriteAllText(_keyPath, _leaf.PemPrivateKey());` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 86 | `File.WriteAllText(_certPath, _leaf.Export(X509ContentType.Ce` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 87 | `File.WriteAllText(_keyPath, wrongKey.ExportRSAPrivateKey().P` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 105 | `File.WriteAllBytes(_certPath, _leaf.ExportToPkcs12(Password)` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 124 | `File.WriteAllText(_certPath, _leaf.Export(X509ContentType.Ce` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 127 | `File.WriteAllText(_privateKeyPath, _leaf.PemPkcs8PrivateKey(` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 147 | `File.WriteAllText(_certPath, _leaf.Export(X509ContentType.Ce` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 150 | `File.WriteAllText(_privateKeyPath, _leaf.EncryptedPemPkcs8Pr` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 169 | `File.WriteAllBytes(_certPath, _leaf.ExportToPkcs12(Password)` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 198 | `File.WriteAllBytes(_certPath, builder.Encode());` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 219 | `File.WriteAllText(_certPath, leaf + intermediate);` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 220 | `File.WriteAllText(_keyPath, _leaf.PemPrivateKey());` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 245 | `File.WriteAllText(_certPath, leaf + intermediate);` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 246 | `File.WriteAllText(_keyPath, wrongKey.ExportRSAPrivateKey().P` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 267 | `File.WriteAllText(_certPath, intermediate + leaf);` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 268 | `File.WriteAllText(_keyPath, _leaf.PemPrivateKey());` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 298 | `File.WriteAllBytes(_certPath, builder.Encode());` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 331 | `File.WriteAllBytes(_certPath, builder.Encode());` |
| src | `src/KurrentDB.Core.Tests/Certificates/with_certificate_files.cs` | 364 | `File.WriteAllBytes(_certPath, builder.Encode());` |

*... and 89 more*

**Repos:** src

### File.Read (33 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Core.Tests/Index/IndexV1/saving_index_with_single_item_to_a_file.cs` | 65 | `using (var fs = File.OpenRead(_filename))` |
| src | `src/KurrentDB.Core.Tests/Index/IndexV1/index_map_should_detect_corruption.cs` | 69 | `var lines = File.ReadAllLines(_indexMapFileName);` |
| src | `src/KurrentDB.Core.Tests/Index/IndexV1/index_map_should_detect_corruption.cs` | 78 | `var lines = File.ReadAllLines(_indexMapFileName);` |
| src | `src/KurrentDB.Core.Tests/Index/IndexV1/index_map_should_detect_corruption.cs` | 117 | `var lines = File.ReadAllLines(_indexMapFileName);` |
| src | `src/KurrentDB.Core.Tests/Index/IndexV1/index_map_should_detect_corruption.cs` | 126 | `var lines = File.ReadAllLines(_indexMapFileName);` |
| src | `src/KurrentDB.Core.Tests/Index/IndexV1/index_map_should_detect_corruption.cs` | 135 | `var lines = File.ReadAllLines(_indexMapFileName);` |
| src | `src/KurrentDB.Core.Tests/Index/IndexV1/saving_index_with_six_items_to_a_file.cs` | 70 | `using (var fs = File.OpenRead(_filename))` |
| src | `src/KurrentDB.Core.Tests/Index/IndexVAny/saving_empty_index_to_a_file.cs` | 35 | `using (var fs = File.OpenRead(_filename))` |
| src | `src/KurrentDB.Core.Tests/Index/IndexVAny/when_opening_v1_indexmap.cs` | 44 | `Assert.AreEqual(V2FileContents, File.ReadAllText(v2File));` |
| src | `src/KurrentDB.Core.Tests/Index/IndexVAny/when_opening_v1_indexmap.cs` | 72 | `var lines = File.ReadAllLines(newIndexFile);` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/Unbuffered/UnbufferedTests.cs` | 521 | `var read = File.ReadAllBytes(filename);` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/Truncation/when_truncating_into_the_middle_of_ongoing_chunk.cs` | 89 | `using (var fs = File.OpenRead(GetFilePathFor("chunk-000000.0` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/Truncation/when_truncating_into_the_middle_of_ongoing_chunk.cs` | 101 | `using (var fs = File.OpenRead(fileInfo.FullName)) {` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/Truncation/when_truncating_into_the_middle_of_completed_chunk.cs` | 91 | `using (var fs = File.OpenRead(GetFilePathFor("chunk-000000.0` |
| src | `src/KurrentDB.Core.Tests/TransactionLog/Truncation/when_truncating_into_the_middle_of_completed_chunk.cs` | 103 | `using (var fs = File.OpenRead(fileInfo.FullName)) {` |
| src | `src/KurrentDB.Core.Tests/Http/Streams/basic.cs` | 721 | `_data = File.ReadAllBytes(fileData);` |
| src | `src/KurrentDB.SystemRuntime/Diagnostics/ProcessStats.cs` | 29 | `foreach (var line in File.ReadLines(procIoFile)) {` |
| src | `src/KurrentDB.Security.EncryptionAtRest/MasterKeySources/File/FileSource.cs` | 49 | `var lines = System.IO.File.ReadAllLines(file);` |
| src | `src/KurrentDB.Projections.Core.Tests/Playground/Launchpad3.cs` | 56 | `var query = File.ReadAllText(Path.Combine(_binFolder, @"Quer` |
| src | `src/KurrentDB.SourceGenerators.Tests/Messaging/GeneratorTests.cs` | 19 | `private static string ReadFile(string fileName) => File.Read` |
| src | `src/KurrentDB.Core.XUnit.Tests/Services/Archive/Storage/BlobStorageTests.cs` | 92 | `var localContent = await File.ReadAllBytesAsync(localPath);` |
| src | `src/KurrentDB.Core.XUnit.Tests/Services/Archive/Storage/BlobStorageTests.cs` | 119 | `var localContent = await File.ReadAllBytesAsync(localPath);` |
| src | `src/KurrentDB.Core.XUnit.Tests/Services/Archive/Storage/BlobStorageTests.cs` | 149 | `var localContent = await File.ReadAllBytesAsync(localPath);` |
| src | `src/KurrentDB.Core.XUnit.Tests/Services/Archive/Storage/BlobStorageTests.cs` | 177 | `var localContent = await File.ReadAllBytesAsync(localPath);` |
| src | `src/KurrentDB.Core/Certificates/CertificateUtils.cs` | 35 | `var pkcs12Info = Pkcs12Info.Decode(File.ReadAllBytes(certifi` |

*... and 8 more*

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

## Connector

### IMessageAdapter (4 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Transport.Http/EntityManagement/CoreHttpRequestAdapter.cs` | 13 | `public class CoreHttpRequestAdapter : IHttpRequest {` |
| src | `src/KurrentDB.Transport.Http/EntityManagement/HttpListenerRequestAdapter.cs` | 12 | `public class HttpListenerRequestAdapter : IHttpRequest {` |
| src | `src/KurrentDB.Transport.Http/EntityManagement/CoreHttpResponseAdapter.cs` | 10 | `public class CoreHttpResponseAdapter : IHttpResponse {` |
| src | `src/KurrentDB.Transport.Http/EntityManagement/HttpListenerResponseAdapter.cs` | 10 | `public class HttpListenerResponseAdapter : IHttpResponse {` |

**Repos:** src

## Ui

### WPF.ViewModel (2 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| src | `src/KurrentDB.Common/Properties/JetbrainsAnnotations.cs` | 106 | `/// public class Foo : INotifyPropertyChanged {` |
| src | `src/KurrentDB/Tools/LogObserver.cs` | 14 | `public readonly ObservableCollection<LogEvent> Items = [];` |

**Repos:** src


---

*[Back to Index](../index.md)*
