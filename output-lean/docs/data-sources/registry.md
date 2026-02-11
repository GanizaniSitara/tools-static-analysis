# Data Source Registry

## Summary

| Type | Occurrences |
|------|-------------|
| cache | 896 |
| storage | 141 |
| database | 61 |
| messaging | 35 |
| api | 27 |

## Cache

### Redis.Read (580 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| Lean | `Configuration/Config.cs` | 151 | `Log.Debug(Invariant($"Config.Get(): Configuration key not fo` |
| Lean | `Optimizer.Launcher/Program.cs` | 46 | `Log.FilePath = Path.Combine(Config.Get("results-destination-` |
| Lean | `Optimizer.Launcher/Program.cs` | 47 | `Log.LogHandler = Composer.Instance.GetExportedValueByTypeNam` |
| Lean | `Optimizer.Launcher/Program.cs` | 49 | `var optimizationStrategyName = Config.Get("optimization-stra` |
| Lean | `Optimizer.Launcher/Program.cs` | 51 | `var channel = Config.Get("data-channel");` |
| Lean | `Optimizer.Launcher/Program.cs` | 52 | `var optimizationId = Config.Get("optimization-id", Guid.NewG` |
| Lean | `Optimizer.Launcher/Program.cs` | 57 | `OptimizationStrategySettings = (OptimizationStrategySettings` |
| Lean | `Optimizer.Launcher/Program.cs` | 60 | `Criterion = JsonConvert.DeserializeObject<Target>(Config.Get` |
| Lean | `Optimizer.Launcher/Program.cs` | 61 | `Constraints = JsonConvert.DeserializeObject<List<Constraint>` |
| Lean | `Optimizer.Launcher/Program.cs` | 62 | `OptimizationParameters = JsonConvert.DeserializeObject<HashS` |
| Lean | `Optimizer.Launcher/Program.cs` | 67 | `var outOfSampleMaxEndDate = Config.Get("out-of-sample-max-en` |
| Lean | `Optimizer.Launcher/Program.cs` | 74 | `var optimizerType = Config.Get("optimization-launcher", type` |
| Lean | `Optimizer.Launcher/ConsoleLeanOptimizer.cs` | 45 | `_rootResultDirectory = Configuration.Config.Get("results-des` |
| Lean | `Optimizer.Launcher/ConsoleLeanOptimizer.cs` | 49 | `_leanLocation = Configuration.Config.Get("lean-binaries-loca` |
| Lean | `Optimizer.Launcher/ConsoleLeanOptimizer.cs` | 55 | `var algorithmTypeName = Configuration.Config.Get("algorithm-` |
| Lean | `Optimizer.Launcher/ConsoleLeanOptimizer.cs` | 61 | `var algorithmLanguage = Configuration.Config.Get("algorithm-` |
| Lean | `Optimizer.Launcher/ConsoleLeanOptimizer.cs` | 67 | `var algorithmLocation = Configuration.Config.Get("algorithm-` |
| Lean | `Messaging/StreamingMessageHandler.cs` | 53 | `_port = Config.Get("desktop-http-port");` |
| Lean | `Brokerages/Paper/PaperBrokerageFactory.cs` | 38 | `{ "live-cash-balance", Config.Get("live-cash-balance")},` |
| Lean | `Brokerages/Paper/PaperBrokerageFactory.cs` | 39 | `{ "live-holdings", Config.Get("live-holdings")},` |
| Lean | `DownloaderDataProvider/Program.cs` | 68 | `var dataDownloader = Composer.Instance.GetExportedValueByTyp` |
| Lean | `DownloaderDataProvider/Program.cs` | 69 | `var commandDataType = Config.Get(DownloaderCommandArguments.` |
| Lean | `DownloaderDataProvider/Program.cs` | 117 | `var downloadedData = dataDownloader.Get(downloadParameters);` |
| Lean | `DownloaderDataProvider/Program.cs` | 212 | `Log.LogHandler = Composer.Instance.GetExportedValueByTypeNam` |
| Lean | `DownloaderDataProvider/Program.cs` | 215 | `var mapFileProvider = Composer.Instance.GetExportedValueByTy` |

