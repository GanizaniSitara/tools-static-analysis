# Data Source Registry

## Summary

| Type | Occurrences |
|------|-------------|
| connector | 104 |
| api | 37 |
| storage | 1 |
| database | 1 |
| config | 1 |

## Connector

### IMessageAdapter (104 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Algo.Testing/EmulationMessageAdapter.cs` | 9 | `public class EmulationMessageAdapter : MessageAdapterWrapper` |
| StockSharp | `Algo.Testing/HistoryMessageAdapter.cs` | 10 | `public class HistoryMessageAdapter : MessageAdapter, IEmulat` |
| StockSharp | `Algo.Testing/MarketEmulatorAdapter.cs` | 6 | `public class MarketEmulatorAdapter : MessageAdapter` |
| StockSharp | `Tests/SecurityNativeIdMessageAdapterTests.cs` | 6 | `private sealed class TestPassThroughAdapter : PassThroughMes` |
| StockSharp | `Tests/RecordingMessageAdapter.cs` | 3 | `sealed class RecordingMessageAdapter : MessageAdapter` |
| StockSharp | `Tests/BasketMessageAdapterRoutingTests.cs` | 13 | `private sealed class TestRoutingInnerAdapter : MessageAdapte` |
| StockSharp | `Tests/BasketRoutingManagerTests.cs` | 14 | `private sealed class TestRoutingAdapter : MessageAdapter` |
| StockSharp | `Tests/AdapterRouterTests.cs` | 14 | `private sealed class TestRouterAdapter : MessageAdapter` |
| StockSharp | `Tests/StorageMessageAdapterTests.cs` | 10 | `private sealed class TestInnerAdapter : PassThroughMessageAd` |
| StockSharp | `Tests/ConnectorBasketTests.cs` | 35 | `private sealed class MockAdapter : MessageAdapter` |
| StockSharp | `Tests/FindAdaptersTests.cs` | 8 | `public class FindAdaptersTestValidAdapter(IdGenerator transa` |
| StockSharp | `Tests/FindAdaptersTests.cs` | 17 | `public class FindAdaptersTestNoIdGeneratorConstructorAdapter` |
| StockSharp | `Tests/FindAdaptersTests.cs` | 26 | `public class FindAdaptersTestPrivateConstructorAdapter : Mes` |
| StockSharp | `Tests/FindAdaptersTests.cs` | 51 | `public abstract class FindAdaptersTestAbstractAdapter(IdGene` |
| StockSharp | `Tests/FindAdaptersTests.cs` | 58 | `public class FindAdaptersTestMultipleConstructorsAdapter : M` |
| StockSharp | `Tests/ConnectorRoutingTests.cs` | 18 | `private sealed class LiveFeedCryptoAdapter : MessageAdapter` |
| StockSharp | `Tests/BasketTestBase.cs` | 13 | `protected sealed class TestBasketInnerAdapter : MessageAdapt` |
| StockSharp | `Tests/ExtensionsMethodsTests.cs` | 3528 | `private sealed class TestMessageAdapter : MessageAdapter` |
| StockSharp | `Tests/AdapterTestHarness.cs` | 3 | `class PassThroughMessageAdapter(IdGenerator transactionIdGen` |
| StockSharp | `Tests/AdapterTestHarness.cs` | 12 | `class RecordingPassThroughMessageAdapter : PassThroughMessag` |
| StockSharp | `Tests/AdapterWrapperPipelineBuilderTests.cs` | 19 | `private sealed class TestPipelineAdapter : MessageAdapter` |
| StockSharp | `Tests/CandleBuilderMessageAdapterTests.cs` | 16 | `private class MockCandleAdapter : MessageAdapter` |
| StockSharp | `Tests/PositionTests.cs` | 207 | `private class TestInnerAdapter(bool? emulate) : PassThroughM` |
| StockSharp | `Tests/RemoteStorageClientTests.cs` | 1387 | `class MockRemoteAdapter : MessageAdapter,` |
| StockSharp | `Tests/AsyncExtensionsTests.cs` | 8 | `private class MockAdapter : MessageAdapter` |

*... and 79 more*

**Repos:** StockSharp

## Api

