# Data Source Registry

## Summary

| Type | Occurrences |
|------|-------------|
| api | 1126 |
| cache | 314 |
| messaging | 107 |
| connector | 104 |
| storage | 20 |
| database | 10 |
| config | 1 |

## Api

### gRPC (984 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 8 | `using pb = global::Google.Protobuf;` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 9 | `using pbc = global::Google.Protobuf.Collections;` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 10 | `using pbr = global::Google.Protobuf.Reflection;` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 485 | `new pbr::FileDescriptor[] { global::Google.Protobuf.WellKnow` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 9577 | `private global::Google.Protobuf.WellKnownTypes.Timestamp tim` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 9583 | `public global::Google.Protobuf.WellKnownTypes.Timestamp Time` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 9592 | `private global::Google.Protobuf.WellKnownTypes.Timestamp las` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 9598 | `public global::Google.Protobuf.WellKnownTypes.Timestamp Last` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 9997 | `Time = new global::Google.Protobuf.WellKnownTypes.Timestamp(` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 10003 | `LastTradeTs = new global::Google.Protobuf.WellKnownTypes.Tim` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 10086 | `Time = new global::Google.Protobuf.WellKnownTypes.Timestamp(` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 10093 | `LastTradeTs = new global::Google.Protobuf.WellKnownTypes.Tim` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 10183 | `Time = new global::Google.Protobuf.WellKnownTypes.Timestamp(` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 10190 | `LastTradeTs = new global::Google.Protobuf.WellKnownTypes.Tim` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 10360 | `private global::Google.Protobuf.WellKnownTypes.Timestamp tim` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 10366 | `public global::Google.Protobuf.WellKnownTypes.Timestamp Time` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 10688 | `Time = new global::Google.Protobuf.WellKnownTypes.Timestamp(` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 10757 | `Time = new global::Google.Protobuf.WellKnownTypes.Timestamp(` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 10833 | `Time = new global::Google.Protobuf.WellKnownTypes.Timestamp(` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 11246 | `private global::Google.Protobuf.WellKnownTypes.Timestamp tim` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 11252 | `public global::Google.Protobuf.WellKnownTypes.Timestamp Time` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 11525 | `Time = new global::Google.Protobuf.WellKnownTypes.Timestamp(` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 11581 | `Time = new global::Google.Protobuf.WellKnownTypes.Timestamp(` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 11642 | `Time = new global::Google.Protobuf.WellKnownTypes.Timestamp(` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/Marketdata.cs` | 11757 | `private global::Google.Protobuf.WellKnownTypes.Timestamp tim` |

*... and 959 more*

**Repos:** StockSharp

### gRPC.Server (125 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 523 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 535 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 547 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 559 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 571 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 583 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 595 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 607 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 619 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 631 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 643 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 655 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 668 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 680 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 692 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 704 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 716 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 728 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 740 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 752 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 764 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 776 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 789 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 801 | `public virtual global::System.Threading.Tasks.Task<global::S` |
| StockSharp | `Connectors/Tinkoff/Native/Protos/Generated/InstrumentsGrpc.cs` | 813 | `public virtual global::System.Threading.Tasks.Task<global::S` |

*... and 100 more*

**Repos:** StockSharp

### WebSocket (9 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Connectors/Coinbase/Native/SocketClient.cs` | 19 | `private readonly WebSocketClient _client;` |
| StockSharp | `Connectors/Bitexbook/Native/PusherClient.cs` | 25 | `private readonly WebSocketClient _client;` |
| StockSharp | `Connectors/BitStamp/Native/PusherClient.cs` | 24 | `private readonly WebSocketClient _client;` |
| StockSharp | `Connectors/Btce/Native/PusherClient.cs` | 15 | `private readonly WebSocketClient _client;` |
| StockSharp | `Connectors/FTX/FtxMessageAdapter.cs` | 6 | `private FtxWebSocketClient _wsClient;` |
| StockSharp | `Connectors/FTX/FtxMessageAdapter.cs` | 144 | `if (_wsClient is FtxWebSocketClient sc)` |
| StockSharp | `Connectors/FTX/Native/FtxWebSocketClient.cs` | 21 | `class FtxWebSocketClient : BaseLogReceiver` |
| StockSharp | `Connectors/FTX/Native/FtxWebSocketClient.cs` | 36 | `private readonly WebSocketClient _client;` |
| StockSharp | `Connectors/FTX/Native/FtxWebSocketClient.cs` | 38 | `public FtxWebSocketClient(SecureString key, SecureString sec` |

