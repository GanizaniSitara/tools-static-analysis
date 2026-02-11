# Data Source Registry

## Summary

| Type | Occurrences |
|------|-------------|
| cache | 941 |
| messaging | 435 |
| database | 318 |
| api | 73 |
| connector | 39 |
| config | 33 |
| storage | 21 |

## Connection Strings Found

| File | Repo | Connection Name | Value |
|------|------|----------------|-------|
| `src/examples/AppConfig/App.config` | akka.net | myConnectionString | `myDB://MyConnectionString` |

## Cache

### Redis.Read (912 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/benchmark/Akka.Cluster.Benchmarks/Sharding/ShardingInfrastructure.cs` | 41 | `Sender.Tell(new ResolveResp(entityId, Cluster.Get(Context.Sy` |
| akka.net | `src/benchmark/Akka.Cluster.Benchmarks/Sharding/ShardingInfrastructure.cs` | 252 | `var sharding = ClusterSharding.Get(system);` |
| akka.net | `src/benchmark/Akka.Cluster.Benchmarks/Sharding/ShardMessageRoutingBenchmarks.cs` | 63 | `var c1 = Cluster.Get(_sys1);` |
| akka.net | `src/benchmark/Akka.Cluster.Benchmarks/Sharding/ShardMessageRoutingBenchmarks.cs` | 64 | `var c2 = Cluster.Get(_sys2);` |
| akka.net | `src/benchmark/Akka.Cluster.Benchmarks/Sharding/ShardMessageRoutingBenchmarks.cs` | 106 | `var c1 = Cluster.Get(_sys1);` |
| akka.net | `src/benchmark/Akka.Cluster.Benchmarks/Sharding/ShardMessageRoutingBenchmarks.cs` | 107 | `var c2 = Cluster.Get(_sys2);` |
| akka.net | `src/benchmark/Akka.Cluster.Benchmarks/Sharding/ShardSpawnBenchmarks.cs` | 55 | `var c1 = Cluster.Get(_sys1);` |
| akka.net | `src/benchmark/Akka.Cluster.Benchmarks/Sharding/ShardSpawnBenchmarks.cs` | 56 | `var c2 = Cluster.Get(_sys2);` |
| akka.net | `src/benchmark/Akka.Cluster.Benchmarks/Sharding/ShardSpawnBenchmarks.cs` | 87 | `var t2 = CoordinatedShutdown.Get(_sys2).Run(CoordinatedShutd` |
| akka.net | `src/benchmark/Akka.Cluster.Benchmarks/Sharding/ShardSpawnBenchmarks.cs` | 88 | `var t1 = CoordinatedShutdown.Get(_sys1).Run(CoordinatedShutd` |
| akka.net | `src/benchmark/Akka.Cluster.Cpu.Benchmark/BenchmarkNode.cs` | 69 | `=> await CoordinatedShutdown.Get(_actorSystem).Run(Coordinat` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/ClusterClient/ClusterClientDiscoverySpec.cs` | 117 | `ClusterClientReceptionist.Get(Sys);` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/ClusterClient/ClusterClientDiscoverySpec.cs` | 143 | `await AkkaManagement.Get(Sys).Start();` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/ClusterClient/ClusterClientDiscoverySpec.cs` | 146 | `ClusterClientReceptionist.Get(Sys).RegisterService(service);` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/ClusterClient/ClusterClientDiscoverySpec.cs` | 155 | `(ConfigServiceDiscovery)Discovery.Discovery.Get(Sys).LoadSer` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/ClusterClient/ClusterClientDiscoverySpec.cs` | 192 | `await AkkaManagement.Get(Sys).Stop();` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/ClusterClient/ClusterClientDiscoverySpec.cs` | 194 | `Cluster.Get(Sys).Leave((await NodeAsync(_config.First)).Addr` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/ClusterClient/ClusterClientDiscoverySpec.cs` | 218 | `await AkkaManagement.Get(Sys).Start();` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/ClusterClient/ClusterClientDiscoverySpec.cs` | 221 | `ClusterClientReceptionist.Get(Sys).RegisterService(service);` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/ClusterClient/ClusterClientDiscoverySpec.cs` | 263 | `await AkkaManagement.Get(Sys).Stop();` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/ClusterClient/ClusterClientDiscoverySpec.cs` | 277 | `await AkkaManagement.Get(Sys).Start();` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/ClusterClient/ClusterClientDiscoverySpec.cs` | 280 | `ClusterClientReceptionist.Get(Sys).RegisterService(service);` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/ClusterClient/ClusterClientHandoverSpec.cs` | 75 | `ClusterClientReceptionist.Get(Sys);` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/ClusterClient/ClusterClientHandoverSpec.cs` | 111 | `ClusterClientReceptionist.Get(Sys).RegisterService(service);` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/ClusterClient/ClusterClientHandoverSpec.cs` | 138 | `ClusterClientReceptionist.Get(Sys).RegisterService(service);` |

*... and 887 more*

**Repos:** akka.net

