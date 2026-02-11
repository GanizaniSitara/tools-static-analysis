# Dependency Visualizations

## landscape

```mermaid
graph LR
    subgraph Applications
        akka_net_SerializationBenchmarks["SerializationBenchmarks"]
        akka_net_Akka_Benchmarks["Akka.Benchmarks"]
        akka_net_Akka_Cluster_Benchmarks["Akka.Cluster.Benchmarks"]
        akka_net_RemotePingPong["RemotePingPong"]
        akka_net_Akka_Cluster_Cpu_Benchmark["Akka.Cluster.Cpu.Benchmark"]
        akka_net_PingPong["PingPong"]
        akka_net_SpawnBenchmark["SpawnBenchmark"]
        akka_net_TimeServer["TimeServer"]
        akka_net_System1["System1"]
        akka_net_System2["System2"]
        akka_net_Shared["Shared"]
        akka_net_ClusterSharding_Node["ClusterSharding.Node"]
        akka_net_ShoppingCart["ShoppingCart"]
        akka_net_HelloAkka["HelloAkka"]
        akka_net_Routing["Routing"]
        akka_net_HelloWorld["HelloWorld"]
        akka_net_ChatServer["ChatServer"]
        akka_net_AppConfig["AppConfig"]
        akka_net_FaultTolerance["FaultTolerance"]
    end
    subgraph Tests
        akka_net_Akka_DependencyInjection_Tests["Akka.DependencyInjection.Tests"]
        akka_net_Akka_TestKit_Xunit_Tests["Akka.TestKit.Xunit.Tests"]
        akka_net_Akka_TestKit_Xunit2["Akka.TestKit.Xunit2"]
        akka_net_Akka_TestKit_Xunit2_Tests["Akka.TestKit.Xunit2.Tests"]
        akka_net_Akka_TestKit_Xunit["Akka.TestKit.Xunit"]
        akka_net_Akka_Cluster_Tools_Tests_MultiNode["Akka.Cluster.Tools.Tests.MultiNode"]
        akka_net_Akka_Cluster_Sharding_Tests["Akka.Cluster.Sharding.Tests"]
        akka_net_Akka_DistributedData_Tests_MultiNode["Akka.DistributedData.Tests.MultiNode"]
        akka_net_Akka_Cluster_Metrics_Tests["Akka.Cluster.Metrics.Tests"]
        akka_net_Akka_Cluster_Tools_Tests["Akka.Cluster.Tools.Tests"]
        akka_net_Akka_Cluster_Sharding_Tests_MultiNode["Akka.Cluster.Sharding.Tests.MultiNode"]
        akka_net_Akka_DistributedData_Tests["Akka.DistributedData.Tests"]
        akka_net_Akka_Cluster_Metrics_Tests_MultiNode["Akka.Cluster.Metrics.Tests.MultiNode"]
        akka_net_Akka_Persistence_Query_InMemory_Tests["Akka.Persistence.Query.InMemory.Tests"]
        akka_net_Akka_Serialization_TestKit["Akka.Serialization.TestKit"]
        akka_net_Akka_Serialization_Hyperion_Tests["Akka.Serialization.Hyperion.Tests"]
        akka_net_Akka_Persistence_Custom_Tests["Akka.Persistence.Custom.Tests"]
        akka_net_DDataStressTest["DDataStressTest"]
        akka_net_Akka_Persistence_Tests["Akka.Persistence.Tests"]
        akka_net_Akka_Tests_Performance["Akka.Tests.Performance"]
        akka_net_Akka_Docs_Tests["Akka.Docs.Tests"]
        akka_net_Akka_Remote_Tests_MultiNode["Akka.Remote.Tests.MultiNode"]
        akka_net_Akka_Remote_TestKit["Akka.Remote.TestKit"]
        akka_net_Akka_Cluster_Tests_MultiNode["Akka.Cluster.Tests.MultiNode"]
        akka_net_Akka_Streams_Tests["Akka.Streams.Tests"]
        akka_net_Akka_Cluster_TestKit["Akka.Cluster.TestKit"]
        akka_net_Akka_Streams_TestKit["Akka.Streams.TestKit"]
        akka_net_Akka_Remote_Tests_Performance["Akka.Remote.Tests.Performance"]
        akka_net_Akka_TestKit_Tests["Akka.TestKit.Tests"]
        akka_net_Akka_Streams_Tests_TCK["Akka.Streams.Tests.TCK"]
        akka_net_Akka_Discovery_Tests["Akka.Discovery.Tests"]
        akka_net_Akka_Coordination_Tests["Akka.Coordination.Tests"]
        akka_net_Akka_Persistence_Query_Tests["Akka.Persistence.Query.Tests"]
        akka_net_Akka_Persistence_TCK_Tests["Akka.Persistence.TCK.Tests"]
        akka_net_Akka_API_Tests["Akka.API.Tests"]
        akka_net_Akka_Persistence_TestKit_Tests["Akka.Persistence.TestKit.Tests"]
        akka_net_Akka_Persistence_TestKit_Xunit2["Akka.Persistence.TestKit.Xunit2"]
        akka_net_Akka_Cluster_Tests_Performance["Akka.Cluster.Tests.Performance"]
        akka_net_Akka_Remote_Tests["Akka.Remote.Tests"]
        akka_net_Akka_Persistence_TestKit["Akka.Persistence.TestKit"]
        akka_net_Akka_Streams_TestKit_Tests["Akka.Streams.TestKit.Tests"]
        akka_net_Akka_Tests["Akka.Tests"]
        akka_net_Akka_Cluster_Tests["Akka.Cluster.Tests"]
        akka_net_Akka_TestKit["Akka.TestKit"]
        akka_net_Akka_Docs_Tutorials["Akka.Docs.Tutorials"]
        akka_net_Akka_Streams_Tests_Performance["Akka.Streams.Tests.Performance"]
        akka_net_Akka_Remote_TestKit_Tests["Akka.Remote.TestKit.Tests"]
        akka_net_Akka_Tests_Shared_Internals["Akka.Tests.Shared.Internals"]
    end
    subgraph Librarys
        akka_net_Akka_DependencyInjection["Akka.DependencyInjection"]
        akka_net_Akka_DistributedData_LightningDB["Akka.DistributedData.LightningDB"]
        akka_net_Akka_Cluster_Metrics["Akka.Cluster.Metrics"]
        akka_net_Akka_DistributedData["Akka.DistributedData"]
        akka_net_Akka_Cluster_Sharding["Akka.Cluster.Sharding"]
        akka_net_Akka_Persistence_Query_InMemory["Akka.Persistence.Query.InMemory"]
        akka_net_Akka_Serialization_Hyperion["Akka.Serialization.Hyperion"]
        akka_net_Akka_Persistence_Custom["Akka.Persistence.Custom"]
        akka_net_ChatMessages["ChatMessages"]
        akka_net_Akka_Discovery["Akka.Discovery"]
        akka_net_Akka_Cluster["Akka.Cluster"]
        akka_net_Akka_Persistence_Query["Akka.Persistence.Query"]
        akka_net_Akka_Persistence_TCK["Akka.Persistence.TCK"]
        akka_net_Akka_Persistence["Akka.Persistence"]
        akka_net_Akka_Streams["Akka.Streams"]
        akka_net_Akka_Coordination["Akka.Coordination"]
        akka_net_Akka_Remote["Akka.Remote"]
        akka_net_Akka["Akka"]
    end
    subgraph Tools
        akka_net_Akka_Cluster_Tools["Akka.Cluster.Tools"]
        akka_net_TimeClient["TimeClient"]
        akka_net_ChatClient["ChatClient"]
    end
    subgraph Webapps
        akka_net_Akka_AspNetCore["Akka.AspNetCore"]
    end
    subgraph Services
        akka_net_TcpEchoService_Server["TcpEchoService.Server"]
        akka_net_AkkaWindowsService["AkkaWindowsService"]
        akka_net_AkkaHeadlesssService["AkkaHeadlesssService"]
    end
    subgraph Desktopapps
        akka_net_SymbolLookup["SymbolLookup"]
    end
    akka_net_SerializationBenchmarks --> akka_net_Akka_Serialization_Hyperion
    akka_net_SerializationBenchmarks --> akka_net_Akka
    akka_net_Akka_Benchmarks --> akka_net_Akka_DistributedData
    akka_net_Akka_Benchmarks --> akka_net_Akka_Serialization_Hyperion
    akka_net_Akka_Benchmarks --> akka_net_Akka_Cluster
    akka_net_Akka_Benchmarks --> akka_net_Akka_Persistence
    akka_net_Akka_Benchmarks --> akka_net_Akka_Remote
    akka_net_Akka_Benchmarks --> akka_net_Akka_Streams
    akka_net_Akka_Benchmarks --> akka_net_Akka
    akka_net_Akka_Cluster_Benchmarks --> akka_net_Akka_Cluster_Sharding
    akka_net_RemotePingPong --> akka_net_Akka_Remote
    akka_net_Akka_Cluster_Cpu_Benchmark --> akka_net_Akka_Cluster
    akka_net_PingPong --> akka_net_Akka
    akka_net_SpawnBenchmark --> akka_net_Akka
    akka_net_Akka_DependencyInjection_Tests --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_DependencyInjection_Tests --> akka_net_Akka_DependencyInjection
    akka_net_Akka_DependencyInjection --> akka_net_Akka
    akka_net_Akka_TestKit_Xunit_Tests --> akka_net_Akka_TestKit_Xunit
    akka_net_Akka_TestKit_Xunit2 --> akka_net_Akka_TestKit
    akka_net_Akka_TestKit_Xunit2_Tests --> akka_net_Akka_TestKit_Xunit2
    akka_net_Akka_TestKit_Xunit --> akka_net_Akka_TestKit
    akka_net_Akka_Cluster_Tools_Tests_MultiNode --> akka_net_Akka_Coordination_Tests
    akka_net_Akka_Cluster_Tools_Tests_MultiNode --> akka_net_Akka_Cluster_Tools
    akka_net_Akka_Cluster_Tools_Tests_MultiNode --> akka_net_Akka_Cluster_TestKit
    akka_net_Akka_Cluster_Tools_Tests_MultiNode --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Cluster_Sharding_Tests --> akka_net_Akka_Coordination_Tests
    akka_net_Akka_Cluster_Sharding_Tests --> akka_net_Akka_Cluster_Sharding
    akka_net_Akka_Cluster_Sharding_Tests --> akka_net_Akka_Persistence
    akka_net_Akka_Cluster_Sharding_Tests --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_DistributedData_LightningDB --> akka_net_Akka_DistributedData
    akka_net_Akka_Cluster_Metrics --> akka_net_Akka_Cluster
    akka_net_Akka_DistributedData_Tests_MultiNode --> akka_net_Akka_DistributedData_LightningDB
    akka_net_Akka_DistributedData_Tests_MultiNode --> akka_net_Akka_DistributedData
    akka_net_Akka_DistributedData_Tests_MultiNode --> akka_net_Akka_Cluster_TestKit
    akka_net_Akka_DistributedData_Tests_MultiNode --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_DistributedData --> akka_net_Akka_Cluster
    akka_net_Akka_Cluster_Metrics_Tests --> akka_net_Akka_Cluster_Metrics
    akka_net_Akka_Cluster_Metrics_Tests --> akka_net_Akka_Cluster_Tests
    akka_net_Akka_Cluster_Tools_Tests --> akka_net_Akka_Coordination_Tests
    akka_net_Akka_Cluster_Tools_Tests --> akka_net_Akka_Cluster_Tools
    akka_net_Akka_Cluster_Tools_Tests --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Cluster_Sharding_Tests_MultiNode --> akka_net_Akka_Serialization_Hyperion
    akka_net_Akka_Cluster_Sharding_Tests_MultiNode --> akka_net_Akka_Cluster_Sharding
    akka_net_Akka_Cluster_Sharding_Tests_MultiNode --> akka_net_Akka_Cluster_TestKit
    akka_net_Akka_Cluster_Sharding_Tests_MultiNode --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Cluster_Sharding_Tests_MultiNode --> akka_net_Akka_DistributedData_LightningDB
    akka_net_Akka_DistributedData_Tests --> akka_net_Akka_Cluster_Sharding
    akka_net_Akka_DistributedData_Tests --> akka_net_Akka_DistributedData_LightningDB
    akka_net_Akka_DistributedData_Tests --> akka_net_Akka_DistributedData
    akka_net_Akka_DistributedData_Tests --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Cluster_Metrics_Tests_MultiNode --> akka_net_Akka_Cluster_Metrics_Tests
    akka_net_Akka_Cluster_Metrics_Tests_MultiNode --> akka_net_Akka_Cluster_Metrics
    akka_net_Akka_Cluster_Metrics_Tests_MultiNode --> akka_net_Akka_Cluster_TestKit
    akka_net_Akka_Cluster_Tools --> akka_net_Akka_Cluster
    akka_net_Akka_Cluster_Tools --> akka_net_Akka_Coordination
    akka_net_Akka_Cluster_Tools --> akka_net_Akka_Discovery
    akka_net_Akka_Cluster_Sharding --> akka_net_Akka_Coordination
    akka_net_Akka_Cluster_Sharding --> akka_net_Akka_Persistence
    akka_net_Akka_Cluster_Sharding --> akka_net_Akka_Cluster_Tools
    akka_net_Akka_Cluster_Sharding --> akka_net_Akka_DistributedData_LightningDB
    akka_net_Akka_Cluster_Sharding --> akka_net_Akka_DistributedData
    akka_net_Akka_Persistence_Query_InMemory --> akka_net_Akka_Persistence_Query
    akka_net_Akka_Persistence_Query_InMemory_Tests --> akka_net_Akka_Persistence_TCK
    akka_net_Akka_Persistence_Query_InMemory_Tests --> akka_net_Akka_Persistence_Query_InMemory
    akka_net_Akka_Serialization_TestKit --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Serialization_Hyperion --> akka_net_Akka
    akka_net_Akka_Serialization_Hyperion_Tests --> akka_net_Akka_Serialization_Hyperion
    akka_net_Akka_Serialization_Hyperion_Tests --> akka_net_Akka_Serialization_TestKit
    akka_net_Akka_Serialization_Hyperion_Tests --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_AspNetCore --> akka_net_Akka_DependencyInjection
    akka_net_Akka_AspNetCore --> akka_net_Akka
    akka_net_TimeClient --> akka_net_Akka_Remote
    akka_net_TimeClient --> akka_net_Akka
    akka_net_TimeServer --> akka_net_Akka_Remote
    akka_net_TimeServer --> akka_net_Akka
    akka_net_Akka_Persistence_Custom --> akka_net_Akka_Persistence
    akka_net_System1 --> akka_net_Akka_Remote
    akka_net_System1 --> akka_net_Akka
    akka_net_System1 --> akka_net_Shared
    akka_net_System2 --> akka_net_Akka_Remote
    akka_net_System2 --> akka_net_Akka
    akka_net_System2 --> akka_net_Shared
    akka_net_Shared --> akka_net_Akka
    akka_net_Akka_Persistence_Custom_Tests --> akka_net_Akka_Persistence_TCK
    akka_net_Akka_Persistence_Custom_Tests --> akka_net_Akka_Persistence_Custom
    akka_net_ClusterSharding_Node --> akka_net_Akka_Cluster_Sharding
    akka_net_ClusterSharding_Node --> akka_net_Akka_Serialization_Hyperion
    akka_net_ShoppingCart --> akka_net_Akka_Cluster_Sharding
    akka_net_DDataStressTest --> akka_net_Akka_DistributedData
    akka_net_TcpEchoService_Server --> akka_net_Akka
    akka_net_HelloAkka --> akka_net_Akka
    akka_net_Routing --> akka_net_Akka
    akka_net_AkkaWindowsService --> akka_net_Akka_DependencyInjection
    akka_net_AkkaWindowsService --> akka_net_Akka
    akka_net_HelloWorld --> akka_net_Akka
    akka_net_AkkaHeadlesssService --> akka_net_Akka_DependencyInjection
    akka_net_AkkaHeadlesssService --> akka_net_Akka
    akka_net_SymbolLookup --> akka_net_Akka
    akka_net_ChatClient --> akka_net_Akka_Remote
    akka_net_ChatClient --> akka_net_ChatMessages
    akka_net_ChatServer --> akka_net_Akka_Remote
    akka_net_ChatServer --> akka_net_ChatMessages
    akka_net_ChatMessages --> akka_net_Akka
    akka_net_FaultTolerance --> akka_net_Akka
    akka_net_Akka_Persistence_Tests --> akka_net_Akka_Serialization_Hyperion
    akka_net_Akka_Persistence_Tests --> akka_net_Akka_Persistence_TestKit_Xunit2
    akka_net_Akka_Persistence_Tests --> akka_net_Akka_Persistence
    akka_net_Akka_Persistence_Tests --> akka_net_Akka_Remote
    akka_net_Akka_Persistence_Tests --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Tests_Performance --> akka_net_Akka
    akka_net_Akka_Tests_Performance --> akka_net_Akka_TestKit
    akka_net_Akka_Docs_Tests --> akka_net_Akka_Cluster_Metrics
    akka_net_Akka_Docs_Tests --> akka_net_Akka_Coordination_Tests
    akka_net_Akka_Docs_Tests --> akka_net_Akka
    akka_net_Akka_Docs_Tests --> akka_net_Akka_Persistence
    akka_net_Akka_Docs_Tests --> akka_net_Akka_Streams
    akka_net_Akka_Docs_Tests --> akka_net_Akka_TestKit
    akka_net_Akka_Docs_Tests --> akka_net_Akka_Cluster_Tools
    akka_net_Akka_Docs_Tests --> akka_net_Akka_TestKit_Xunit2
    akka_net_Akka_Remote_Tests_MultiNode --> akka_net_Akka_Remote_TestKit
    akka_net_Akka_Remote_Tests_MultiNode --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Remote_TestKit --> akka_net_Akka_Remote
    akka_net_Akka_Remote_TestKit --> akka_net_Akka_TestKit_Xunit2
    akka_net_Akka_Cluster_Tests_MultiNode --> akka_net_Akka_Cluster_TestKit
    akka_net_Akka_Cluster_Tests_MultiNode --> akka_net_Akka_Coordination_Tests
    akka_net_Akka_Cluster_Tests_MultiNode --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Discovery --> akka_net_Akka
    akka_net_Akka_Streams_Tests --> akka_net_Akka_Remote
    akka_net_Akka_Streams_Tests --> akka_net_Akka_Streams
    akka_net_Akka_Streams_Tests --> akka_net_Akka_Streams_TestKit
    akka_net_Akka_Streams_Tests --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Cluster_TestKit --> akka_net_Akka_Remote_TestKit
    akka_net_Akka_Cluster_TestKit --> akka_net_Akka_Cluster
    akka_net_Akka_Streams_TestKit --> akka_net_Akka_Streams
    akka_net_Akka_Streams_TestKit --> akka_net_Akka_TestKit
    akka_net_Akka_Remote_Tests_Performance --> akka_net_Akka_Remote
    akka_net_Akka_Cluster --> akka_net_Akka_Coordination
    akka_net_Akka_Cluster --> akka_net_Akka_Remote
    akka_net_Akka_TestKit_Tests --> akka_net_Akka
    akka_net_Akka_TestKit_Tests --> akka_net_Akka_TestKit
    akka_net_Akka_TestKit_Tests --> akka_net_Akka_TestKit_Xunit2
    akka_net_Akka_TestKit_Tests --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Streams_Tests_TCK --> akka_net_Akka
    akka_net_Akka_Streams_Tests_TCK --> akka_net_Akka_Streams
    akka_net_Akka_Streams_Tests_TCK --> akka_net_Akka_Streams_TestKit
    akka_net_Akka_Streams_Tests_TCK --> akka_net_Akka_TestKit
    akka_net_Akka_Streams_Tests_TCK --> akka_net_Akka_TestKit_Xunit2
    akka_net_Akka_Streams_Tests_TCK --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Discovery_Tests --> akka_net_Akka_TestKit_Xunit2
    akka_net_Akka_Discovery_Tests --> akka_net_Akka_Discovery
    akka_net_Akka_Coordination_Tests --> akka_net_Akka_Coordination
    akka_net_Akka_Coordination_Tests --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Persistence_Query_Tests --> akka_net_Akka_Persistence_Query
    akka_net_Akka_Persistence_Query_Tests --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Persistence_TCK_Tests --> akka_net_Akka_Persistence_TCK
    akka_net_Akka_API_Tests --> akka_net_Akka_Cluster_Metrics
    akka_net_Akka_API_Tests --> akka_net_Akka_Cluster_Sharding
    akka_net_Akka_API_Tests --> akka_net_Akka_DistributedData
    akka_net_Akka_API_Tests --> akka_net_Akka_Persistence_Query_InMemory
    akka_net_Akka_API_Tests --> akka_net_Akka_TestKit_Xunit2
    akka_net_Akka_API_Tests --> akka_net_Akka_Coordination
    akka_net_Akka_API_Tests --> akka_net_Akka_Discovery
    akka_net_Akka_API_Tests --> akka_net_Akka_Persistence_Query
    akka_net_Akka_API_Tests --> akka_net_Akka_TestKit
    akka_net_Akka_API_Tests --> akka_net_Akka
    akka_net_Akka_API_Tests --> akka_net_Akka_Cluster
    akka_net_Akka_API_Tests --> akka_net_Akka_Cluster_Tools
    akka_net_Akka_API_Tests --> akka_net_Akka_Persistence
    akka_net_Akka_API_Tests --> akka_net_Akka_Remote
    akka_net_Akka_API_Tests --> akka_net_Akka_Streams
    akka_net_Akka_Persistence_TestKit_Tests --> akka_net_Akka_Persistence_TestKit
    akka_net_Akka_Persistence_TestKit_Tests --> akka_net_Akka_Persistence_TestKit_Xunit2
    akka_net_Akka_Persistence_TestKit_Tests --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Persistence_TestKit_Xunit2 --> akka_net_Akka_TestKit_Xunit2
    akka_net_Akka_Persistence_TestKit_Xunit2 --> akka_net_Akka_Persistence_TestKit
    akka_net_Akka_Persistence_TestKit_Xunit2 --> akka_net_Akka_TestKit
    akka_net_Akka_Cluster_Tests_Performance --> akka_net_Akka_Cluster
    akka_net_Akka_Remote_Tests --> akka_net_Akka_Serialization_Hyperion
    akka_net_Akka_Remote_Tests --> akka_net_Akka_Remote
    akka_net_Akka_Remote_Tests --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Persistence_Query --> akka_net_Akka_Persistence
    akka_net_Akka_Persistence_Query --> akka_net_Akka_Streams
    akka_net_Akka_Persistence_TCK --> akka_net_Akka_Persistence_Query
    akka_net_Akka_Persistence_TCK --> akka_net_Akka_Persistence
    akka_net_Akka_Persistence_TCK --> akka_net_Akka_TestKit_Xunit2
    akka_net_Akka_Persistence_TCK --> akka_net_Akka_Streams_TestKit
    akka_net_Akka_Persistence --> akka_net_Akka
    akka_net_Akka_Persistence_TestKit --> akka_net_Akka_TestKit_Xunit2
    akka_net_Akka_Persistence_TestKit --> akka_net_Akka_Persistence
    akka_net_Akka_Persistence_TestKit --> akka_net_Akka_TestKit
    akka_net_Akka_Streams --> akka_net_Akka
    akka_net_Akka_Coordination --> akka_net_Akka
    akka_net_Akka_Remote --> akka_net_Akka
    akka_net_Akka_Streams_TestKit_Tests --> akka_net_Akka_Streams_TestKit
    akka_net_Akka_Streams_TestKit_Tests --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Tests --> akka_net_Akka
    akka_net_Akka_Tests --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Cluster_Tests --> akka_net_Akka_Cluster
    akka_net_Akka_Cluster_Tests --> akka_net_Akka_Coordination_Tests
    akka_net_Akka_Cluster_Tests --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_TestKit --> akka_net_Akka
    akka_net_Akka_Docs_Tutorials --> akka_net_Akka
    akka_net_Akka_Docs_Tutorials --> akka_net_Akka_Persistence
    akka_net_Akka_Docs_Tutorials --> akka_net_Akka_Streams
    akka_net_Akka_Docs_Tutorials --> akka_net_Akka_TestKit
    akka_net_Akka_Docs_Tutorials --> akka_net_Akka_Cluster_Tools
    akka_net_Akka_Docs_Tutorials --> akka_net_Akka_TestKit_Xunit2
    akka_net_Akka_Streams_Tests_Performance --> akka_net_Akka_Streams
    akka_net_Akka_Streams_Tests_Performance --> akka_net_Akka_Streams_Tests
    akka_net_Akka_Streams_Tests_Performance --> akka_net_Akka_Streams_TestKit
    akka_net_Akka_Remote_TestKit_Tests --> akka_net_Akka_Remote_TestKit
    akka_net_Akka_Remote_TestKit_Tests --> akka_net_Akka_Tests_Shared_Internals
    akka_net_Akka_Tests_Shared_Internals --> akka_net_Akka_TestKit_Xunit2
```