*... and 555 more*

**Repos:** Lean

### Redis.Write (316 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| Lean | `Optimizer.Launcher/Program.cs` | 83 | `endedEvent.Set();` |
| Lean | `Optimizer.Launcher/Program.cs` | 92 | `endedEvent.Set();` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 285 | `connectedEvent.Set();` |
| Lean | `Brokerages/DefaultConnectionHandler.cs` | 92 | `waitHandle.Set();` |
| Lean | `Brokerages/BrokerageConcurrentMessageHandler.cs` | 167 | `_messagesProcessedEvent.Set();` |
| Lean | `Brokerages/BaseWebsocketsBrokerage.cs` | 222 | `EventHandler triggerEvent = (o, args) => resetEvent.Set();` |
| Lean | `Engine/DataFeeds/LiveSynchronizer.cs` | 79 | `_realTimeScheduleEventService.NewEvent += (sender, args) => ` |
| Lean | `Engine/DataFeeds/LiveSynchronizer.cs` | 188 | `_newLiveDataEmitted.Set();` |
| Lean | `Engine/DataFeeds/LiveSynchronizer.cs` | 228 | `_newLiveDataEmitted.Set();` |
| Lean | `Engine/DataFeeds/Enumerators/EnqueueableEnumerator.cs` | 86 | `_resetEvent.Set();` |
| Lean | `Engine/DataFeeds/Enumerators/EnqueueableEnumerator.cs` | 103 | `_resetEvent.Set();` |
| Lean | `Engine/DataFeeds/RealTimeScheduleEventService.cs` | 103 | `_event.Set();` |
| Lean | `Engine/DataFeeds/WorkScheduling/WeightedWorkQueue.cs` | 125 | `_workAvailableEvent.Set();` |
| Lean | `Engine/DataFeeds/WorkScheduling/WeightedWorkScheduler.cs` | 95 | `_newWorkEvent.Set();` |
| Lean | `Engine/DataFeeds/BaseDataExchange.cs` | 87 | `_manualResetEventSlim.Set();` |
| Lean | `Engine/DataFeeds/BaseDataExchange.cs` | 149 | `manualEvent.Set();` |
| Lean | `Engine/Results/LiveTradingResultHandler.cs` | 962 | `ExitEvent.Set();` |
| Lean | `Engine/Results/BacktestingResultHandler.cs` | 649 | `ExitEvent.Set();` |
| Lean | `Engine/TransactionHandlers/BrokerageTransactionHandler.cs` | 513 | `_cancelPendingOrders.Set(order.Id, order.Status);` |
| Lean | `Common/Securities/SecurityService.cs` | 128 | `SymbolCache.Set(symbol.Value, symbol);` |
| Lean | `Common/Securities/SecurityService.cs` | 178 | `if (addToSymbolCache) SymbolCache.Set(symbol.Underlying.Valu` |
| Lean | `Common/Securities/SecurityService.cs` | 183 | `if (addToSymbolCache) SymbolCache.Set(symbol.Underlying.Valu` |
| Lean | `Common/Securities/SecurityService.cs` | 188 | `if (addToSymbolCache) SymbolCache.Set(symbol.Underlying.Valu` |
| Lean | `Common/Orders/OrderTicket.cs` | 549 | `_orderStatusClosedEvent.Set();` |
| Lean | `Common/Orders/OrderTicket.cs` | 566 | `_orderSetEvent.Set();` |

*... and 291 more*

**Repos:** Lean

## Storage