### Redis.Write (29 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/examples/Cluster/ClusterSharding/ClusterSharding.Node/Program.cs` | 36 | `exitEvent.Set();` |
| akka.net | `src/examples/Cluster/ClusterSharding/ClusterSharding.Node/Program.cs` | 40 | `exitEvent.Set();` |
| akka.net | `src/examples/Cluster/ClusterSharding/ShoppingCart/Program.cs` | 34 | `exitEvent.Set();` |
| akka.net | `src/examples/Cluster/ClusterSharding/ShoppingCart/Program.cs` | 38 | `exitEvent.Set();` |
| akka.net | `src/core/Akka.Tests.Performance/IO/TcpSingleConnectionSpec.cs` | 47 | `reset.Set();` |
| akka.net | `src/core/Akka.Tests.Performance/IO/TcpSingleConnectionSpec.cs` | 69 | `reset.Set();` |
| akka.net | `src/core/Akka.Tests.Performance/IO/TcpSingleConnectionSpec.cs` | 90 | `reset.Set();` |
| akka.net | `src/core/Akka.Tests.Performance/IO/TcpSingleConnectionSpec.cs` | 105 | `reset.Set();` |
| akka.net | `src/core/Akka.Tests.Performance/IO/TcpSingleConnectionSpec.cs` | 110 | `reset.Set();` |
| akka.net | `src/core/Akka.Tests.Performance/IO/TcpInboundOnlySpec.cs` | 49 | `reset.Set();` |
| akka.net | `src/core/Akka.Tests.Performance/Actor/ActorSelectionSpecs.cs` | 52 | `_resetEvent.Set();` |
| akka.net | `src/core/Akka.Tests.Performance/Actor/ActorThroughputSpec.cs` | 68 | `_resetEvent.Set();` |
| akka.net | `src/core/Akka.Tests.Performance/Actor/ActorThroughputSpec.cs` | 99 | `_resetEvent.Set();` |
| akka.net | `src/core/Akka.Tests.Performance/Actor/ActorThroughputSpec.cs` | 127 | `_resetEvent.Set();` |
| akka.net | `src/core/Akka.Tests.Performance/Dispatch/ReceiveOnlyBenchmark.cs` | 45 | `ResetEvent.Set();` |
| akka.net | `src/core/Akka.Tests.Performance/Dispatch/DispatcherThroughputSpecBase.cs` | 68 | `EventBlock.Set();` |
| akka.net | `src/core/Akka.Tests.Performance/Dispatch/DispatcherThroughputSpecBase.cs` | 110 | `EventBlock.Set();` |
| akka.net | `src/core/Akka.Remote.Tests/RemoteDaemonSpec.cs` | 35 | `childCreatedEvent.Set();` |
| akka.net | `src/core/Akka.Streams/Actors/ActorSubscriber.cs` | 239 | `_state.Set(Self, new ActorSubscriberState.State(_subscriptio` |
| akka.net | `src/core/Akka.Streams/Actors/ActorPublisher.cs` | 604 | `_state.Set(Self, new ActorPublisherState.State(UntypedSubscr` |
| akka.net | `src/core/Akka.Tests/Actor/Scheduler/TaskBasedScheduler_ActionScheduler_Schedule_Tests.cs` | 251 | `testScheduler.ScheduleOnce(0, () => manualResetEvent.Set());` |
| akka.net | `src/core/Akka.Tests/Actor/Scheduler/TaskBasedScheduler_ActionScheduler_Schedule_Tests.cs` | 270 | `testScheduler.ScheduleRepeatedly(0, 100, () => manualResetEv` |
| akka.net | `src/core/Akka.Tests/Util/Internal/InterlockedSpinTests.cs` | 52 | `hasEnteredUpdateMethod.Set();	//Signal THREAD 1 to update sh` |
| akka.net | `src/core/Akka.Tests/Util/Internal/InterlockedSpinTests.cs` | 59 | `okToContinue.Set();	//Signal THREAD 1 it can continue in upd` |
| akka.net | `src/core/Akka.Tests/Util/Internal/InterlockedSpinTests.cs` | 96 | `hasEnteredUpdateMethod.Set();	//Signal THREAD 1 to update sh` |

*... and 4 more*

**Repos:** akka.net

## Messaging