**Repos:** StockSharp

### HttpClient.DeleteAsync (5 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Tests/PermissionsTests.cs` | 538 | `var deleted = await storage.DeleteAsync("delete", Cancellati` |
| StockSharp | `Tests/PermissionsTests.cs` | 551 | `var deleted = await storage.DeleteAsync("nonexistent", Cance` |
| StockSharp | `Tests/FileCredentialsStorageTests.cs` | 119 | `var result = await storage.DeleteAsync("test@example.com", C` |
| StockSharp | `Tests/FileCredentialsStorageTests.cs` | 132 | `var result = await storage.DeleteAsync("nonexistent", Cancel` |
| StockSharp | `Tests/FileCredentialsStorageTests.cs` | 213 | `var result = await storage.DeleteAsync("TEST@EXAMPLE.COM", C` |

**Repos:** StockSharp

### HttpClient.GetAsync (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Tests/CsvStorageTests.cs` | 963 | `var item2 = await ((IExtendedInfoStorage)storage2).GetAsync(` |

**Repos:** StockSharp

### gRPC.Client (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Connectors/Tinkoff/TinkoffMessageAdapter.cs` | 85 | `_channel = GrpcChannel.ForAddress($"https://{prefix}{_domain` |

**Repos:** StockSharp

### HttpClient.New (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Connectors/Bitalong/BitalongMessageAdapter.cs` | 76 | `_httpClient = new HttpClient(Address, Key, Secret) { Parent ` |

**Repos:** StockSharp

## Cache

### Redis.Write (210 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 475 | `.Set(nameof(CandlePrice), CandlePrice)` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 476 | `.Set(nameof(MatchOnTouch), MatchOnTouch)` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 477 | `.Set(nameof(Failing), Failing)` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 478 | `.Set(nameof(Latency), Latency)` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 479 | `.Set(nameof(InitialOrderId), InitialOrderId)` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 480 | `.Set(nameof(InitialTradeId), InitialTradeId)` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 481 | `.Set(nameof(SpreadSize), SpreadSize)` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 482 | `.Set(nameof(MaxDepth), MaxDepth)` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 483 | `.Set(nameof(PortfolioRecalcInterval), PortfolioRecalcInterva` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 484 | `.Set(nameof(ConvertTime), ConvertTime)` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 485 | `.Set(nameof(PriceLimitOffset), PriceLimitOffset)` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 486 | `.Set(nameof(IncreaseDepthVolume), IncreaseDepthVolume)` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 487 | `.Set(nameof(CheckTradingState), CheckTradingState)` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 488 | `.Set(nameof(CheckMoney), CheckMoney)` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 489 | `.Set(nameof(CheckShortable), CheckShortable)` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 490 | `.Set(nameof(AllowStoreGenerateMessages), AllowStoreGenerateM` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 491 | `.Set(nameof(CheckTradableDates), CheckTradableDates)` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 492 | `.Set(nameof(CommissionRules), CommissionRules.Select(c => c.` |
| StockSharp | `Algo.Testing/MarketEmulatorSettings.cs` | 495 | `storage.Set(nameof(TimeZone), TimeZone);` |
| StockSharp | `Algo.Testing/HistoryMarketDataManager.cs` | 157 | `_syncRoot.Set();` |
| StockSharp | `Algo.Testing/HistoryMarketDataManager.cs` | 312 | `_syncRoot.Set();` |
| StockSharp | `Algo.Testing/HistoryMarketDataManager.cs` | 335 | `_syncRoot.Set();` |
| StockSharp | `Configuration/Permissions/PermissionCredentials.cs` | 49 | `.Set("Permission", p.Key)` |
| StockSharp | `Configuration/Permissions/PermissionCredentials.cs` | 50 | `.Set("Settings", p.Value` |
| StockSharp | `Configuration/Permissions/PermissionCredentials.cs` | 53 | `.Set("Name", p1.Key.name)` |

*... and 185 more*