### WebSocket (26 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Connectors/Coinbase/Native/Authenticator.cs` | 120 | `/// Generate JWT token for WebSocket authentication (CDP aut` |
| StockSharp | `Connectors/Coinbase/Native/Authenticator.cs` | 122 | `public string GenerateWebSocketJwt()` |
| StockSharp | `Connectors/Coinbase/Native/SocketClient.cs` | 19 | `private readonly WebSocketClient _client;` |
| StockSharp | `Connectors/Coinbase/Native/SocketClient.cs` | 68 | `private async ValueTask OnProcess(WebSocketMessage msg, Canc` |
| StockSharp | `Connectors/Coinbase/Native/SocketClient.cs` | 271 | `// Legacy HMAC authentication for WebSocket` |
| StockSharp | `Connectors/Coinbase/Native/SocketClient.cs` | 287 | `// CDP JWT authentication for WebSocket` |
| StockSharp | `Connectors/Coinbase/Native/SocketClient.cs` | 288 | `var jwt = _authenticator.GenerateWebSocketJwt();` |
| StockSharp | `Connectors/Bitexbook/Native/PusherClient.cs` | 25 | `private readonly WebSocketClient _client;` |
| StockSharp | `Connectors/Bitexbook/Native/PusherClient.cs` | 74 | `private async ValueTask OnProcess(WebSocketMessage msg, Canc` |
| StockSharp | `Connectors/BitStamp/Native/PusherClient.cs` | 24 | `private readonly WebSocketClient _client;` |
| StockSharp | `Connectors/BitStamp/Native/PusherClient.cs` | 73 | `private async ValueTask OnProcess(WebSocketMessage msg, Canc` |
| StockSharp | `Connectors/Btce/Native/PusherClient.cs` | 15 | `private readonly WebSocketClient _client;` |
| StockSharp | `Connectors/Btce/Native/PusherClient.cs` | 61 | `private async ValueTask OnProcess(WebSocketMessage msg, Canc` |
| StockSharp | `Connectors/FTX/FtxMessageAdapter.cs` | 6 | `private FtxWebSocketClient _wsClient;` |
| StockSharp | `Connectors/FTX/FtxMessageAdapter.cs` | 144 | `if (_wsClient is FtxWebSocketClient sc)` |
| StockSharp | `Connectors/FTX/Native/FtxWebSocketClient.cs` | 21 | `class FtxWebSocketClient : BaseLogReceiver` |
| StockSharp | `Connectors/FTX/Native/FtxWebSocketClient.cs` | 36 | `private readonly WebSocketClient _client;` |
| StockSharp | `Connectors/FTX/Native/FtxWebSocketClient.cs` | 38 | `public FtxWebSocketClient(SecureString key, SecureString sec` |
| StockSharp | `Connectors/FTX/Native/FtxWebSocketClient.cs` | 86 | `/// Closes the WebSocket connection` |
| StockSharp | `Connectors/FTX/Native/FtxWebSocketClient.cs` | 244 | `private async ValueTask OnProcess(WebSocketMessage msg, Canc` |
| StockSharp | `Connectors/FTX/Native/FtxWebSocketClient.cs` | 254 | `WebSocketResponse<Level1> level1 = Parse<WebSocketResponse<L` |
| StockSharp | `Connectors/FTX/Native/FtxWebSocketClient.cs` | 265 | `WebSocketResponse<List<Trade>> trade = Parse<WebSocketRespon` |
| StockSharp | `Connectors/FTX/Native/FtxWebSocketClient.cs` | 277 | `WebSocketResponse<OrderBook> ob = Parse<WebSocketResponse<Or` |
| StockSharp | `Connectors/FTX/Native/FtxWebSocketClient.cs` | 288 | `WebSocketResponse<Order> order = Parse<WebSocketResponse<Ord` |
| StockSharp | `Connectors/FTX/Native/FtxWebSocketClient.cs` | 299 | `WebSocketResponse<Fill> fill = Parse<WebSocketResponse<Fill>` |

*... and 1 more*

**Repos:** StockSharp

### gRPC (10 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 8 | `using grpc = global::Grpc.Core;` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/MarketdataGrpc.cs` | 8 | `using grpc = global::Grpc.Core;` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/StopordersGrpc.cs` | 8 | `using grpc = global::Grpc.Core;` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/OrdersGrpc.cs` | 8 | `using grpc = global::Grpc.Core;` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/SandboxGrpc.cs` | 8 | `using grpc = global::Grpc.Core;` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/UsersGrpc.cs` | 8 | `using grpc = global::Grpc.Core;` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/OperationsGrpc.cs` | 8 | `using grpc = global::Grpc.Core;` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/SignalsGrpc.cs` | 8 | `using grpc = global::Grpc.Core;` |
| StockSharp | `Connectors/Tinkoff/Properties/Usings.cs` | 11 | `global using global::Grpc.Core;` |
| StockSharp | `Connectors/Tinkoff/Properties/Usings.cs` | 12 | `global using global::Grpc.Net.Client;` |

**Repos:** StockSharp

### HttpClient.New (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Connectors/Bitalong/BitalongMessageAdapter.cs` | 76 | `_httpClient = new HttpClient(Address, Key, Secret) { Parent ` |

**Repos:** StockSharp

## Storage

### FileStorage (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Tests/StrategyReportTemplateHelper.cs` | 141 | `using var file = File.Create(filePath);` |

**Repos:** StockSharp

## Database

### SqlClient (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Tests/AsmInit.cs` | 8 | `using Microsoft.Data.SqlClient;` |

**Repos:** StockSharp

## Config

### ConnectionString (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Tests/ExportTests.cs` | 51 | `ConnectionString = GetSecret("DB_CONNECTION_STRING"),` |

**Repos:** StockSharp


---

*[Back to Index](../index.md)*