### Kafka.Consumer (394 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/benchmark/Akka.Benchmarks/EventStream/EventStreamBenchmarks.cs` | 44 | `_eventStream.Subscribe(_fakeActor, typeof(string));` |
| akka.net | `src/contrib/dependencyinjection/Akka.DependencyInjection.Tests/RouterIntegrationSpec.cs` | 69 | `system.EventStream.Subscribe(probe, typeof(Error));` |
| akka.net | `src/contrib/dependencyinjection/Akka.DependencyInjection.Tests/RouterIntegrationSpec.cs` | 96 | `system.EventStream.Subscribe(probe, typeof(Error));` |
| akka.net | `src/contrib/dependencyinjection/Akka.DependencyInjection.Tests/RouterIntegrationSpec.cs` | 127 | `system.EventStream.Subscribe(probe, typeof(Error));` |
| akka.net | `src/contrib/dependencyinjection/Akka.DependencyInjection.Tests/BugFixSpec.cs` | 43 | `system.EventStream.Subscribe(probe, typeof(Error));` |
| akka.net | `src/contrib/testkits/Akka.TestKit.Xunit2/Internals/Loggers.cs` | 37 | `e.LoggingBus.Subscribe(Self, typeof (LogEvent));` |
| akka.net | `src/contrib/testkits/Akka.TestKit.Xunit/Internals/Loggers.cs` | 37 | `e.LoggingBus.Subscribe(Self, typeof (LogEvent));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/Singleton/ClusterSingletonManagerChaosSpec.cs` | 99 | `Cluster.Subscribe(memberProbe.Ref, new[] { typeof(ClusterEve` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/Singleton/ClusterSingletonManagerSpec.cs` | 524 | `Cluster.Subscribe(memberProbe.Ref, new[] { typeof(ClusterEve` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding.Tests/WrappedShardBufferedMessageSpec.cs` | 176 | `Sys.EventStream.Subscribe(TestActor, typeof(ShardStoreCreate` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding.Tests/WrappedShardBufferedMessageSpec.cs` | 177 | `Sys.EventStream.Subscribe(TestActor, typeof(CoordinatorStore` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding.Tests/RememberEntitiesFailureSpec.cs` | 510 | `Sys.EventStream.Subscribe(storeProbe.Ref, typeof(ShardStoreC` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding.Tests/RememberEntitiesFailureSpec.cs` | 590 | `Sys.EventStream.Subscribe(storeProbe.Ref, typeof(ShardStoreC` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding.Tests/RememberEntitiesFailureSpec.cs` | 657 | `Sys.EventStream.Subscribe(storeProbe.Ref, typeof(ShardStoreC` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding.Tests/RememberEntitiesFailureSpec.cs` | 730 | `Sys.EventStream.Subscribe(storeProbe.Ref, typeof(Coordinator` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Metrics/ClusterMetricsCollector.cs` | 93 | `_cluster.Subscribe(Self, typeof(ClusterEvent.IMemberEvent), ` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Metrics/Routing/ClusterMetricsRouting.cs` | 412 | `_extension.Subscribe(Self);` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Metrics/ClusterMetrics.cs` | 111 | `_system.EventStream.Subscribe(metricsListener, typeof(IClust` |
| akka.net | `src/contrib/cluster/Akka.DistributedData.Tests.MultiNode/ReplicatorSpec.cs` | 141 | `_replicator.Tell(Dsl.Subscribe(KeyA, changedProbe.Ref));` |
| akka.net | `src/contrib/cluster/Akka.DistributedData.Tests.MultiNode/ReplicatorSpec.cs` | 142 | `_replicator.Tell(Dsl.Subscribe(KeyX, changedProbe.Ref));` |
| akka.net | `src/contrib/cluster/Akka.DistributedData.Tests.MultiNode/ReplicatorSpec.cs` | 257 | `_replicator.Tell(Dsl.Subscribe(KeyA, changedProbe.Ref));` |
| akka.net | `src/contrib/cluster/Akka.DistributedData.Tests.MultiNode/ReplicatorSpec.cs` | 337 | `_replicator.Tell(Dsl.Subscribe(KeyC, changedProbe.Ref));` |
| akka.net | `src/contrib/cluster/Akka.DistributedData.Tests.MultiNode/ReplicatorSpec.cs` | 674 | `_replicator.Tell(Dsl.Subscribe(KeyH, changedProbe.Ref));` |
| akka.net | `src/contrib/cluster/Akka.DistributedData.Tests.MultiNode/ReplicatorSpec.cs` | 710 | `_replicator.Tell(Dsl.Subscribe(KeyI, changedProbe.Ref));` |
| akka.net | `src/contrib/cluster/Akka.DistributedData.Tests.MultiNode/DurableDataPocoSpec.cs` | 266 | `r.Tell(Dsl.Subscribe(_keyC, TestActor));` |

*... and 369 more*

**Repos:** akka.net

### Kafka.Topic (39 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/PublishSubscribe/DistributedPubSubMediatorSpec.cs` | 110 | `_mediator.Tell(new Subscribe("content", Self));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/PublishSubscribe/DistributedPubSubMediatorSpec.cs` | 426 | `var s8 = new Subscribe("topic1", CreateChatUser("u8"));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/PublishSubscribe/DistributedPubSubMediatorSpec.cs` | 429 | `var s9 = new Subscribe("topic1", CreateChatUser("u9"));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/PublishSubscribe/DistributedPubSubMediatorSpec.cs` | 436 | `var s10 = new Subscribe("topic1", CreateChatUser("u10"));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/PublishSubscribe/DistributedPubSubMediatorSpec.cs` | 705 | `var topic = "sample-topic-14";` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/PublishSubscribe/DistributedPubSubMediatorSpec.cs` | 723 | `var s1 = new Subscribe("topic_a1", CreateChatUser("u14"));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/PublishSubscribe/DistributedPubSubMediatorSpec.cs` | 727 | `var s2 = new Subscribe("topic_a1", CreateChatUser("u15"));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/PublishSubscribe/DistributedPubSubMediatorSpec.cs` | 731 | `var s3 = new Subscribe("topic_a2", CreateChatUser("u16"));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/PublishSubscribe/DistributedPubSubMediatorSpec.cs` | 739 | `var s3 = new Subscribe("topic_a1", CreateChatUser("u17"));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/PublishSubscribe/DistributedPubSubMediatorSpec.cs` | 775 | `var s1 = new Subscribe("topic_b1", CreateChatUser("u18"));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/PublishSubscribe/DistributedPubSubRestartSpec.cs` | 93 | `Mediator.Tell(new Subscribe("topic1", TestActor));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/PublishSubscribe/DistributedPubSubRestartSpec.cs` | 168 | `newMediator.Tell(new Subscribe("topic2", probe.Ref), probe.R` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests.MultiNode/PublishSubscribe/DistributedPubSubPublishWithAckSpec.cs` | 119 | `Mediator.Tell(new Subscribe("content", TestActor));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests/PublishSubscribe/DistributedPubSubMessageSerializerSpec.cs` | 105 | `var message = new SendToOneSubscriber("hello");` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests/PublishSubscribe/DistributedPubSubMediatorSpec.cs` | 73 | `mediator.Tell(new Subscribe("pub-sub", actor));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests/PublishSubscribe/DistributedPubSubMediatorRouterSpec.cs` | 111 | `mediator.Tell(new Subscribe("topic", TestActor));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests/PublishSubscribe/DistributedPubSubMediatorRouterSpec.cs` | 123 | `mediator.Tell(new Subscribe("topic", TestActor, "group"));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests/PublishSubscribe/DistributedPubSubPublishWithAckSpec.cs` | 48 | `mediator.Tell(new Subscribe("topic2", TestActor));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests/PublishSubscribe/DistributedPubSubPublishWithAckSpec.cs` | 54 | `mediator.Tell(new Subscribe("topic", TestActor));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests/PublishSubscribe/DistributedPubSubPublishWithAckSpec.cs` | 60 | `PredicateInfo.Create<PublishSucceeded>(msg => msg.Message is` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests/PublishSubscribe/DistributedPubSubPublishWithAckSpec.cs` | 62 | `PredicateInfo.Create<PublishSucceeded>(msg => msg.Message is` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests/PublishSubscribe/DistributedPubSubPublishWithAckSpec.cs` | 89 | `mediator.Tell(new Subscribe("topic", TestActor));` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests/PublishSubscribe/DistributedPubSubPublishWithAckSpec.cs` | 95 | `PredicateInfo.Create<PublishSucceeded>(msg => msg.Message is` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests/PublishSubscribe/DistributedPubSubPublishWithAckSpec.cs` | 97 | `PredicateInfo.Create<PublishSucceeded>(msg => msg.Message is` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools.Tests/PublishSubscribe/DistributedPubSubPublishWithAckSpec.cs` | 121 | `mediator.Tell(new Subscribe("topic", TestActor));` |

*... and 14 more*

**Repos:** akka.net

### Kafka.Producer (2 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/core/Akka/Actor/Props.cs` | 562 | `return _producer.Produce();` |
| akka.net | `src/core/Akka/Dispatch/Dispatcher.cs` | 57 | `_executor = new FastLazy<ExecutorService>(() => executorServ` |

**Repos:** akka.net

## Database

### MongoDB.Read (178 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/benchmark/Akka.Benchmarks/Cluster/VectorClockBenchmarks.cs` | 33 | `.Aggregate((VectorClock.Create(), ImmutableSortedSet<Node>.E` |
| akka.net | `src/benchmark/Akka.Benchmarks/Cluster/VectorClockBenchmarks.cs` | 44 | `var versions = vc.Versions.Aggregate(ImmutableSortedDictiona` |
| akka.net | `src/benchmark/Akka.Benchmarks/Cluster/ReachabilityBenchmarks.cs` | 35 | `return Enumerable.Range(1, size).Aggregate(baseReachability,` |
| akka.net | `src/benchmark/Akka.Benchmarks/Cluster/ReachabilityBenchmarks.cs` | 49 | `return observers.Aggregate(baseReachability, (r, o) =>` |
| akka.net | `src/benchmark/Akka.Benchmarks/Cluster/ReachabilityBenchmarks.cs` | 51 | `return Enumerable.Range(1, 5).Aggregate(r, (r2, _) =>` |
| akka.net | `src/benchmark/Akka.Benchmarks/DData/VersionVectorBenchmark.cs` | 38 | `.Aggregate((VersionVector.Empty, ImmutableSortedSet<UniqueAd` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Metrics/Routing/MetricSelectors.cs` | 175 | `return combined.Aggregate(init, (acc, pair) =>` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Metrics/Serialization/ClusterMetricsMessageSerializer.cs` | 209 | `var allMetricNames = allNodeMetrics.Aggregate(` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Metrics/Serialization/MetricsGossip.cs` | 56 | `return otherGossip.Nodes.Aggregate(this, (gossip, node) => g` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/ORDictionary.cs` | 107 | `elements.Aggregate(ORDictionary<TKey, TValue>.Empty, (acc, t` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/ORDictionary.cs` | 110 | `elements.Aggregate(ORDictionary<TKey, TValue>.Empty, (acc, t` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/ORDictionary.cs` | 361 | `KeySet.ModifiedByNodes.Union(ValueMap.Aggregate(ImmutableHas` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/ORDictionary.cs` | 381 | `var prunedValues = ValueMap.Aggregate(ValueMap, (acc, kv) =>` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/ORDictionary.cs` | 394 | `var pruningCleanupValues = ValueMap.Aggregate(ValueMap, (acc` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/GCounter.cs` | 89 | `Value = State.Aggregate(Zero, (v, acc) => v + acc.Value);` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/LWWDictionary.cs` | 99 | `elements.Aggregate(LWWDictionary<TKey, TValue>.Empty, (dicti` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/LWWDictionary.cs` | 110 | `elements.Aggregate(LWWDictionary<TKey, TValue>.Empty, (dicti` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/DeltaPropagationSelector.cs` | 107 | `deltaGroup = deltaEntriesAfterJ.Values.Aggregate((d1, d2) =>` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/Internal/Internal.cs` | 491 | `var cleanedDeltaVersions = removedNodes.Aggregate(DeltaVersi` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/Internal/Internal.cs` | 492 | `var cleanedOtherDeltaVersions = removedNodes.Aggregate(other` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/Internal/Internal.cs` | 525 | `private IReplicatedData Cleaned(IReplicatedData c, IImmutabl` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/ORMultiValueDictionary.cs` | 158 | `bucket.Aggregate(old.Clear(node), (set, element) => set.Add(` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/ORSet.cs` | 98 | `elements.Aggregate(ORSet<T>.Empty, (set, kv) => set.Add(kv.K` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/ORSet.cs` | 101 | `elements.Aggregate(ORSet<T>.Empty, (set, kv) => set.Add(kv.K` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/ORSet.cs` | 186 | `internal static ImmutableDictionary<T, VersionVector> MergeC` |

*... and 153 more*

**Repos:** akka.net

### Dapper.Execute (122 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 292 | `var result = await command.ExecuteScalarAsync(cts.Token);` |
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 371 | `await command.ExecuteScalarAsync(cts.Token);` |
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 428 | `var res = await highestSeqNrCommand.ExecuteScalarAsync(cts.T` |
| akka.net | `src/core/Akka.Streams.Tests/IO/OutputStreamSourceSpec.cs` | 101 | `await probe.AsyncBuilder().ExpectNext(_byteString).ExecuteAs` |
| akka.net | `src/core/Akka.Streams.Tests/IO/OutputStreamSourceSpec.cs` | 104 | `await probe.AsyncBuilder().ExpectComplete().ExecuteAsync();` |
| akka.net | `src/core/Akka.Streams.Tests/Implementation/Fusing/GraphInterpreterSpecKit.cs` | 39 | `public void StepAll() => Interpreter.Execute(int.MaxValue);` |
| akka.net | `src/core/Akka.Streams.Tests/Implementation/Fusing/GraphInterpreterSpecKit.cs` | 41 | `public virtual void Step() => Interpreter.Execute(1);` |
| akka.net | `src/core/Akka.Streams.Tests/Implementation/Fusing/GraphInterpreterSpecKit.cs` | 411 | `Interpreter.Execute(eventLimit);` |
| akka.net | `src/core/Akka.Streams.Tests/Implementation/Fusing/GraphInterpreterSpecKit.cs` | 419 | `Interpreter.Execute(eventLimit);` |
| akka.net | `src/core/Akka.Streams.Tests/Implementation/Fusing/GraphInterpreterSpecKit.cs` | 427 | `Interpreter.Execute(eventLimit);` |
| akka.net | `src/core/Akka.Streams.Tests/Implementation/Fusing/GraphInterpreterSpecKit.cs` | 459 | `Interpreter.Execute(eventLimit);` |
| akka.net | `src/core/Akka.Streams.Tests/Implementation/Fusing/GraphInterpreterSpecKit.cs` | 467 | `Interpreter.Execute(eventLimit);` |
| akka.net | `src/core/Akka.Streams.Tests/Implementation/Fusing/GraphInterpreterSpecKit.cs` | 539 | `public override void Step() => Interpreter.Execute(!_chasing` |
| akka.net | `src/core/Akka.Streams.Tests/Implementation/Fusing/GraphInterpreterSpecKit.cs` | 944 | `protected sealed override void Run() => Interpreter.Execute(` |
| akka.net | `src/core/Akka.Streams.Tests/Implementation/GraphStageLogicSpec.cs` | 491 | `interpreter.Execute(2);` |
| akka.net | `src/core/Akka.Streams.Tests/Implementation/TimeoutsSpec.cs` | 186 | `.ExecuteAsync();` |
| akka.net | `src/core/Akka.Streams.Tests/Implementation/TimeoutsSpec.cs` | 226 | `.ExecuteAsync();` |
| akka.net | `src/core/Akka.Streams.Tests/Implementation/TimeoutsSpec.cs` | 232 | `.ExecuteAsync();` |
| akka.net | `src/core/Akka.Streams.Tests/Implementation/TimeoutsSpec.cs` | 251 | `.ExecuteAsync();` |
| akka.net | `src/core/Akka.Streams.Tests/Implementation/TimeoutsSpec.cs` | 257 | `.ExecuteAsync();` |
| akka.net | `src/core/Akka.Streams.Tests/Implementation/TimeoutsSpec.cs` | 282 | `.ExecuteAsync();` |
| akka.net | `src/core/Akka.Streams.Tests/Dsl/FlowGroupBySpec.cs` | 145 | `.ExecuteAsync();` |
| akka.net | `src/core/Akka.Streams.Tests/Dsl/FlowGroupBySpec.cs` | 152 | `.ExecuteAsync();` |
| akka.net | `src/core/Akka.Streams.Tests/Dsl/FlowGroupBySpec.cs` | 194 | `.ExecuteAsync();` |
| akka.net | `src/core/Akka.Streams.Tests/Dsl/FlowGroupBySpec.cs` | 440 | `.ExecuteAsync();` |

*... and 97 more*

**Repos:** akka.net

### SQL.Delete (4 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/examples/Akka.Persistence.Custom/Snapshot/SqliteSnapshotStore.cs` | 55 | `DELETE FROM snapshot` |
| akka.net | `src/examples/Akka.Persistence.Custom/Snapshot/SqliteSnapshotStore.cs` | 62 | `DELETE FROM snapshot` |
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 96 | `DELETE FROM event_journal` |
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 98 | `DELETE FROM journal_metadata` |

**Repos:** akka.net

### SQL.CreateTable (3 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/examples/Akka.Persistence.Custom/Snapshot/SqliteSnapshotStore.cs` | 27 | `CREATE TABLE IF NOT EXISTS snapshot (` |
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 30 | `CREATE TABLE IF NOT EXISTS event_journal (` |
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 42 | `CREATE TABLE IF NOT EXISTS journal_metadata (` |

**Repos:** akka.net

### SQL.Select (3 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 67 | `SELECT MAX(e.sequence_nr) as SeqNr FROM event_journal e` |
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 70 | `SELECT MAX(m.sequence_nr) as SeqNr FROM journal_metadata m` |
| akka.net | `src/core/Akka/Util/Internal/ArrayExtensions.cs` | 110 | `/// Select all the items in this array from the beginning un` |

**Repos:** akka.net

### SQL.Update (3 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/core/Akka/Util/ConcurrentSet.cs` | 63 | `/// <param name="concurrencyLevel">The estimated number of t` |
| akka.net | `src/core/Akka/Util/ConcurrentSet.cs` | 73 | `/// <param name="concurrencyLevel">The estimated number of t` |
| akka.net | `src/core/Akka/Util/ConcurrentSet.cs` | 85 | `/// <param name="concurrencyLevel">The estimated number of t` |

**Repos:** akka.net

### SQL.Insert (2 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 76 | `INSERT INTO event_journal (` |
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 104 | `INSERT INTO journal_metadata (persistence_id, sequence_nr)` |

**Repos:** akka.net

### MongoDB.Write (2 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/core/Akka.Persistence.TestKit.Tests/TestSnapshotStoreSpec.cs` | 95 | `actor.Tell(new SnapshotActor.DeleteOne(nr), TestActor);` |
| akka.net | `src/core/Akka.Persistence.TestKit.Tests/TestSnapshotStoreSpec.cs` | 99 | `actor.Tell(new SnapshotActor.DeleteOne(nr), TestActor);` |

**Repos:** akka.net

### Dapper.Query (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/core/Akka.Persistence.Query/Interfaces.cs` | 26 | `/// var events = journal.Query(new EventsByTag("mytag", 0L))` |

**Repos:** akka.net

## Api

### gRPC (62 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/benchmark/Akka.Benchmarks/Remoting/AkkaPduCodecBenchmark.cs` | 21 | `using Google.Protobuf;` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding.Tests/ClusterShardingMessageSerializerSpec.cs` | 23 | `using Google.Protobuf;` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Metrics/Serialization/ClusterMetricsMessageSerializer.cs` | 16 | `using Google.Protobuf;` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/Serialization/ReplicatorMessageSerializer.cs` | 14 | `using Google.Protobuf;` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/Serialization/ReplicatorMessageSerializer.cs` | 15 | `using Google.Protobuf.Collections;` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/Serialization/SerializationSupport.cs` | 17 | `using Google.Protobuf;` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/Serialization/ReplicatedDataSerializer.cs` | 11 | `using Google.Protobuf;` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/Internal/Internal.cs` | 16 | `using Google.Protobuf;` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/Replicator.cs` | 20 | `using Google.Protobuf;` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Metrics.Tests/Helpers/MetricsCollectorMock.cs` | 11 | `using Google.Protobuf.WellKnownTypes;` |
| akka.net | `src/contrib/cluster/Akka.DistributedData.Tests/Serialization/ReplicatorMessageSerializerSpec.cs` | 14 | `using Google.Protobuf;` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools/Client/Serialization/ClusterClientMessageSerializer.cs` | 14 | `using Google.Protobuf;` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools/Singleton/ClusterSingletonProxySettings.cs` | 12 | `using Google.Protobuf.WellKnownTypes;` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools/PublishSubscribe/Serialization/DistributedPubSubMessageSerializer.cs` | 18 | `using Google.Protobuf;` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/ClusterShardingMessageSerializer.cs` | 19 | `using Google.Protobuf;` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/ClusterShardingMessageSerializer.cs` | 20 | `using Google.Protobuf.WellKnownTypes;` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/Proto/ClusterShardingMessages.g.cs` | 15 | `using pb = global::Google.Protobuf;` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/Proto/ClusterShardingMessages.g.cs` | 16 | `using pbc = global::Google.Protobuf.Collections;` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/Proto/ClusterShardingMessages.g.cs` | 17 | `using pbr = global::Google.Protobuf.Reflection;` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/Proto/ClusterShardingMessages.g.cs` | 76 | `new pbr::FileDescriptor[] { global::Google.Protobuf.WellKnow` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/Proto/ClusterShardingMessages.g.cs` | 2821 | `private global::Google.Protobuf.WellKnownTypes.Duration time` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/Proto/ClusterShardingMessages.g.cs` | 2824 | `public global::Google.Protobuf.WellKnownTypes.Duration Timeo` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/Proto/ClusterShardingMessages.g.cs` | 2918 | `Timeout = new global::Google.Protobuf.WellKnownTypes.Duratio` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/Proto/ClusterShardingMessages.g.cs` | 2939 | `Timeout = new global::Google.Protobuf.WellKnownTypes.Duratio` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/Proto/ClusterShardingMessages.g.cs` | 2961 | `Timeout = new global::Google.Protobuf.WellKnownTypes.Duratio` |

*... and 37 more*

**Repos:** akka.net

### HttpClient.New (3 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools/Client/ClusterClientDiscovery.cs` | 102 | `_http = new HttpClient();` |
| akka.net | `src/examples/Stocks/SymbolLookup/Actors/DispatcherActor.cs` | 25 | `private IActorRef stock = Context.ActorOf(Props.Create(() =>` |
| akka.net | `src/core/Akka.Docs.Tests/Streams/RestartDocTests.cs` | 38 | `var httpClient = new HttpClient();` |

**Repos:** akka.net

### API.Controller (2 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/examples/AspNetCore/Akka.AspNetCore/Controllers/AkkaController.cs` | 18 | `public class AkkaController : ControllerBase` |
| akka.net | `src/core/Akka.Remote.TestKit.Tests/BarrierSpec.cs` | 346 | `//TODO: Controller tests.` |

**Repos:** akka.net

### API.HttpGet (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/examples/AspNetCore/Akka.AspNetCore/Controllers/AkkaController.cs` | 29 | `[HttpGet]` |

**Repos:** akka.net

### API.HttpPost (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/examples/AspNetCore/Akka.AspNetCore/Controllers/AkkaController.cs` | 36 | `[HttpPost]` |

**Repos:** akka.net

### API.Route (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/examples/AspNetCore/Akka.AspNetCore/Controllers/AkkaController.cs` | 16 | `[Route("api/[controller]")]` |

**Repos:** akka.net

### API.MapGet (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/examples/AspNetCore/Samples.Akka.AspNetCore/Startup.cs` | 54 | `endpoints.MapGet("/", async context =>` |

**Repos:** akka.net

### HttpClient.Injection (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/examples/WindowsService/AkkaWindowsService/Program.cs` | 21 | `services.AddHttpClient<JokeService>();` |

**Repos:** akka.net

### HttpClient.GetAsync (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/core/Akka.Docs.Tests/Streams/RestartDocTests.cs` | 50 | `httpClient.GetAsync("http://example.com/eventstream") // Mak` |

**Repos:** akka.net

## Connector

### IMessageAdapter (39 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/benchmark/Akka.Benchmarks/Logging/LoggingBenchmarks.cs` | 19 | `private sealed class BenchmarkLogAdapter : LoggingAdapterBas` |
| akka.net | `src/benchmark/Akka.Benchmarks/Logging/SemanticLoggingBenchmarks.cs` | 305 | `private sealed class BenchmarkLogAdapter : LoggingAdapterBas` |
| akka.net | `src/contrib/testkits/Akka.TestKit.Xunit2/Internals/AkkaAssertEqualityComparerAdapter.cs` | 21 | `internal class AkkaAssertEqualityComparerAdapter<T> : IEqual` |
| akka.net | `src/contrib/testkits/Akka.TestKit.Xunit/Internals/AkkaAssertEqualityComparerAdapter.cs` | 21 | `internal class AkkaAssertEqualityComparerAdapter<T> : IEqual` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding.Tests/WrappedShardBufferedMessageSpec.cs` | 36 | `private sealed class BufferMessageAdapter: IShardingBufferMe` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding.Tests/ShardingBufferAdapterSpec.cs` | 57 | `private class TestMessageAdapter: IShardingBufferMessageAdap` |
| akka.net | `src/contrib/cluster/Akka.DistributedData.Tests/WriteAggregatorSpec.cs` | 48 | `internal class WriteAckAdapter : ReceiveActor` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/OldCoordinatorStateMigrationEventAdapter.cs` | 18 | `internal sealed class OldCoordinatorStateMigrationEventAdapt` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/IShardingBufferMessageAdapter.cs` | 21 | `internal class EmptyBufferMessageAdapter: IShardingBufferMes` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/ClusterSharding.cs` | 55 | `internal sealed class ExtractorAdapter : IMessageExtractor` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/ClusterSharding.cs` | 1560 | `internal sealed class DeprecatedHandlerExtractorAdapter : IM` |
| akka.net | `src/core/Akka.Persistence.Tests/MemoryEventAdapterSpec.cs` | 160 | `public class UserAgeTaggingAdapter : IEventAdapter` |
| akka.net | `src/core/Akka.Persistence.Tests/MemoryEventAdapterSpec.cs` | 184 | `public class ReplayPassThroughAdapter : UserAgeTaggingAdapte` |
| akka.net | `src/core/Akka.Persistence.Tests/MemoryEventAdapterSpec.cs` | 193 | `public class LoggingAdapter : IEventAdapter` |
| akka.net | `src/core/Akka.Persistence.Tests/Journal/MemoryEventAdaptersSpec.cs` | 149 | `public abstract class BaseTestAdapter : IEventAdapter` |
| akka.net | `src/core/Akka.Persistence.Tests/Journal/MemoryEventAdaptersSpec.cs` | 167 | `public class ExampleEventAdapter : BaseTestAdapter { }` |
| akka.net | `src/core/Akka.Persistence.Tests/Journal/MemoryEventAdaptersSpec.cs` | 168 | `public class MarkerInterfaceAdapter : BaseTestAdapter { }` |
| akka.net | `src/core/Akka.Persistence.Tests/Journal/MemoryEventAdaptersSpec.cs` | 169 | `public class PreciseAdapter : BaseTestAdapter { }` |
| akka.net | `src/core/Akka.Persistence.Tests/Journal/MemoryEventAdaptersSpec.cs` | 195 | `public class ReaderAdapter : IReadEventAdapter` |
| akka.net | `src/core/Akka.Persistence.Tests/Journal/MemoryEventAdaptersSpec.cs` | 203 | `public class AnotherReaderAdapter : IReadEventAdapter` |
| akka.net | `src/core/Akka.Persistence.Tests/Journal/MemoryEventAdaptersSpec.cs` | 218 | `public class WriterAdapter : IWriteEventAdapter` |
| akka.net | `src/core/Akka.Persistence.Tests/EndToEndEventAdapterSpec.cs` | 101 | `public class AEndToEndAdapter : IEventAdapter` |
| akka.net | `src/core/Akka.Persistence.Tests/EndToEndEventAdapterSpec.cs` | 128 | `public class NewAEndToEndAdapter : IEventAdapter` |
| akka.net | `src/core/Akka.Persistence.Tests/EndToEndEventAdapterSpec.cs` | 155 | `public class BEndToEndAdapter : IEventAdapter` |
| akka.net | `src/core/Akka.Persistence.Tests/EndToEndEventAdapterSpec.cs` | 182 | `public class NewBEndToEndAdapter : IEventAdapter` |

*... and 14 more*

**Repos:** akka.net

## Config

### ConnectionString (33 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/benchmark/Akka.Cluster.Benchmarks/Sharding/ShardingInfrastructure.cs` | 214 | `var connectionString =` |
| akka.net | `src/benchmark/Akka.Cluster.Benchmarks/Sharding/ShardingInfrastructure.cs` | 225 | `connection-string = ""{connectionString}""` |
| akka.net | `src/benchmark/Akka.Cluster.Benchmarks/Sharding/ShardingInfrastructure.cs` | 232 | `connection-string = ""{connectionString}""` |
| akka.net | `src/examples/Akka.Persistence.Custom/Snapshot/SqliteSnapshotStore.cs` | 83 | `private readonly string _connectionString;` |
| akka.net | `src/examples/Akka.Persistence.Custom/Snapshot/SqliteSnapshotStore.cs` | 92 | `_connectionString = _settings.ConnectionString;` |
| akka.net | `src/examples/Akka.Persistence.Custom/Snapshot/SqliteSnapshotStore.cs` | 135 | `using (var connection = new SqliteConnection(_connectionStri` |
| akka.net | `src/examples/Akka.Persistence.Custom/Snapshot/SqliteSnapshotStore.cs` | 191 | `using (var connection = new SqliteConnection(_connectionStri` |
| akka.net | `src/examples/Akka.Persistence.Custom/Snapshot/SqliteSnapshotStore.cs` | 242 | `using (var connection = new SqliteConnection(_connectionStri` |
| akka.net | `src/examples/Akka.Persistence.Custom/Snapshot/SqliteSnapshotStore.cs` | 310 | `using (var connection = new SqliteConnection(_connectionStri` |
| akka.net | `src/examples/Akka.Persistence.Custom/Snapshot/SqliteSnapshotStore.cs` | 355 | `using (var connection = new SqliteConnection(_connectionStri` |
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 109 | `private readonly string _connectionString;` |
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 119 | `_connectionString = _settings.ConnectionString;` |
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 187 | `using (var connection = new SqliteConnection(_connectionStri` |
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 219 | `using (var connection = new SqliteConnection(_connectionStri` |
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 280 | `using (var connection = new SqliteConnection(_connectionStri` |
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 309 | `using (var connection = new SqliteConnection(_connectionStri` |
| akka.net | `src/examples/Akka.Persistence.Custom/Journal/SqliteJournal.cs` | 401 | `using (var connection = new SqliteConnection(_connectionStri` |
| akka.net | `src/examples/Akka.Persistence.Custom/Settings.cs` | 21 | `public string ConnectionString { get; }` |
| akka.net | `src/examples/Akka.Persistence.Custom/Settings.cs` | 45 | `ConnectionString = config.GetString("connection-string");` |
| akka.net | `src/examples/Akka.Persistence.Custom/Settings.cs` | 59 | `public string ConnectionString { get; }` |
| akka.net | `src/examples/Akka.Persistence.Custom/Settings.cs` | 89 | `ConnectionString = config.GetString("connection-string");` |
| akka.net | `src/examples/Akka.Persistence.Custom.Tests/SqliteSnapshotStoreSpec.cs` | 25 | `private static Config CreateSpecConfig(string connectionStri` |
| akka.net | `src/examples/Akka.Persistence.Custom.Tests/SqliteSnapshotStoreSpec.cs` | 36 | `connection-string = """ + connectionString + @"""` |
| akka.net | `src/examples/Akka.Persistence.Custom.Tests/SqliteSnapshotStoreSerializationSpec.cs` | 22 | `private static Config CreateSpecConfig(string connectionStri` |
| akka.net | `src/examples/Akka.Persistence.Custom.Tests/SqliteSnapshotStoreSerializationSpec.cs` | 33 | `connection-string = """ + connectionString + @"""` |

*... and 8 more*

**Repos:** akka.net

## Storage

### File.Read (14 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/examples/AspNetCore/Samples.Akka.AspNetCore/Actors/AkkaService.cs` | 41 | `var hocon = ConfigurationFactory.ParseString(await File.Read` |
| akka.net | `src/examples/Cluster/Metrics/Samples.Cluster.Metrics/Program.cs` | 23 | `var config = ConfigurationFactory.ParseString(await File.Rea` |
| akka.net | `src/examples/Cluster/Metrics/Samples.Cluster.AdaptiveGroup/Program.cs` | 25 | `var config = ConfigurationFactory.ParseString(await File.Rea` |
| akka.net | `src/examples/Cluster/ClusterSharding/ClusterSharding.Node/Program.cs` | 45 | `var config = ConfigurationFactory.ParseString(await File.Rea` |
| akka.net | `src/examples/Cluster/ClusterTools/ClusterToolsExample.Seed/Program.cs` | 25 | `var config = await File.ReadAllTextAsync("akka.conf");` |
| akka.net | `src/examples/Cluster/ClusterTools/ClusterToolsExample.Node/Program.cs` | 23 | `var config = await File.ReadAllTextAsync("akka.conf");` |
| akka.net | `src/core/Akka.Streams.Tests/Dsl/UnfoldResourceSourceSpec.cs` | 50 | `_open = () => new StreamReader(_manyLinesFile.OpenRead());` |
| akka.net | `src/core/Akka.API.Tests/LogFormatSpec.cs` | 105 | `var text = File.ReadAllText(filePath);` |
| akka.net | `src/core/Akka.API.Tests/LogFormatSpec.cs` | 158 | `var text = File.ReadAllText(filePath);` |
| akka.net | `src/core/Akka.API.Tests/LogFormatSpec.cs` | 199 | `var text = File.ReadAllText(filePath);` |
| akka.net | `src/core/Akka.Remote.Tests/Serialization/Bugfix7215Spec.cs` | 32 | `var bytes = File.ReadAllBytes($"./test-files/SerializedExcep` |
| akka.net | `src/core/Akka.Streams.Tests.Performance/IO/FileSourcesBenchmark.cs` | 40 | `_fileInputStreamSource = StreamConverters.FromInputStream(()` |
| akka.net | `src/core/Akka.Streams.Tests.Performance/IO/FileSourcesBenchmark.cs` | 41 | `_ioSourceLinesIterator = Source.FromEnumerator(() => File.Re` |
| akka.net | `src/core/Akka.Streams.Tests.Performance/IO/FileSourcesBenchmark.cs` | 101 | `[PerfBenchmark(Description = "Test the performance of a File` |

**Repos:** akka.net

### File.Write (7 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/benchmark/Akka.Cluster.Cpu.Benchmark/Program.cs` | 167 | `await File.WriteAllTextAsync($"CpuBenchmark_{now.ToFileTime(` |
| akka.net | `src/core/Akka.Streams.Tests/IO/FileSourceSpec.cs` | 352 | `File.WriteAllLines(_manyLinesPath.FullName, lines);` |
| akka.net | `src/core/Akka.Streams.Tests/IO/FileSourceSpec.cs` | 358 | `File.WriteAllText(_testFilePath.FullName, _testText);` |
| akka.net | `src/core/Akka.Streams.Tests/IO/FileSinkSpec.cs` | 456 | `targetFile.Create().Dispose();` |
| akka.net | `src/core/Akka.Remote.Tests/Transport/DotNettyCertificateValidationSpec.cs` | 67 | `File.WriteAllBytes(NoKeyCertPath, publicKeyBytes);` |
| akka.net | `src/core/Akka.Remote.Tests/Transport/DotNettyTlsHandshakeFailureSpec.cs` | 67 | `File.WriteAllBytes(NoKeyCertPath, publicKeyBytes);` |
| akka.net | `src/core/Akka.Streams.Tests.Performance/IO/FileSourcesBenchmark.cs` | 49 | `File.WriteAllLines(file.FullName, Enumerable.Repeat(line, 10` |

**Repos:** akka.net


---

*[Back to Index](../index.md)*