## core libraries

```mermaid
graph TD
    akka_net_Akka_DependencyInjection["Akka.DependencyInjection"]
    akka_net_Akka_DistributedData_LightningDB["Akka.DistributedData.LightningDB"]
    akka_net_Akka_Cluster_Metrics["Akka.Cluster.Metrics"]
    akka_net_Akka_DistributedData["Akka.DistributedData"]
    akka_net_Akka_Cluster_Sharding["Akka.Cluster.Sharding"]
    akka_net_Akka_Persistence_Query_InMemory["Akka.Persistence.Query.InMemory"]
    akka_net_Akka_Serialization_Hyperion["Akka.Serialization.Hyperion"]
    akka_net_Akka_Persistence_Custom["Akka.Persistence.Custom"]
    akka_net_ChatMessages["ChatMessages"]
    akka_net_Akka_Discovery["Akka.Discovery"]
    akka_net_Akka_Cluster["Akka.Cluster"]
    akka_net_Akka_Persistence_Query["Akka.Persistence.Query"]
    akka_net_Akka_Persistence_TCK["Akka.Persistence.TCK"]
    akka_net_Akka_Persistence["Akka.Persistence"]
    akka_net_Akka_Streams["Akka.Streams"]
    akka_net_Akka_Coordination["Akka.Coordination"]
    akka_net_Akka_Remote["Akka.Remote"]
    akka_net_Akka["Akka"]
    akka_net_Akka_DependencyInjection --> akka_net_Akka
    akka_net_Akka_DistributedData_LightningDB --> akka_net_Akka_DistributedData
    akka_net_Akka_Cluster_Metrics --> akka_net_Akka_Cluster
    akka_net_Akka_DistributedData --> akka_net_Akka_Cluster
    akka_net_Akka_Cluster_Sharding --> akka_net_Akka_Coordination
    akka_net_Akka_Cluster_Sharding --> akka_net_Akka_Persistence
    akka_net_Akka_Cluster_Sharding --> akka_net_Akka_DistributedData_LightningDB
    akka_net_Akka_Cluster_Sharding --> akka_net_Akka_DistributedData
    akka_net_Akka_Persistence_Query_InMemory --> akka_net_Akka_Persistence_Query
    akka_net_Akka_Serialization_Hyperion --> akka_net_Akka
    akka_net_Akka_Persistence_Custom --> akka_net_Akka_Persistence
    akka_net_ChatMessages --> akka_net_Akka
    akka_net_Akka_Discovery --> akka_net_Akka
    akka_net_Akka_Cluster --> akka_net_Akka_Coordination
    akka_net_Akka_Cluster --> akka_net_Akka_Remote
    akka_net_Akka_Persistence_Query --> akka_net_Akka_Persistence
    akka_net_Akka_Persistence_Query --> akka_net_Akka_Streams
    akka_net_Akka_Persistence_TCK --> akka_net_Akka_Persistence_Query
    akka_net_Akka_Persistence_TCK --> akka_net_Akka_Persistence
    akka_net_Akka_Persistence --> akka_net_Akka
    akka_net_Akka_Streams --> akka_net_Akka
    akka_net_Akka_Coordination --> akka_net_Akka
    akka_net_Akka_Remote --> akka_net_Akka
```

