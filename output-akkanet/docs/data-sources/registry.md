# Data Source Registry

## Summary

| Type | Occurrences |
|------|-------------|
| api | 128 |
| connector | 39 |
| config | 33 |
| database | 18 |
| messaging | 6 |
| storage | 1 |

## Connection Strings Found

| File | Repo | Connection Name | Value |
|------|------|----------------|-------|
| `src/examples/AppConfig/App.config` | akka.net | myConnectionString | `myDB://MyConnectionString` |

## Api

### gRPC (124 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/benchmark/Akka.Benchmarks/Remoting/AkkaPduCodecBenchmark.cs` | 57 | `private Akka.Remote.Serialization.Proto.Msg.Payload _payload` |
| akka.net | `src/benchmark/Akka.Cluster.Benchmarks/Serialization/DDataSerializationBenchmarks.cs` | 16 | `using Akka.Cluster.Sharding.Serialization.Proto.Msg;` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding.Tests/ClusterShardingMessageSerializerSpec.cs` | 132 | `var message1 = new Serialization.Proto.Msg.EntityStarted();` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding.Tests/ClusterShardingMessageSerializerSpec.cs` | 143 | `var message2 = new Serialization.Proto.Msg.EntityStopped();` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Metrics/Serialization/ClusterMetricsMessageSerializer.cs` | 381 | `private IMetricsSelector MetricSelectorFromProto(Serializati` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/Serialization/ReplicatorMessageSerializer.cs` | 16 | `using Akka.DistributedData.Serialization.Proto.Msg;` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/Serialization/SerializationSupport.cs` | 15 | `using Akka.DistributedData.Serialization.Proto.Msg;` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/Serialization/ReplicatedDataSerializer.cs` | 18 | `using Akka.DistributedData.Serialization.Proto.Msg;` |
| akka.net | `src/contrib/cluster/Akka.DistributedData/Serialization/OtherMessageComparer.cs` | 11 | `using Akka.DistributedData.Serialization.Proto.Msg;` |
| akka.net | `src/contrib/cluster/Akka.DistributedData.Tests/Serialization/ReplicatedDataSerializerBackCompatSpec.cs` | 11 | `using Akka.DistributedData.Serialization.Proto.Msg;` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools/Client/Serialization/ClusterClientMessageSerializer.cs` | 164 | `var protoMessage = new PublishSubscribe.Serialization.Proto.` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools/Client/Serialization/ClusterClientMessageSerializer.cs` | 173 | `var sendProto = PublishSubscribe.Serialization.Proto.Msg.Sen` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools/Client/Serialization/ClusterClientMessageSerializer.cs` | 179 | `var protoMessage = new PublishSubscribe.Serialization.Proto.` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools/Client/Serialization/ClusterClientMessageSerializer.cs` | 188 | `var sendToAllProto = PublishSubscribe.Serialization.Proto.Ms` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools/Client/Serialization/ClusterClientMessageSerializer.cs` | 194 | `var protoMessage = new PublishSubscribe.Serialization.Proto.` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools/Client/Serialization/ClusterClientMessageSerializer.cs` | 202 | `var publishProto = PublishSubscribe.Serialization.Proto.Msg.` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools/PublishSubscribe/Serialization/DistributedPubSubMessageSerializer.cs` | 19 | `using AddressData = Akka.Remote.Serialization.Proto.Msg.Addr` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/ClusterShardingMessageSerializer.cs` | 15 | `using Akka.Cluster.Sharding.Serialization.Proto.Msg;` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/ClusterShardingMessageSerializer.cs` | 17 | `using Akka.Remote.Serialization.Proto.Msg;` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/ClusterShardingMessageSerializer.cs` | 21 | `using ActorRefMessage = Akka.Remote.Serialization.Proto.Msg.` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/Proto/ClusterShardingMessages.g.cs` | 19 | `namespace Akka.Cluster.Sharding.Serialization.Proto.Msg {` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/Proto/ClusterShardingMessages.g.cs` | 76 | `new pbr::FileDescriptor[] { global::Google.Protobuf.WellKnow` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/Proto/ClusterShardingMessages.g.cs` | 78 | `new pbr::GeneratedClrTypeInfo(typeof(global::Akka.Cluster.Sh` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/Proto/ClusterShardingMessages.g.cs` | 79 | `new pbr::GeneratedClrTypeInfo(typeof(global::Akka.Cluster.Sh` |
| akka.net | `src/contrib/cluster/Akka.Cluster.Sharding/Serialization/Proto/ClusterShardingMessages.g.cs` | 80 | `new pbr::GeneratedClrTypeInfo(typeof(global::Akka.Cluster.Sh` |

*... and 99 more*

**Repos:** akka.net

### HttpClient.New (3 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/contrib/cluster/Akka.Cluster.Tools/Client/ClusterClientDiscovery.cs` | 102 | `_http = new HttpClient();` |
| akka.net | `src/examples/Stocks/SymbolLookup/Actors/DispatcherActor.cs` | 25 | `private IActorRef stock = Context.ActorOf(Props.Create(() =>` |
| akka.net | `src/core/Akka.Docs.Tests/Streams/RestartDocTests.cs` | 38 | `var httpClient = new HttpClient();` |

**Repos:** akka.net

### HttpClient.Injection (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/examples/WindowsService/AkkaWindowsService/Program.cs` | 21 | `services.AddHttpClient<JokeService>();` |

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

## Database

### Dapper (18 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
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
| akka.net | `src/core/Akka.Persistence.Query/Interfaces.cs` | 26 | `/// var events = journal.Query(new EventsByTag("mytag", 0L))` |
| akka.net | `src/core/Akka.Streams/Implementation/Fusing/ActorGraphInterpreter.cs` | 354 | `Interpreter.Execute(_abortLimit);` |
| akka.net | `src/core/Akka.Streams/Implementation/Fusing/ActorGraphInterpreter.cs` | 375 | `var remainingQuota = _interpreter.Execute(Math.Min(actorEven` |
| akka.net | `src/core/Akka/Actor/Scheduler/HashedWheelTimerScheduler.cs` | 205 | `bucket.Execute(deadline);` |
| akka.net | `src/core/Akka/Actor/Scheduler/HashedWheelTimerScheduler.cs` | 300 | `bucket.Execute(deadline);` |
| akka.net | `src/core/Akka/Dispatch/Dispatcher.cs` | 76 | `Executor.Execute(run);` |
| akka.net | `src/core/Akka/Dispatch/Dispatcher.cs` | 82 | `Executor.Execute(run);` |
| akka.net | `src/core/Akka.Streams.Tests.Performance/InterpreterBenchmark.cs` | 69 | `setup.Interpreter.Execute(int.MaxValue);` |

**Repos:** akka.net

## Messaging

### Kafka (5 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/core/Akka/Delivery/ProducerController.cs` | 164 | `public interface IProducerCommand<T>` |
| akka.net | `src/core/Akka/Delivery/ProducerController.cs` | 171 | `public sealed class Start<T> : IProducerCommand<T>` |
| akka.net | `src/core/Akka/Delivery/ProducerController.cs` | 184 | `public sealed class RequestNext<T> : IProducerCommand<T>, IN` |
| akka.net | `src/core/Akka/Delivery/ProducerController.cs` | 257 | `public sealed class MessageWithConfirmation<T> : IProducerCo` |
| akka.net | `src/core/Akka/Delivery/ProducerController.cs` | 281 | `public sealed record RegisterConsumer<T>(IActorRef ConsumerC` |

**Repos:** akka.net

### RabbitMQ (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/examples/HeadlessService/AkkaHeadlesssService/HeadlessActor.cs` | 17 | `// Connect to an Apache Kafka, Apache Pulsar, RabbitMQ insta` |

**Repos:** akka.net

## Storage

### FileStorage (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| akka.net | `src/core/Akka.Streams.Tests/IO/FileSinkSpec.cs` | 456 | `targetFile.Create().Dispose();` |

**Repos:** akka.net


---

*[Back to Index](../index.md)*