### File.Read (84 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| Lean | `Configuration/Config.cs` | 106 | `return JObject.Parse(File.ReadAllText(ConfigurationFileName)` |
| Lean | `Compression/Compression.cs` | 435 | `using (var fs = File.OpenRead(source))` |
| Lean | `Compression/Compression.cs` | 548 | `using (var archive = new ZipArchive(File.OpenRead(zip)))` |
| Lean | `Compression/Compression.cs` | 595 | `using (var fstream = File.OpenRead(file))` |
| Lean | `Compression/Compression.cs` | 860 | `var stream = File.OpenRead(zipFile);` |
| Lean | `Compression/Compression.cs` | 935 | `var inStream = File.OpenRead(source);` |
| Lean | `Compression/Compression.cs` | 949 | `var inStream = File.OpenRead(source);` |
| Lean | `Compression/Compression.cs` | 992 | `using (var file = File.OpenRead(source))` |
| Lean | `Optimizer.Launcher/ConsoleLeanOptimizer.cs` | 115 | `NewResult(File.Exists(resultJson) ? File.ReadAllText(resultJ` |
| Lean | `Engine/Storage/FileHandler.cs` | 56 | `return File.ReadAllBytes(path);` |
| Lean | `Queues/JobQueue.cs` | 162 | `Algorithm = File.ReadAllBytes(AlgorithmLocation),` |
| Lean | `Queues/JobQueue.cs` | 232 | `Algorithm = File.ReadAllBytes(AlgorithmLocation),` |
| Lean | `AlgorithmFactory/Loader.cs` | 226 | `debugInformationBytes = File.ReadAllBytes(pdbFilename);` |
| Lean | `AlgorithmFactory/Loader.cs` | 231 | `debugInformationBytes = File.ReadAllBytes(mdbFilename);` |
| Lean | `AlgorithmFactory/Loader.cs` | 245 | `var assemblyBytes = File.ReadAllBytes(assemblyPath);` |
| Lean | `ToolBox/GzipStreamProvider.cs` | 34 | `var stream = new GZipStream(File.OpenRead(source), Compressi` |
| Lean | `ToolBox/Bz2StreamProvider.cs` | 31 | `yield return new BZip2InputStream(File.OpenRead(source));` |
| Lean | `ToolBox/CoarseUniverseGenerator/CoarseUniverseGeneratorProgram.cs` | 129 | `blackListedTickers = File.ReadAllLines(_blackListedTickersFi` |
| Lean | `ToolBox/CoarseUniverseGenerator/CoarseUniverseGeneratorProgram.cs` | 298 | `using (var fileStream = dailyFile.OpenRead())` |
| Lean | `ToolBox/AlgoSeekFuturesConverter/AlgoSeekFuturesConverter.cs` | 230 | `return File.ReadAllLines("AlgoSeekFuturesConverter/AlgoSeek.` |
| Lean | `ToolBox/ExchangeInfoUpdater.cs` | 57 | `var fileLines = File.ReadLines(file).ToList();` |
| Lean | `ToolBox/FileStreamProvider.cs` | 35 | `yield return File.OpenRead(source);` |
| Lean | `Common/Commands/FileCommandHandler.cs` | 104 | `contents = File.ReadAllText(commandFilePath);` |
| Lean | `Common/Securities/SymbolPropertiesDatabase.cs` | 215 | `foreach (var line in File.ReadLines(file).Where(x => !x.Star` |
| Lean | `Common/Securities/MarketHoursDatabase.cs` | 142 | `return JsonConvert.DeserializeObject<MarketHoursDatabase>(Fi` |

*... and 59 more*

**Repos:** Lean