**Repos:** StockSharp

### Redis.Read (104 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Configuration/ITransactionIdStorage.cs` | 144 | `ISessionTransactionIdStorage ITransactionIdStorage.Get(strin` |
| StockSharp | `Configuration/ITransactionIdStorage.cs` | 195 | `ISessionTransactionIdStorage ITransactionIdStorage.Get(strin` |
| StockSharp | `Algo.Import/ImportSettings.cs` | 392 | `ExtendedStorage = AsyncHelper.Run(() => eis.GetAsync(extende` |
| StockSharp | `Tests/SnapshotRegistryTests.cs` | 51 | `var snapDay1 = storage.Get(secId);` |
| StockSharp | `Tests/SnapshotRegistryTests.cs` | 68 | `var latest = storage.Get(secId);` |
| StockSharp | `Tests/SnapshotRegistryTests.cs` | 98 | `storage.Get(secId1).AssertNotNull();` |
| StockSharp | `Tests/SnapshotRegistryTests.cs` | 99 | `storage.Get(secId2).AssertNotNull();` |
| StockSharp | `Tests/SnapshotRegistryTests.cs` | 102 | `storage.Get(secId1).AssertNull();` |
| StockSharp | `Tests/SnapshotRegistryTests.cs` | 103 | `storage.Get(secId2).AssertNotNull();` |
| StockSharp | `Tests/SnapshotRegistryTests.cs` | 106 | `storage.Get(secId1).AssertNull();` |
| StockSharp | `Tests/SnapshotRegistryTests.cs` | 107 | `storage.Get(secId2).AssertNull();` |
| StockSharp | `Tests/SnapshotRegistryTests.cs` | 137 | `var snap1 = storage.Get(secId);` |
| StockSharp | `Tests/SnapshotRegistryTests.cs` | 151 | `var snap2 = storage.Get(secId);` |
| StockSharp | `Tests/CsvStorageTests.cs` | 963 | `var item2 = await ((IExtendedInfoStorage)storage2).GetAsync(` |
| StockSharp | `Tests/CsvStorageTests.cs` | 1063 | `var items = await storage.GetAsync(token);` |
| StockSharp | `Tests/CsvStorageTests.cs` | 1294 | `var itemsB = await storageB.GetAsync(token);` |
| StockSharp | `Tests/CsvStorageTests.cs` | 1299 | `var itemsA = await storageA.GetAsync(token);` |
| StockSharp | `Tests/IndicatorTests.cs` | 744 | `var builder = provider.Get(typeof(TimeFrameCandleMessage));` |
| StockSharp | `Tests/BufferMessageAdapterTests.cs` | 30 | `Message ISnapshotStorage.Get(object key) => Get((TKey)key);` |
| StockSharp | `Tests/TransactionIdStorageTests.cs` | 46 | `var session1 = storage.Get(_session1, persistable: false);` |
| StockSharp | `Tests/TransactionIdStorageTests.cs` | 47 | `var session2 = storage.Get(_session1, persistable: false);` |
| StockSharp | `Tests/TransactionIdStorageTests.cs` | 59 | `var session1 = storage.Get(_session1, persistable: true);` |
| StockSharp | `Tests/TransactionIdStorageTests.cs` | 60 | `var session2 = storage.Get(_session1, persistable: true);` |
| StockSharp | `Tests/TransactionIdStorageTests.cs` | 72 | `var session1 = storage.Get(_session1, persistable: true);` |
| StockSharp | `Tests/TransactionIdStorageTests.cs` | 73 | `var session2 = storage.Get(_session2, persistable: true);` |

*... and 79 more*

**Repos:** StockSharp

## Messaging