## data infrastructure

```mermaid
graph LR
    subgraph Applications
        akka_net_SerializationBenchmarks["SerializationBenchmarks"]
        akka_net_Akka_Benchmarks["Akka.Benchmarks"]
        akka_net_Akka_Cluster_Benchmarks["Akka.Cluster.Benchmarks"]
        akka_net_RemotePingPong["RemotePingPong"]
        akka_net_Akka_Cluster_Cpu_Benchmark["Akka.Cluster.Cpu.Benchmark"]
        akka_net_PingPong["PingPong"]
        akka_net_SpawnBenchmark["SpawnBenchmark"]
        akka_net_Akka_AspNetCore["Akka.AspNetCore"]
        akka_net_TimeServer["TimeServer"]
        akka_net_System1["System1"]
        akka_net_System2["System2"]
        akka_net_Shared["Shared"]
        akka_net_ClusterSharding_Node["ClusterSharding.Node"]
        akka_net_ShoppingCart["ShoppingCart"]
        akka_net_TcpEchoService_Server["TcpEchoService.Server"]
        akka_net_HelloAkka["HelloAkka"]
        akka_net_Routing["Routing"]
        akka_net_AkkaWindowsService["AkkaWindowsService"]
        akka_net_HelloWorld["HelloWorld"]
        akka_net_AkkaHeadlesssService["AkkaHeadlesssService"]
        akka_net_SymbolLookup["SymbolLookup"]
        akka_net_ChatServer["ChatServer"]
        akka_net_AppConfig["AppConfig"]
        akka_net_FaultTolerance["FaultTolerance"]
    end
    subgraph DataSources
        datasource_akka_net_RabbitMQ[("RabbitMQ")]
        datasource_akka_net_Dapper[("Dapper")]
        datasource_akka_net_Kafka[("Kafka")]
    end
```