### File.Write (57 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| Lean | `Configuration/Config.cs` | 350 | `File.WriteAllText(taget, serialized);` |
| Lean | `Compression/Compression.cs` | 64 | `using (var stream = new ZipOutputStream(File.Create(zipPath)` |
| Lean | `Compression/Compression.cs` | 105 | `using (var stream = new ZipOutputStream(File.Create(zipPath)` |
| Lean | `Compression/Compression.cs` | 150 | `using (var stream = new ZipOutputStream(File.Create(zipPath)` |
| Lean | `Compression/Compression.cs` | 396 | `using (var fileOutput = File.Create(newFileOutput))` |
| Lean | `Compression/Compression.cs` | 429 | `using (var stream = new ZipOutputStream(File.Create(destinat` |
| Lean | `Compression/Compression.cs` | 478 | `using (var stream = new ZipOutputStream(File.Create(zipPath)` |
| Lean | `Compression/Compression.cs` | 582 | `using (var zipStream = new ZipOutputStream(File.Create(desti` |
| Lean | `Compression/Compression.cs` | 905 | `using (var streamWriter = File.Create(fullZipToPath))` |
| Lean | `Engine/DataFeeds/Transport/RemoteFileSubscriptionStreamReader.cs` | 106 | `File.WriteAllBytes(LocalFileName, bytes);` |
| Lean | `Engine/Results/LiveTradingResultHandler.cs` | 402 | `File.WriteAllText(path, data);` |
| Lean | `Engine/Results/LiveTradingResultHandler.cs` | 820 | `File.AppendAllLines(path, logLines);` |
| Lean | `Engine/Results/RegressionResultHandler.cs` | 385 | `File.WriteAllText(GetResultsPath(name), JsonConvert.Serializ` |
| Lean | `Engine/Results/BaseResultsHandler.cs` | 391 | `File.WriteAllText(path, data);` |
| Lean | `Engine/Results/BaseResultsHandler.cs` | 417 | `File.WriteAllText(alphaResultsPath, JsonConvert.SerializeObj` |
| Lean | `Engine/Results/BaseResultsHandler.cs` | 600 | `File.WriteAllLines(path, logLines);` |
| Lean | `Engine/Results/BaseResultsHandler.cs` | 611 | `File.WriteAllText(GetResultsPath(name), JsonConvert.Serializ` |
| Lean | `Engine/Storage/FileHandler.cs` | 48 | `File.WriteAllBytes(path, data);` |
| Lean | `ToolBox/CoarseUniverseGenerator/CoarseUniverseGeneratorProgram.cs` | 222 | `File.WriteAllLines(filePath, coarseByDate.Value.Select(x => ` |
| Lean | `Common/Commands/FileCommandHandler.cs` | 85 | `File.WriteAllText(resultFilePath, JsonConvert.SerializeObjec` |
| Lean | `Common/Data/Auxiliary/MapFile.cs` | 167 | `File.WriteAllLines(filePath, ToCsvLines());` |
| Lean | `Common/Data/Auxiliary/FactorFile.cs` | 118 | `File.WriteAllLines(filePath, GetFileFormat());` |
| Lean | `Common/Data/DataMonitor.cs` | 247 | `File.WriteAllText(path, data);` |
| Lean | `Tests/ResearchRegressionTests.cs` | 170 | `File.WriteAllLines(templatePath, lines);` |
| Lean | `Tests/Compression/CompressionTests.cs` | 66 | `File.WriteAllBytes("entry.zip", zippedBytes);` |

*... and 32 more*

**Repos:** Lean

## Database

### Dapper.Execute (29 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| Lean | `Api/ApiConnection.cs` | 182 | `var restsharpResponse = await Client.ExecuteAsync(request).C` |
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

*... and 4 more*

**Repos:** Lean