### Kafka.Consumer (102 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Diagram.Core/Elements/SecurityIndexDiagramElement.cs` | 105 | `Strategy.Subscribe(new(new SecurityLookupMessage { SecurityI` |
| StockSharp | `Diagram.Core/Elements/SubscriptionDiagramElement.cs` | 91 | `Strategy.Subscribe(_subscription);` |
| StockSharp | `Tests/ConnectorRoutingTests.cs` | 451 | `connector.Subscribe(btcSubscription);` |
| StockSharp | `Tests/ConnectorRoutingTests.cs` | 452 | `connector.Subscribe(ethSubscription);` |
| StockSharp | `Tests/ConnectorRoutingTests.cs` | 579 | `connector.Subscribe(btcSub);` |
| StockSharp | `Tests/ConnectorRoutingTests.cs` | 580 | `connector.Subscribe(ethSub);` |
| StockSharp | `Tests/ConnectorRoutingTests.cs` | 715 | `connector.Subscribe(sub);` |
| StockSharp | `Tests/ConnectorRoutingTests.cs` | 796 | `connector.Subscribe(sub);` |
| StockSharp | `Tests/ConnectorRoutingTests.cs` | 859 | `connector.Subscribe(sub);` |
| StockSharp | `Tests/ConnectorRoutingTests.cs` | 898 | `connector.Subscribe(btcSub);` |
| StockSharp | `Tests/ConnectorRoutingTests.cs` | 1005 | `connector.Subscribe(sub1);` |
| StockSharp | `Tests/ConnectorRoutingTests.cs` | 1006 | `connector.Subscribe(sub2);` |
| StockSharp | `Tests/ConnectorRoutingTests.cs` | 1083 | `connector.Subscribe(sub);` |
| StockSharp | `Tests/ConnectorRoutingTests.cs` | 1124 | `connector.Subscribe(sub);` |
| StockSharp | `Tests/StrategyDecomposedTests.cs` | 499 | `registry.Subscribe(sub);` |
| StockSharp | `Tests/StrategyDecomposedTests.cs` | 520 | `registry.Subscribe(sub);` |
| StockSharp | `Tests/StrategyDecomposedTests.cs` | 539 | `registry.Subscribe(sub1);` |
| StockSharp | `Tests/StrategyDecomposedTests.cs` | 540 | `registry.Subscribe(sub2);` |
| StockSharp | `Tests/StrategyDecomposedTests.cs` | 572 | `registry.Subscribe(sub);` |
| StockSharp | `Tests/StrategyDecomposedTests.cs` | 588 | `registry.Subscribe(sub);` |
| StockSharp | `Tests/StrategyDecomposedTests.cs` | 602 | `registry.Subscribe(sub);` |
| StockSharp | `Tests/StrategyDecomposedTests.cs` | 627 | `registry.Subscribe(sub);` |
| StockSharp | `Tests/StrategyDecomposedTests.cs` | 854 | `strategy.Subscriptions.Subscribe(trackedSub);` |
| StockSharp | `Tests/StrategyDecomposedTests.cs` | 890 | `strategy.Subscriptions.Subscribe(sub);` |
| StockSharp | `Tests/StrategyDecomposedTests.cs` | 909 | `strategy.Subscriptions.Subscribe(sub);` |

*... and 77 more*

**Repos:** StockSharp

### Kafka.Topic (5 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Connectors/Coinbase/Native/SocketClient.cs` | 191 | `public const string Subscribe = "subscribe";` |
| StockSharp | `Connectors/Coinbase/Native/SocketClient.cs` | 192 | `public const string UnSubscribe = "unsubscribe";` |
| StockSharp | `Connectors/Bitexbook/Native/PusherClient.cs` | 168 | `public const string Subscribe = "subscribe";` |
| StockSharp | `Connectors/BitStamp/Native/PusherClient.cs` | 173 | `public const string Subscribe = "subscribe";` |
| StockSharp | `Connectors/BitStamp/Native/PusherClient.cs` | 174 | `public const string UnSubscribe = "unsubscribe";` |

**Repos:** StockSharp

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

## Storage

