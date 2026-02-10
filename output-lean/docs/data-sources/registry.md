# Data Source Registry

## Summary

| Type | Occurrences |
|------|-------------|
| api | 149 |
| database | 28 |
| storage | 13 |
| messaging | 5 |

## Api

### WebSocket (141 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 31 | `public class BrokerageMultiWebSocketSubscriptionManager : Ev` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 34 | `private readonly int _maximumSymbolsPerWebSocket;` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 35 | `private readonly int _maximumWebSocketConnections;` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 36 | `private readonly Func<WebSocketClientWrapper> _webSocketFact` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 37 | `private readonly Func<IWebSocket, Symbol, bool> _subscribeFu` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 38 | `private readonly Func<IWebSocket, Symbol, bool> _unsubscribe` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 39 | `private readonly Action<WebSocketMessage> _messageHandler;` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 46 | `private readonly List<BrokerageMultiWebSocketEntry> _webSock` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 49 | `/// Initializes a new instance of the <see cref="BrokerageMu` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 52 | `/// <param name="maximumSymbolsPerWebSocket">The maximum num` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 53 | `/// <param name="maximumWebSocketConnections">The maximum nu` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 61 | `public BrokerageMultiWebSocketSubscriptionManager(` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 63 | `int maximumSymbolsPerWebSocket,` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 64 | `int maximumWebSocketConnections,` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 66 | `Func<WebSocketClientWrapper> webSocketFactory,` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 67 | `Func<IWebSocket, Symbol, bool> subscribeFunc,` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 68 | `Func<IWebSocket, Symbol, bool> unsubscribeFunc,` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 69 | `Action<WebSocketMessage> messageHandler,` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 74 | `_maximumSymbolsPerWebSocket = maximumSymbolsPerWebSocket;` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 75 | `_maximumWebSocketConnections = maximumWebSocketConnections;` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 83 | `if (_maximumWebSocketConnections > 0)` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 86 | `for (var i = 0; i < _maximumWebSocketConnections; i++)` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 88 | `var webSocket = CreateWebSocket();` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 90 | `_webSocketEntries.Add(new BrokerageMultiWebSocketEntry(symbo` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 103 | `List<BrokerageMultiWebSocketEntry> webSocketEntries;` |

*... and 116 more*

**Repos:** Lean

### HttpClient.New (8 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| Lean | `Api/ApiConnection.cs` | 102 | `_httpClient = new HttpClient() { BaseAddress = new Uri($"{ba` |
| Lean | `Engine/DataFeeds/Transport/RestSubscriptionStreamReader.cs` | 31 | `private static readonly HttpClient _client = new HttpClient(` |
| Lean | `Engine/DataFeeds/LiveOptionChainProvider.cs` | 64 | `_client = new HttpClient(new HttpClientHandler() { Automatic` |
| Lean | `Common/Extensions.cs` | 338 | `using var client = new HttpClient();` |
| Lean | `Common/Extensions.cs` | 348 | `using (var wc = new HttpClient())` |
| Lean | `Tests/Brokerages/Authentication/TokenHandlerTests.cs` | 41 | `using var client = new HttpClient(tokenHandler);` |
| Lean | `Tests/Brokerages/Authentication/TokenHandlerTests.cs` | 56 | `using var client = new HttpClient(tokenHandler);` |
| Lean | `Tests/Brokerages/Authentication/TokenHandlerTests.cs` | 71 | `using var client = new HttpClient(tokenHandler);` |

**Repos:** Lean

## Database