### MongoDB.Read (22 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| Lean | `Configuration/ApplicationParser.cs` | 56 | `var matchingOption = options.Find(o => o.Name == optionKey);` |
| Lean | `Brokerages/Brokerage.cs` | 530 | `var balanceCash = balances.Find(balance => balance.Currency ` |
| Lean | `Algorithm.CSharp/RevertComboOrderPositionsAlgorithm.cs` | 153 | `return orderTickets.Aggregate(0m, (accumulatedPrice, ticket)` |
| Lean | `Algorithm.CSharp/OptionOTMExpiryOrderHasZeroPriceRegressionAlgorithm.cs` | 143 | `var exerciseOrder = orders.Find(x => x.Type == OrderType.Opt` |
| Lean | `Algorithm.CSharp/ComboOrdersFillModelAlgorithm.cs` | 190 | `var fill = fills.Find(x => x.OrderId == order.Id);` |
| Lean | `Algorithm.Framework/Alphas/PearsonCorrelationPairsTradingAlphaModel.cs` | 78 | `var maxTuple = pearsonMatrix.Find(x => x == maxValue);` |
| Lean | `Engine/Results/BacktestingResultHandler.cs` | 183 | `updates = updates.Aggregate(SeriesType.StackedArea);` |
| Lean | `Engine/TransactionHandlers/BrokerageTransactionHandler.cs` | 834 | `var openOrderQuantity = openOrderTickets.Aggregate(0m, (d, t` |
| Lean | `Common/Statistics/TradeBuilder.cs` | 424 | `if (position.PendingFills.Aggregate(0m, (d, x) => d + x.Fill` |
| Lean | `Common/Securities/Option/StrategyMatcher/OptionStrategyDefinition.cs` | 230 | `return predicates.Aggregate(new Builder(name),` |
| Lean | `Common/Securities/Option/StrategyMatcher/OptionPositionCollection.cs` | 351 | `return positions.Aggregate(this, (current, position) => curr` |
| Lean | `Common/Securities/SecurityTransactionManager.cs` | 364 | `.Aggregate(0m, (d, t) => d + t.QuantityRemaining);` |
| Lean | `Common/Securities/SecurityTransactionManager.cs` | 384 | `.Aggregate(0m, (d, t) => d + t.QuantityRemaining);` |
| Lean | `Common/Securities/CurrencyConversion/SecurityCurrencyConversion.cs` | 184 | `var securitiesBySymbol = existingSecurities.Aggregate(new Di` |
| Lean | `Common/Securities/CashBook.cs` | 79 | `return this.Aggregate(0m, (d, pair) => d + pair.Value.ValueI` |
| Lean | `Common/Orders/Fills/FillModel.cs` | 183 | `var currentPrice = fillParameters.Aggregate(0m, (accumulated` |
| Lean | `Common/Orders/OrderTicket.cs` | 522 | `.Aggregate(0m, (d, x) => d + x.AbsoluteFillQuantity * x.Fill` |
| Lean | `Common/Util/LeanData.cs` | 1066 | `var typeString = info.Find(x => SecurityTypeAsDataPath.Conta` |
| Lean | `Common/Util/LeanData.cs` | 1070 | `var foundMarket = info.Find(x => existingMarkets.Contains(x.` |
| Lean | `Tests/Engine/DataFeeds/LiveTradingDataFeedTests.cs` | 1584 | `Assert.AreEqual(4, changes.Aggregate(0, (i, securityChanges)` |
| Lean | `Tests/Common/Securities/FakeOrderProcessor.cs` | 113 | `.Aggregate(0m, (d, t) => d + t.QuantityRemaining);` |
| Lean | `Algorithm/QCAlgorithm.Trading.cs` | 1476 | `.Aggregate(0m, (d, ticket) => d + ticket.QuantityRemaining);` |

**Repos:** Lean

### SQL.Select (10 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| Lean | `ToolBox/RandomDataGenerator/FutureSymbolGenerator.cs` | 94 | `// Randomly select one expiry from the valid set` |
| Lean | `Common/Data/Market/DataDictionary.cs` | 56 | `/// <param name="keySelector">Delegate used to select a key ` |
| Lean | `Common/Util/BaseExtendedDictionary.cs` | 58 | `/// <param name="keySelector">Delegate used to select a key ` |
| Lean | `Common/Util/BaseExtendedDictionary.cs` | 251 | `/// <param name="keySelector">Delegate used to select a key ` |
| Lean | `Common/Util/ReadOnlyExtendedDictionary.cs` | 48 | `/// <param name="keySelector">Delegate used to select a key ` |
| Lean | `Common/Util/LinqExtensions.cs` | 124 | `/// <param name="selector">Function used to select a value f` |
| Lean | `Algorithm/QCAlgorithm.Indicators.cs` | 638 | `/// <param name="selector">Function to select a value from t` |
| Lean | `Algorithm/QCAlgorithm.Indicators.cs` | 1039 | `/// <param name="selector">Function to select a value from t` |
| Lean | `Algorithm/QCAlgorithm.Indicators.cs` | 1434 | `/// <param name="selector">Optional function to select a val` |
| Lean | `Algorithm/QCAlgorithm.Indicators.cs` | 2342 | `/// <param name="selector">Optional function to select a val` |