### File.Read (15 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Localization.Extractor/Program.cs` | 72 | `var strings = File.ReadAllText(file).DeserializeObject<IDict` |
| StockSharp | `Localization.Extractor/Program.cs` | 109 | `var translates = File.ReadAllText(settings.JsonFile).Deseria` |
| StockSharp | `Localization.Extractor/Program.cs` | 118 | `strings.AddRange(File.ReadAllText(langFile).DeserializeObjec` |
| StockSharp | `Localization.Extractor/Program.cs` | 141 | `var lines = File.ReadAllText($@"{_locPath}{_stringsFile}").D` |
| StockSharp | `Localization.Extractor/Program.cs` | 147 | `var strings = File.ReadAllText(file).DeserializeObject<IDict` |
| StockSharp | `Localization.Extractor/Program.cs` | 202 | `var dict = File.ReadAllText(file).DeserializeObject<IDiction` |
| StockSharp | `Tests/IndicatorTests.cs` | 1367 | `var data = Do.Invariant(() => File.ReadAllLines(Path.Combine` |
| StockSharp | `Tests/AsmInit.cs` | 25 | `await CompilationExtensions.Init(Paths.FileSystem, Helper.Lo` |
| StockSharp | `Tests/CompilationTests.cs` | 80 | `var sourceCode = await File.ReadAllTextAsync(scriptFile, tok` |
| StockSharp | `Tests/CompilationTests.cs` | 126 | `? await File.ReadAllTextAsync(Path.Combine(folderPath, "Prop` |
| StockSharp | `Tests/CompilationTests.cs` | 166 | `var sourceCode = await File.ReadAllTextAsync(scriptFile, tok` |
| StockSharp | `Tests/CompilationTests.cs` | 490 | `var sourceCode = File.ReadAllText(Path.Combine(_designerFold` |
| StockSharp | `Tests/CompilationTests.cs` | 529 | `var sourceCode = File.ReadAllText(Path.Combine(_designerFold` |
| StockSharp | `Tests/CompilationTests.cs` | 572 | `var sourceCode = File.ReadAllText(Path.Combine(_designerFold` |
| StockSharp | `Tests/ReportTests.cs` | 180 | `var expected = File.ReadAllText(expectedPath);` |

**Repos:** StockSharp

### File.Write (5 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Localization.Extractor/Program.cs` | 74 | `File.WriteAllText(file, ordered.ToJson());` |
| StockSharp | `Localization.Extractor/Program.cs` | 122 | `File.WriteAllText(langFile, strings.ToJson());` |
| StockSharp | `Localization.Extractor/Program.cs` | 222 | `File.WriteAllText(file, ordered.ToJson());` |
| StockSharp | `Tests/StrategyReportTemplateHelper.cs` | 141 | `using var file = File.Create(filePath);` |
| StockSharp | `Samples/07_Testing/04_HistoryConsole/Program.cs` | 226 | `await using var stream = File.OpenWrite(reportPath);` |

**Repos:** StockSharp

## Database

### MongoDB.Read (8 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Diagram.Core/Elements/LogicalConditionDiagramElement.cs` | 203 | `result = bools.Aggregate((a, b) => a ^ b);` |
| StockSharp | `Tests/MarketEmulatorTests.cs` | 130 | `var m = (ExecutionMessage)res.Find(x => x is ExecutionMessag` |
| StockSharp | `Tests/MarketEmulatorTests.cs` | 157 | `var m = (ExecutionMessage)res.Find(x => x is ExecutionMessag` |
| StockSharp | `Algo.Strategies/StrategyParamHelper.cs` | 451 | `totalCount = optimizeDict.Aggregate(1, (c, p) => c * p.Value` |
| StockSharp | `Algo.Strategies/StrategyParamHelper.cs` | 555 | `totalCount = optimizeDict.Aggregate(1, (c, p) => c * p.Value` |
| StockSharp | `Algo.Strategies/StrategyParamHelper.cs` | 654 | `totalCount = optimizeDict.Aggregate(1, (c, p) => c * p.Value` |
| StockSharp | `Algo/Storages/StorageHelper.cs` | 682 | `.Aggregate(folderName, (current, pair) => current.Replace(pa` |
| StockSharp | `Algo/Storages/StorageHelper.cs` | 705 | `.Aggregate(id, (current, pair) => current.ReplaceIgnoreCase(` |

**Repos:** StockSharp

### SqlClient (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Tests/AsmInit.cs` | 8 | `using Microsoft.Data.SqlClient;` |

**Repos:** StockSharp

### SQL.CreateTable (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Algo.Analytics/IAnalyticsPanel.cs` | 11 | `/// Create table to show analytics result.` |

**Repos:** StockSharp

## Config

### ConnectionString (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| StockSharp | `Tests/ExportTests.cs` | 51 | `ConnectionString = GetSecret("DB_CONNECTION_STRING"),` |

**Repos:** StockSharp


---

*[Back to Index](../index.md)*