## nuget groups

```mermaid
graph LR
    subgraph System["System"]
        nuget_System_Diagnostics_Process["System.Diagnostics.Process<br/>4.3.0"]
        nuget_System_Reflection["System.Reflection<br/>4.3.0"]
        nuget_System_Runtime["System.Runtime<br/>4.3.1"]
        nuget_System_Collections_Specialized["System.Collections.Specialized<br/>4.3.0"]
        nuget_System_Net_Sockets["System.Net.Sockets<br/>4.3.0"]
        nuget_System_Runtime_Extensions["System.Runtime.Extensions<br/>4.3.1"]
        nuget_System_Reflection_TypeExtensions["System.Reflection.TypeExtensions<br/>4.7.0"]
        nuget_System_Linq_Async["System.Linq.Async<br/>6.0.1"]
        System_more["... +6 more"]
    end
    subgraph Microsoft["Microsoft"]
        nuget_Microsoft_Extensions_Hosting["Microsoft.Extensions.Hosting<br/>[6.0.*,)"]
        nuget_Microsoft_NET_Test_Sdk["Microsoft.NET.Test.Sdk<br/>17.9.0"]
        nuget_Microsoft_Extensions_DependencyInjection_Abstractions["Microsoft.Extensions.DependencyInjection.Abstractions<br/>[6.0.*,)"]
        nuget_Microsoft_Data_SQLite["Microsoft.Data.SQLite<br/>8.0.4"]
        nuget_Microsoft_Data_Sqlite["Microsoft.Data.Sqlite<br/>8.0.14"]
        nuget_Microsoft_Data_Sqlite_Core["Microsoft.Data.Sqlite.Core<br/>8.0.14"]
        nuget_Microsoft_Extensions_Hosting_WindowsServices["Microsoft.Extensions.Hosting.WindowsServices<br/>[6.0.*,)"]
        nuget_Microsoft_Extensions_Http["Microsoft.Extensions.Http<br/>[6.0.*,)"]
        Microsoft_more["... +2 more"]
    end
    subgraph xunit["xunit"]
        nuget_xunit["xunit<br/>2.8.1"]
        nuget_xunit_runner_visualstudio["xunit.runner.visualstudio<br/>2.8.1, 3.0.2"]
        nuget_xunit_v3["xunit.v3<br/>2.0.1"]
        nuget_xunit_v3_extensibility_core["xunit.v3.extensibility.core<br/>2.0.1"]
        nuget_xunit_v3_assert["xunit.v3.assert<br/>2.0.1"]
    end
    subgraph Akka["Akka"]
        nuget_Akka_Management["Akka.Management<br/>1.5.50"]
        nuget_Akka_MultiNode_TestAdapter["Akka.MultiNode.TestAdapter<br/>1.5.40"]
        nuget_Akka_Bootstrap_Docker["Akka.Bootstrap.Docker<br/>0.5.3"]
        nuget_Akka_Persistence_Sql["Akka.Persistence.Sql<br/>1.5.44"]
        nuget_Akka_Analyzers["Akka.Analyzers<br/>0.3.3"]
    end
    subgraph Reactive["Reactive"]
        nuget_Reactive_Streams_TCK["Reactive.Streams.TCK<br/>1.0.4"]
        nuget_Reactive_Streams["Reactive.Streams<br/>1.0.4"]
    end
    subgraph FsCheck["FsCheck"]
        nuget_FsCheck_Xunit["FsCheck.Xunit<br/>2.16.6"]
        nuget_FsCheck["FsCheck<br/>2.16.6"]
    end
    subgraph Verify["Verify"]
        nuget_Verify_Xunit["Verify.Xunit<br/>25.0.2"]
        nuget_Verify_DiffPlex["Verify.DiffPlex<br/>3.0.0"]
    end
    subgraph Nito["Nito"]
        nuget_Nito_AsyncEx_Coordination["Nito.AsyncEx.Coordination<br/>5.1.2"]
        nuget_Nito_AsyncEx_Context["Nito.AsyncEx.Context<br/>5.1.2"]
    end
    subgraph BenchmarkDotNet["BenchmarkDotNet"]
        nuget_BenchmarkDotNet["BenchmarkDotNet<br/>0.13.11, 0.15.4"]
    end
    subgraph FluentAssertions["FluentAssertions"]
        nuget_FluentAssertions["FluentAssertions<br/>5.10.3"]
    end
    subgraph NDesk["NDesk"]
        nuget_NDesk_Options_Core["NDesk.Options.Core<br/>1.2.8"]
    end
    subgraph Tmds["Tmds"]
        nuget_Tmds_ExecFunction["Tmds.ExecFunction<br/>0.7.1"]
    end
    subgraph Universe["Universe"]
        nuget_Universe_CpuUsage["Universe.CpuUsage<br/>2.2.497.598"]
    end
    subgraph coverlet["coverlet"]
        nuget_coverlet_collector["coverlet.collector<br/>3.1.2"]
    end
    subgraph LightningDB["LightningDB"]
        nuget_LightningDB["LightningDB<br/>0.16.0"]
    end
```