**Repos:** Lean

## Messaging

### Kafka.Consumer (35 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 137 | `Log.Trace($"BrokerageMultiWebSocketSubscriptionManager.Subsc` |
| Lean | `Brokerages/LevelOneOrderBook/LevelOneServiceManager.cs` | 86 | `_subscriptionManager.Subscribe(dataConfig);` |
| Lean | `Engine/DataFeeds/DataQueueHandlerManager.cs` | 87 | `enumerator = dataHandler.Subscribe(dataConfig, immediateEmis` |
| Lean | `Engine/DataFeeds/Queues/FakeDataQueue.cs` | 123 | `_subscriptionManager.Subscribe(dataConfig);` |
| Lean | `Engine/RealTime/BacktestingRealTimeHandler.cs` | 109 | `IsolatorLimitProvider.Consume(scheduledEvents[0], time, Time` |
| Lean | `Engine/RealTime/BacktestingRealTimeHandler.cs` | 139 | `IsolatorLimitProvider.Consume(scheduledEvent, nextEventUtcTi` |
| Lean | `Engine/RealTime/LiveTradingRealTimeHandler.cs` | 109 | `IsolatorLimitProvider.Consume(scheduledEvent, time, TimeMoni` |
| Lean | `Common/IsolatorLimitResultProvider.cs` | 48 | `isolatorLimitProvider.Consume(timeProvider, () => scheduledE` |
| Lean | `Common/Data/EventBasedDataQueueHandlerSubscriptionManager.cs` | 66 | `Log.Trace("EventBasedDataQueueHandlerSubscriptionManager.Sub` |
| Lean | `Common/Extensions.cs` | 3586 | `result = dataQueueHandler.Subscribe(subscribedConfig, newDat` |
| Lean | `Common/Util/RateLimit/TokenBucket.cs` | 37 | `bucket.Consume(tokens, (long) timeout.TotalMilliseconds);` |
| Lean | `Tests/Engine/DataFeeds/DataQueueHandlerManagerTests.cs` | 59 | `var enumerator = compositeDataQueueHandler.Subscribe(GetConf` |
| Lean | `Tests/Engine/DataFeeds/DataQueueHandlerManagerTests.cs` | 74 | `var enumerator = compositeDataQueueHandler.Subscribe(GetConf` |
| Lean | `Tests/Engine/DataFeeds/DataQueueHandlerManagerTests.cs` | 105 | `var enumerator = compositeDataQueueHandler.Subscribe(dataCon` |
| Lean | `Tests/Engine/DataFeeds/DataQueueHandlerManagerTests.cs` | 107 | `Assert.DoesNotThrow(() => compositeDataQueueHandler.Subscrib` |
| Lean | `Tests/Engine/DataFeeds/DataQueueHandlerManagerTests.cs` | 119 | `var enumerator = compositeDataQueueHandler.Subscribe(dataCon` |
| Lean | `Tests/Engine/DataFeeds/DataQueueHandlerManagerTests.cs` | 171 | `enumerator = compositeDataQueueHandler.Subscribe(GetConfig()` |
| Lean | `Tests/Engine/DataFeeds/DataQueueHandlerManagerTests.cs` | 184 | `using var enumerator = compositeDataQueueHandler.Subscribe(G` |
| Lean | `Tests/Engine/DataFeeds/DataQueueHandlerManagerTests.cs` | 201 | `var enumerator = compositeDataQueueHandler.Subscribe(config,` |
| Lean | `Tests/Engine/DataFeeds/FuncDataQueueHandler.cs` | 133 | `_subscriptionManager.Subscribe(dataConfig);` |
| Lean | `Tests/Engine/DataFeeds/FuncDataQueueHandler.cs` | 147 | `_subscriptionManager.Subscribe(dataConfig);` |
| Lean | `Tests/Engine/DataFeeds/FakeDataQueueTests.cs` | 42 | `enumerators.Add(dataQueue.Subscribe(config, (_, _) => {` |
| Lean | `Tests/Common/IsolatorLimitResultProviderTests.cs` | 67 | `provider.Consume(timeProvider, code, _timeMonitor);` |
| Lean | `Tests/Common/IsolatorLimitResultProviderTests.cs` | 111 | `provider.Consume(timeProvider, code, _timeMonitor);` |
| Lean | `Tests/Common/IsolatorLimitResultProviderTests.cs` | 138 | `provider.Consume(timeProvider, code, _timeMonitor);` |