### Dapper (28 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| Lean | `Configuration/ApplicationParser.cs` | 89 | `application.Execute(args);` |
| Lean | `Algorithm.CSharp/PortfolioTargetTagsRegressionAlgorithm.cs` | 119 | `base.Execute(algorithm, targets);` |
| Lean | `Engine/DataFeeds/DownloaderDataProvider.cs` | 260 | `return DiskSynchronizer.Execute(key, () =>` |
| Lean | `Engine/DataFeeds/BaseDownloaderDataProvider.cs` | 45 | `_singleDownloadSynchronizer.Execute(key, singleExecution: tr` |
| Lean | `Engine/DataFeeds/BaseDownloaderDataProvider.cs` | 51 | `return _singleDownloadSynchronizer.Execute(key, () => GetStr` |
| Lean | `Common/Data/DiskDataCacheProvider.cs` | 65 | `return _synchronizer.Execute(filePath, () =>` |
| Lean | `Common/Data/DiskDataCacheProvider.cs` | 117 | `_synchronizer.Execute(filePath, singleExecution: false, () =` |
| Lean | `Common/Data/DiskDataCacheProvider.cs` | 128 | `return _synchronizer.Execute(zipFile, () =>` |
| Lean | `Common/Data/LeanDataWriter.cs` | 315 | `_keySynchronizer.Execute(filePath, singleExecution: false, (` |
| Lean | `Tests/Common/Util/KeyStringSynchronizerTests.cs` | 39 | `synchronizer.Execute(key, singleExecution: true, () =>` |
| Lean | `Tests/Common/Util/KeyStringSynchronizerTests.cs` | 41 | `synchronizer.Execute(key, singleExecution: true, () =>` |
| Lean | `Tests/Common/Util/KeyStringSynchronizerTests.cs` | 68 | `synchronizer.Execute(new string("someKey"), singleExecution:` |
| Lean | `Tests/Common/Util/KeyStringSynchronizerTests.cs` | 107 | `synchronizer.Execute("someKey", singleExecution: false, () =` |
| Lean | `Tests/Common/Util/KeyStringSynchronizerTests.cs` | 154 | `var newResult = synchronizer.Execute("someKey", () =>` |
| Lean | `Tests/Algorithm/Framework/Execution/StandardDeviationExecutionModelTests.cs` | 61 | `model.Execute(algorithm, new IPortfolioTarget[0]);` |
| Lean | `Tests/Algorithm/Framework/Execution/StandardDeviationExecutionModelTests.cs` | 118 | `model.Execute(algorithm, targets);` |
| Lean | `Tests/Algorithm/Framework/Execution/SpreadExecutionModelTests.cs` | 59 | `model.Execute(algorithm, new IPortfolioTarget[0]);` |
| Lean | `Tests/Algorithm/Framework/Execution/SpreadExecutionModelTests.cs` | 106 | `model.Execute(algorithm, targets);` |
| Lean | `Tests/Algorithm/Framework/Execution/SpreadExecutionModelTests.cs` | 161 | `model.Execute(algorithm, targets);` |
| Lean | `Tests/Algorithm/Framework/Execution/VolumeWeightedAveragePriceExecutionModelTests.cs` | 61 | `model.Execute(algorithm, new IPortfolioTarget[0]);` |
| Lean | `Tests/Algorithm/Framework/Execution/VolumeWeightedAveragePriceExecutionModelTests.cs` | 127 | `model.Execute(algorithm, targets);` |
| Lean | `Tests/Algorithm/Framework/Execution/ImmediateExecutionModelTests.cs` | 62 | `model.Execute(algorithm, new IPortfolioTarget[0]);` |
| Lean | `Tests/Algorithm/Framework/Execution/ImmediateExecutionModelTests.cs` | 122 | `model.Execute(algorithm, targets);` |
| Lean | `Tests/Algorithm/Framework/Execution/ImmediateExecutionModelTests.cs` | 166 | `model.Execute(algorithm, targets);` |
| Lean | `Tests/Algorithm/Framework/Execution/ImmediateExecutionModelTests.cs` | 205 | `model.Execute(algorithm, targets);` |

*... and 3 more*

**Repos:** Lean

## Storage

### FileStorage (13 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| Lean | `Compression/ZipStreamWriter.cs` | 48 | `_archive = ZipFile.Open(filename, ZipArchiveMode.Create);` |
| Lean | `Compression/ZipStreamWriter.cs` | 54 | `_archive = ZipFile.Open(filename, ZipArchiveMode.Update);` |
| Lean | `Compression/Compression.cs` | 64 | `using (var stream = new ZipOutputStream(File.Create(zipPath)` |
| Lean | `Compression/Compression.cs` | 105 | `using (var stream = new ZipOutputStream(File.Create(zipPath)` |
| Lean | `Compression/Compression.cs` | 150 | `using (var stream = new ZipOutputStream(File.Create(zipPath)` |
| Lean | `Compression/Compression.cs` | 396 | `using (var fileOutput = File.Create(newFileOutput))` |
| Lean | `Compression/Compression.cs` | 429 | `using (var stream = new ZipOutputStream(File.Create(destinat` |
| Lean | `Compression/Compression.cs` | 478 | `using (var stream = new ZipOutputStream(File.Create(zipPath)` |
| Lean | `Compression/Compression.cs` | 582 | `using (var zipStream = new ZipOutputStream(File.Create(desti` |
| Lean | `Compression/Compression.cs` | 905 | `using (var streamWriter = File.Create(fullZipToPath))` |
| Lean | `ToolBox/AlgoSeekFuturesConverter/AlgoSeekFuturesConverter.cs` | 277 | `var zip = ZipFile.Open(outputFileName, ZipArchiveMode.Create` |
| Lean | `Tests/Engine/DataProviders/ApiDataProviderTests.cs` | 103 | `File.Create(path).Dispose();` |
| Lean | `Logging/FileLogHandler.cs` | 44 | `() => new StreamWriter(File.Open(filepath, FileMode.Append, ` |

**Repos:** Lean

## Messaging

### RabbitMQ (4 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| Lean | `Tests/Python/PythonWrapperTests.cs` | 40 | `Assert.That(() => model.ValidateImplementationOf<IModel>(), ` |
| Lean | `Tests/Python/PythonWrapperTests.cs` | 56 | `Assert.That(() => model.ValidateImplementationOf<IModel>(), ` |
| Lean | `Tests/Python/PythonWrapperTests.cs` | 318 | `interface IModel` |
| Lean | `Tests/Python/PythonWrapperTests.cs` | 325 | `public class Model : IModel` |

**Repos:** Lean

### Kafka (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| Lean | `Common/Extensions.cs` | 2820 | `public static void ProcessUntilEmpty<T>(this IProducerConsum` |

**Repos:** Lean


---

*[Back to Index](../index.md)*