*... and 10 more*

**Repos:** Lean

## Api

### WebSocket (18 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 36 | `private readonly Func<WebSocketClientWrapper> _webSocketFact` |
| Lean | `Brokerages/BrokerageMultiWebSocketSubscriptionManager.cs` | 66 | `Func<WebSocketClientWrapper> webSocketFactory,` |
| Lean | `Brokerages/WebSocketMessage.cs` | 31 | `public WebSocketClientWrapper.MessageData Data { get; }` |
| Lean | `Brokerages/WebSocketMessage.cs` | 38 | `public WebSocketMessage(IWebSocket webSocket, WebSocketClien` |
| Lean | `Brokerages/WebSocketClientWrapper.cs` | 29 | `/// Wrapper for System.Net.Websockets.ClientWebSocket to enh` |
| Lean | `Brokerages/WebSocketClientWrapper.cs` | 31 | `public class WebSocketClientWrapper : IWebSocket` |
| Lean | `Brokerages/WebSocketClientWrapper.cs` | 38 | `private ClientWebSocket _client;` |
| Lean | `Brokerages/WebSocketClientWrapper.cs` | 85 | `Log.Trace($"WebSocketClientWrapper connection task started: ` |
| Lean | `Brokerages/WebSocketClientWrapper.cs` | 93 | `Log.Error(e, $"Error in WebSocketClientWrapper connection ta` |
| Lean | `Brokerages/WebSocketClientWrapper.cs` | 96 | `Log.Trace($"WebSocketClientWrapper connection task ended: {_` |
| Lean | `Brokerages/WebSocketClientWrapper.cs` | 141 | `Log.Error($"WebSocketClientWrapper.Close({_url}): {e}");` |
| Lean | `Brokerages/WebSocketClientWrapper.cs` | 192 | `Log.Error(e.Exception, $"WebSocketClientWrapper.OnError(): (` |
| Lean | `Brokerages/WebSocketClientWrapper.cs` | 201 | `Log.Trace($"WebSocketClientWrapper.OnOpen(): Connection open` |
| Lean | `Brokerages/WebSocketClientWrapper.cs` | 210 | `Log.Trace($"WebSocketClientWrapper.OnClose(): Connection clo` |
| Lean | `Brokerages/WebSocketClientWrapper.cs` | 220 | `Log.Trace($"WebSocketClientWrapper.HandleConnection({_url}):` |
| Lean | `Brokerages/WebSocketClientWrapper.cs` | 232 | `_client = new ClientWebSocket();` |
| Lean | `Brokerages/WebSocketClientWrapper.cs` | 287 | `ClientWebSocket webSocket,` |
| Lean | `Brokerages/WebSocketClientWrapper.cs` | 321 | `Log.Trace($"WebSocketClientWrapper.HandleConnection({_url}):` |

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

### HttpClient.GetAsync (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| Lean | `Common/Algorithm/Framework/Portfolio/SignalExports/CrunchDAOSignalExport.cs` | 220 | `using HttpResponseMessage roundIdResponse = HttpClient.GetAs` |

**Repos:** Lean


---

*[Back to Index](../index.md)*
