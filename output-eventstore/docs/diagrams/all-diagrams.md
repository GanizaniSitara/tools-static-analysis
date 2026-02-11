# Dependency Visualizations

## landscape

```mermaid
graph LR
    subgraph Tests
        src_KurrentDB_Core_Tests["KurrentDB.Core.Tests"]
        src_FakePlugin["FakePlugin"]
        src_KurrentDB_Core_Testing["KurrentDB.Core.Testing"]
        src_KurrentDB_Plugins_Tests["KurrentDB.Plugins.Tests"]
        src_KurrentDB_Licensing_Tests["KurrentDB.Licensing.Tests"]
        src_KurrentDB_Auth_UserCertificates_Tests["KurrentDB.Auth.UserCertificates.Tests"]
        src_KurrentDB_Auth_Ldaps_Tests["KurrentDB.Auth.Ldaps.Tests"]
        src_KurrentDB_Api_V2_Tests["KurrentDB.Api.V2.Tests"]
        src_KurrentDB_Auth_LegacyAuthorizationWithStreamAuthorizationDisabled_Tests["KurrentDB.Auth.LegacyAuthorizationWithStreamAuthorizationDisabled.Tests"]
        src_KurrentDB_Projections_Core_Tests["KurrentDB.Projections.Core.Tests"]
        src_KurrentDB_Surge_Testing["KurrentDB.Surge.Testing"]
        src_KurrentDB_Common_Tests["KurrentDB.Common.Tests"]
        src_KurrentDB_Security_EncryptionAtRest_Tests["KurrentDB.Security.EncryptionAtRest.Tests"]
        src_KurrentDB_Core_Testing_NUnit["KurrentDB.Core.Testing.NUnit"]
        src_KurrentDB_Projections_Core_XUnit_Tests["KurrentDB.Projections.Core.XUnit.Tests"]
        src_KurrentDB_Auth_StreamPolicyPlugin_Tests["KurrentDB.Auth.StreamPolicyPlugin.Tests"]
        src_KurrentDB_Surge_Testing_Messages["KurrentDB.Surge.Testing.Messages"]
        src_KurrentDB_Core_Testing_XUnit["KurrentDB.Core.Testing.XUnit"]
        src_KurrentDB_SystemRuntime_Tests["KurrentDB.SystemRuntime.Tests"]
        src_KurrentDB_AutoScavenge_Tests["KurrentDB.AutoScavenge.Tests"]
        src_KurrentDB_Projections_Core_Javascript_Tests["KurrentDB.Projections.Core.Javascript.Tests"]
        src_KurrentDB_SchemaRegistry_Tests["KurrentDB.SchemaRegistry.Tests"]
        src_KurrentDB_SecondaryIndexing_LoadTesting["KurrentDB.SecondaryIndexing.LoadTesting"]
        src_KurrentDB_Plugins_TestHelpers["KurrentDB.Plugins.TestHelpers"]
        src_KurrentDB_BufferManagement_Tests["KurrentDB.BufferManagement.Tests"]
        src_KurrentDB_Diagnostics_LogsEndpointPlugin_Tests["KurrentDB.Diagnostics.LogsEndpointPlugin.Tests"]
        src_KurrentDB_LogV3_Tests["KurrentDB.LogV3.Tests"]
        src_KurrentDB_SourceGenerators_Tests["KurrentDB.SourceGenerators.Tests"]
        src_KurrentDB_TestClient["KurrentDB.TestClient"]
        src_KurrentDB_Core_XUnit_Tests["KurrentDB.Core.XUnit.Tests"]
        src_KurrentDB_Auth_OAuth_Tests["KurrentDB.Auth.OAuth.Tests"]
        src_KurrentDB_Surge_Tests["KurrentDB.Surge.Tests"]
        src_KurrentDB_Core_TUnit_Tests["KurrentDB.Core.TUnit.Tests"]
        src_KurrentDB_Testing_ClusterVNodeApp["KurrentDB.Testing.ClusterVNodeApp"]
        src_KurrentDB_SecondaryIndexing_Tests["KurrentDB.SecondaryIndexing.Tests"]
        src_KurrentDB_Connectors_Tests["KurrentDB.Connectors.Tests"]
        src_KurrentDB_Connectors_TestServer["KurrentDB.Connectors.TestServer"]
        src_KurrentDB_Testing["KurrentDB.Testing"]
        src_KurrentDB_OtlpExporterPlugin_Tests["KurrentDB.OtlpExporterPlugin.Tests"]
        src_KurrentDB_TcpPlugin_Tests["KurrentDB.TcpPlugin.Tests"]
    end
    subgraph Librarys
        src_KurrentDB_OtlpExporterPlugin["KurrentDB.OtlpExporterPlugin"]
        src_KurrentDB_SystemRuntime["KurrentDB.SystemRuntime"]
        src_KurrentDB_Auth_StreamPolicyPlugin["KurrentDB.Auth.StreamPolicyPlugin"]
        src_KurrentDB_Native["KurrentDB.Native"]
        src_KurrentDB_LogCommon["KurrentDB.LogCommon"]
        src_KurrentDB_LogV3["KurrentDB.LogV3"]
        src_KurrentDB_Surge["KurrentDB.Surge"]
        src_KurrentDB_Transport_Http["KurrentDB.Transport.Http"]
        src_KurrentDB_NETCore_Compatibility["KurrentDB.NETCore.Compatibility"]
        src_KurrentDB_Projections_Core["KurrentDB.Projections.Core"]
        src_KurrentDB_POC_ConnectedSubsystemsPlugin["KurrentDB.POC.ConnectedSubsystemsPlugin"]
        src_KurrentDB_Licensing["KurrentDB.Licensing"]
        src_KurrentDB_AutoScavenge["KurrentDB.AutoScavenge"]
        src_KurrentDB_Common["KurrentDB.Common"]
        src_KurrentDB_Ammeter["KurrentDB.Ammeter"]
        src_KurrentDB_SchemaRegistry["KurrentDB.SchemaRegistry"]
        src_KurrentDB_SchemaRegistry_Protocol["KurrentDB.SchemaRegistry.Protocol"]
        src_KurrentDB_DuckDB["KurrentDB.DuckDB"]
        src_KurrentDB_Logging["KurrentDB.Logging"]
        src_KurrentDB_Transport_Tcp["KurrentDB.Transport.Tcp"]
        src_KurrentDB_SecondaryIndexing["KurrentDB.SecondaryIndexing"]
        src_KurrentDB_PluginHosting["KurrentDB.PluginHosting"]
        src_KurrentDB_UI["KurrentDB.UI"]
        src_KurrentDB_Core["KurrentDB.Core"]
        src_KurrentDB_POC_IO_Core["KurrentDB.POC.IO.Core"]
        src_KurrentDB_TcpPlugin["KurrentDB.TcpPlugin"]
        src_KurrentDB_BufferManagement["KurrentDB.BufferManagement"]
        src_KurrentDB_Plugins["KurrentDB.Plugins"]
    end
    subgraph Webapps
        src_KurrentDB_Plugins_Api_V2["KurrentDB.Plugins.Api.V2"]
        src_KurrentDB_Api_V2["KurrentDB.Api.V2"]
        src_KurrentDB_ClusterNode_Web["KurrentDB.ClusterNode.Web"]
        src_KurrentDB["KurrentDB"]
    end
    subgraph Applications
        src_KurrentDB_Diagnostics_LogsEndpointPlugin["KurrentDB.Diagnostics.LogsEndpointPlugin"]
        src_KurrentDB_Security_EncryptionAtRest["KurrentDB.Security.EncryptionAtRest"]
        src_KurrentDB_Auth_OAuth["KurrentDB.Auth.OAuth"]
        src_KurrentDB_MicroBenchmarks["KurrentDB.MicroBenchmarks"]
        src_KurrentDB_Plugins_SchemaRegistry["KurrentDB.Plugins.SchemaRegistry"]
        src_KurrentDB_Auth_Ldaps["KurrentDB.Auth.Ldaps"]
        src_KurrentDB_Auth_LegacyAuthorizationWithStreamAuthorizationDisabled["KurrentDB.Auth.LegacyAuthorizationWithStreamAuthorizationDisabled"]
        src_KurrentDB_Auth_UserCertificates["KurrentDB.Auth.UserCertificates"]
    end
    subgraph Tools
        src_KurrentDB_SourceGenerators["KurrentDB.SourceGenerators"]
    end
    subgraph Connectors
        src_KurrentDB_Connectors_Contracts["KurrentDB.Connectors.Contracts"]
        src_KurrentDB_Plugins_Connectors["KurrentDB.Plugins.Connectors"]
        src_KurrentDB_Connectors["KurrentDB.Connectors"]
    end
    src_KurrentDB_Core_Tests --> src_KurrentDB_Core_Testing_NUnit
    src_KurrentDB_OtlpExporterPlugin --> src_KurrentDB_Logging
    src_KurrentDB_Core_Testing --> src_KurrentDB_Core
    src_KurrentDB_Core_Testing --> src_KurrentDB_PluginHosting
    src_KurrentDB_Plugins_Api_V2 --> src_KurrentDB_Api_V2
    src_KurrentDB_Plugins_Tests --> src_KurrentDB_Plugins
    src_KurrentDB_Licensing_Tests --> src_KurrentDB_Core
    src_KurrentDB_Licensing_Tests --> src_KurrentDB_Licensing
    src_KurrentDB_Auth_UserCertificates_Tests --> src_KurrentDB_Auth_UserCertificates
    src_KurrentDB_Auth_UserCertificates_Tests --> src_KurrentDB_Common
    src_KurrentDB_Auth_Ldaps_Tests --> src_KurrentDB_Auth_Ldaps
    src_KurrentDB_Api_V2_Tests --> src_KurrentDB_Testing_ClusterVNodeApp
    src_KurrentDB_Api_V2_Tests --> src_KurrentDB_Testing
    src_KurrentDB_Api_V2_Tests --> src_KurrentDB_Api_V2
    src_KurrentDB_Auth_LegacyAuthorizationWithStreamAuthorizationDisabled_Tests --> src_KurrentDB_Auth_LegacyAuthorizationWithStreamAuthorizationDisabled
    src_KurrentDB_Projections_Core_Tests --> src_KurrentDB_Common
    src_KurrentDB_Projections_Core_Tests --> src_KurrentDB_Core_Testing_NUnit
    src_KurrentDB_Projections_Core_Tests --> src_KurrentDB_Core
    src_KurrentDB_Projections_Core_Tests --> src_KurrentDB_Projections_Core
    src_KurrentDB_Auth_StreamPolicyPlugin --> src_KurrentDB_Core
    src_KurrentDB_Native --> src_KurrentDB_SystemRuntime
    src_KurrentDB_Api_V2 --> src_KurrentDB_Core
    src_KurrentDB_Api_V2 --> src_KurrentDB_SecondaryIndexing
    src_KurrentDB_Surge_Testing --> src_KurrentDB
    src_KurrentDB_Common_Tests --> src_KurrentDB_Common
    src_KurrentDB_LogV3 --> src_KurrentDB_LogCommon
    src_KurrentDB_Security_EncryptionAtRest_Tests --> src_KurrentDB_Common
    src_KurrentDB_Security_EncryptionAtRest_Tests --> src_KurrentDB_Security_EncryptionAtRest
    src_KurrentDB_Core_Testing_NUnit --> src_KurrentDB_Core_Testing
    src_KurrentDB_Projections_Core_XUnit_Tests --> src_KurrentDB_Core_Testing
    src_KurrentDB_Projections_Core_XUnit_Tests --> src_KurrentDB_Projections_Core
    src_KurrentDB_Surge --> src_KurrentDB_Core
    src_KurrentDB_Auth_StreamPolicyPlugin_Tests --> src_KurrentDB_Core_Testing
    src_KurrentDB_Auth_StreamPolicyPlugin_Tests --> src_KurrentDB_Auth_StreamPolicyPlugin
    src_KurrentDB_Transport_Http --> src_KurrentDB_BufferManagement
    src_KurrentDB_Transport_Http --> src_KurrentDB_Common
    src_KurrentDB_Projections_Core --> src_KurrentDB_Common
    src_KurrentDB_Projections_Core --> src_KurrentDB_Core
    src_KurrentDB_Projections_Core --> src_KurrentDB_Transport_Http
    src_KurrentDB_Projections_Core --> src_KurrentDB_SourceGenerators
    src_KurrentDB_POC_ConnectedSubsystemsPlugin --> src_KurrentDB_Core
    src_KurrentDB_POC_ConnectedSubsystemsPlugin --> src_KurrentDB_PluginHosting
    src_KurrentDB_POC_ConnectedSubsystemsPlugin --> src_KurrentDB_POC_IO_Core
    src_KurrentDB_MicroBenchmarks --> src_KurrentDB_Projections_Core_Tests
    src_KurrentDB_MicroBenchmarks --> src_KurrentDB_Projections_Core
    src_KurrentDB_Core_Testing_XUnit --> src_KurrentDB_Core_Testing
    src_KurrentDB_AutoScavenge --> src_KurrentDB_POC_ConnectedSubsystemsPlugin
    src_KurrentDB_AutoScavenge --> src_KurrentDB_POC_IO_Core
    src_KurrentDB_Common --> src_KurrentDB_SystemRuntime
    src_KurrentDB_SystemRuntime_Tests --> src_KurrentDB_SystemRuntime
    src_KurrentDB_SystemRuntime_Tests --> src_KurrentDB_Core
    src_KurrentDB_AutoScavenge_Tests --> src_KurrentDB_AutoScavenge
    src_KurrentDB_Ammeter --> src_KurrentDB_Api_V2_Tests
    src_KurrentDB_Ammeter --> src_KurrentDB_Core_TUnit_Tests
    src_KurrentDB_Projections_Core_Javascript_Tests --> src_KurrentDB_Projections_Core
    src_KurrentDB_SchemaRegistry --> src_KurrentDB_Surge
    src_KurrentDB_SchemaRegistry --> src_KurrentDB_SchemaRegistry_Protocol
    src_KurrentDB_SchemaRegistry_Tests --> src_KurrentDB_Surge_Testing_Messages
    src_KurrentDB_SchemaRegistry_Tests --> src_KurrentDB_Testing_ClusterVNodeApp
    src_KurrentDB_SchemaRegistry_Tests --> src_KurrentDB_Testing
    src_KurrentDB_SchemaRegistry_Tests --> src_KurrentDB
    src_KurrentDB_SchemaRegistry_Tests --> src_KurrentDB_SchemaRegistry
    src_KurrentDB_Plugins_SchemaRegistry --> src_KurrentDB_SchemaRegistry
    src_KurrentDB_SecondaryIndexing_LoadTesting --> src_KurrentDB_Connectors_TestServer
    src_KurrentDB_SecondaryIndexing_LoadTesting --> src_KurrentDB_SecondaryIndexing_Tests
    src_KurrentDB_SecondaryIndexing_LoadTesting --> src_KurrentDB_SecondaryIndexing
    src_KurrentDB_Logging --> src_KurrentDB_Common
    src_KurrentDB_Plugins_TestHelpers --> src_KurrentDB_Plugins
    src_KurrentDB_BufferManagement_Tests --> src_KurrentDB_BufferManagement
    src_KurrentDB_Diagnostics_LogsEndpointPlugin_Tests --> src_KurrentDB_Common
    src_KurrentDB_Diagnostics_LogsEndpointPlugin_Tests --> src_KurrentDB_Diagnostics_LogsEndpointPlugin
    src_KurrentDB_LogV3_Tests --> src_KurrentDB_LogV3
    src_KurrentDB_Transport_Tcp --> src_KurrentDB_BufferManagement
    src_KurrentDB_Transport_Tcp --> src_KurrentDB_Common
    src_KurrentDB_SourceGenerators_Tests --> src_KurrentDB_SourceGenerators
    src_KurrentDB_TestClient --> src_KurrentDB_BufferManagement
    src_KurrentDB_TestClient --> src_KurrentDB_Common
    src_KurrentDB_TestClient --> src_KurrentDB_Core
    src_KurrentDB_TestClient --> src_KurrentDB_Transport_Http
    src_KurrentDB_TestClient --> src_KurrentDB_Transport_Tcp
    src_KurrentDB_Core_XUnit_Tests --> src_KurrentDB_Core_Testing_XUnit
    src_KurrentDB_Core_XUnit_Tests --> src_KurrentDB_Core
    src_KurrentDB_Core_XUnit_Tests --> src_KurrentDB_SourceGenerators
    src_KurrentDB_Auth_OAuth_Tests --> src_KurrentDB_Auth_OAuth
    src_KurrentDB_SecondaryIndexing --> src_KurrentDB_Common
    src_KurrentDB_SecondaryIndexing --> src_KurrentDB_Core
    src_KurrentDB_Surge_Tests --> src_KurrentDB_Surge_Testing
    src_KurrentDB_Core_TUnit_Tests --> src_KurrentDB_Testing_ClusterVNodeApp
    src_KurrentDB_Core_TUnit_Tests --> src_KurrentDB_Testing
    src_KurrentDB_Testing_ClusterVNodeApp --> src_KurrentDB_Testing
    src_KurrentDB_Testing_ClusterVNodeApp --> src_KurrentDB
    src_KurrentDB_Core --> src_KurrentDB_Common
    src_KurrentDB_Core --> src_KurrentDB_DuckDB
    src_KurrentDB_Core --> src_KurrentDB_Licensing
    src_KurrentDB_Core --> src_KurrentDB_Logging
    src_KurrentDB_Core --> src_KurrentDB_LogV3
    src_KurrentDB_Core --> src_KurrentDB_Native
    src_KurrentDB_Core --> src_KurrentDB_Plugins
    src_KurrentDB_Core --> src_KurrentDB_Transport_Http
    src_KurrentDB_Core --> src_KurrentDB_Transport_Tcp
    src_KurrentDB_Core --> src_KurrentDB_NETCore_Compatibility
    src_KurrentDB_Core --> src_KurrentDB_SourceGenerators
    src_KurrentDB_SecondaryIndexing_Tests --> src_KurrentDB_SecondaryIndexing
    src_KurrentDB_SecondaryIndexing_Tests --> src_KurrentDB_Core_Testing_XUnit
    src_KurrentDB_SecondaryIndexing_Tests --> src_KurrentDB_Core
    src_KurrentDB_SecondaryIndexing_Tests --> src_KurrentDB_Surge_Testing
    src_KurrentDB_POC_IO_Core --> src_KurrentDB_Core
    src_KurrentDB_Connectors_Tests --> src_KurrentDB
    src_KurrentDB_Connectors_Tests --> src_KurrentDB_Connectors
    src_KurrentDB_Connectors_Tests --> src_KurrentDB_Surge_Testing
    src_KurrentDB_Plugins_Connectors --> src_KurrentDB_Connectors
    src_KurrentDB_Connectors --> src_KurrentDB_Common
    src_KurrentDB_Connectors --> src_KurrentDB_Core
    src_KurrentDB_Connectors --> src_KurrentDB_Surge
    src_KurrentDB_Connectors --> src_KurrentDB_SystemRuntime
    src_KurrentDB_Connectors --> src_KurrentDB_Connectors_Contracts
    src_KurrentDB_Connectors_TestServer --> src_KurrentDB_Connectors
    src_KurrentDB_OtlpExporterPlugin_Tests --> src_KurrentDB_OtlpExporterPlugin
    src_KurrentDB_TcpPlugin_Tests --> src_KurrentDB_Core_Testing
    src_KurrentDB_TcpPlugin_Tests --> src_KurrentDB_TcpPlugin
    src_KurrentDB_TcpPlugin --> src_KurrentDB_Core
    src_KurrentDB --> src_KurrentDB_Auth_Ldaps
    src_KurrentDB --> src_KurrentDB_Auth_LegacyAuthorizationWithStreamAuthorizationDisabled
    src_KurrentDB --> src_KurrentDB_Auth_OAuth
    src_KurrentDB --> src_KurrentDB_Auth_StreamPolicyPlugin
    src_KurrentDB --> src_KurrentDB_Auth_UserCertificates
    src_KurrentDB --> src_KurrentDB_ClusterNode_Web
    src_KurrentDB --> src_KurrentDB_Common
    src_KurrentDB --> src_KurrentDB_Core
    src_KurrentDB --> src_KurrentDB_Diagnostics_LogsEndpointPlugin
    src_KurrentDB --> src_KurrentDB_OtlpExporterPlugin
    src_KurrentDB --> src_KurrentDB_PluginHosting
    src_KurrentDB --> src_KurrentDB_POC_ConnectedSubsystemsPlugin
    src_KurrentDB --> src_KurrentDB_Projections_Core
    src_KurrentDB --> src_KurrentDB_Security_EncryptionAtRest
    src_KurrentDB --> src_KurrentDB_AutoScavenge
    src_KurrentDB --> src_KurrentDB_TcpPlugin
    src_KurrentDB --> src_KurrentDB_SecondaryIndexing
    src_KurrentDB --> src_KurrentDB_UI
    src_KurrentDB --> src_KurrentDB_Plugins_Connectors
    src_KurrentDB --> src_KurrentDB_Plugins_SchemaRegistry
    src_KurrentDB --> src_KurrentDB_Plugins_Api_V2
```

## core libraries

```mermaid
graph TD
    src_KurrentDB_OtlpExporterPlugin["KurrentDB.OtlpExporterPlugin"]
    src_KurrentDB_SystemRuntime["KurrentDB.SystemRuntime"]
    src_KurrentDB_Auth_StreamPolicyPlugin["KurrentDB.Auth.StreamPolicyPlugin"]
    src_KurrentDB_Native["KurrentDB.Native"]
    src_KurrentDB_LogCommon["KurrentDB.LogCommon"]
    src_KurrentDB_LogV3["KurrentDB.LogV3"]
    src_KurrentDB_Surge["KurrentDB.Surge"]
    src_KurrentDB_Transport_Http["KurrentDB.Transport.Http"]
    src_KurrentDB_NETCore_Compatibility["KurrentDB.NETCore.Compatibility"]
    src_KurrentDB_Projections_Core["KurrentDB.Projections.Core"]
    src_KurrentDB_POC_ConnectedSubsystemsPlugin["KurrentDB.POC.ConnectedSubsystemsPlugin"]
    src_KurrentDB_Licensing["KurrentDB.Licensing"]
    src_KurrentDB_AutoScavenge["KurrentDB.AutoScavenge"]
    src_KurrentDB_Common["KurrentDB.Common"]
    src_KurrentDB_Ammeter["KurrentDB.Ammeter"]
    src_KurrentDB_SchemaRegistry["KurrentDB.SchemaRegistry"]
    src_KurrentDB_SchemaRegistry_Protocol["KurrentDB.SchemaRegistry.Protocol"]
    src_KurrentDB_DuckDB["KurrentDB.DuckDB"]
    src_KurrentDB_Logging["KurrentDB.Logging"]
    src_KurrentDB_Transport_Tcp["KurrentDB.Transport.Tcp"]
    src_KurrentDB_SecondaryIndexing["KurrentDB.SecondaryIndexing"]
    src_KurrentDB_PluginHosting["KurrentDB.PluginHosting"]
    src_KurrentDB_UI["KurrentDB.UI"]
    src_KurrentDB_Core["KurrentDB.Core"]
    src_KurrentDB_POC_IO_Core["KurrentDB.POC.IO.Core"]
    src_KurrentDB_TcpPlugin["KurrentDB.TcpPlugin"]
    src_KurrentDB_BufferManagement["KurrentDB.BufferManagement"]
    src_KurrentDB_Plugins["KurrentDB.Plugins"]
    src_KurrentDB_OtlpExporterPlugin --> src_KurrentDB_Logging
    src_KurrentDB_Auth_StreamPolicyPlugin --> src_KurrentDB_Core
    src_KurrentDB_Native --> src_KurrentDB_SystemRuntime
    src_KurrentDB_LogV3 --> src_KurrentDB_LogCommon
    src_KurrentDB_Surge --> src_KurrentDB_Core
    src_KurrentDB_Transport_Http --> src_KurrentDB_BufferManagement
    src_KurrentDB_Transport_Http --> src_KurrentDB_Common
    src_KurrentDB_Projections_Core --> src_KurrentDB_Common
    src_KurrentDB_Projections_Core --> src_KurrentDB_Core
    src_KurrentDB_Projections_Core --> src_KurrentDB_Transport_Http
    src_KurrentDB_POC_ConnectedSubsystemsPlugin --> src_KurrentDB_Core
    src_KurrentDB_POC_ConnectedSubsystemsPlugin --> src_KurrentDB_PluginHosting
    src_KurrentDB_POC_ConnectedSubsystemsPlugin --> src_KurrentDB_POC_IO_Core
    src_KurrentDB_AutoScavenge --> src_KurrentDB_POC_ConnectedSubsystemsPlugin
    src_KurrentDB_AutoScavenge --> src_KurrentDB_POC_IO_Core
    src_KurrentDB_Common --> src_KurrentDB_SystemRuntime
    src_KurrentDB_SchemaRegistry --> src_KurrentDB_Surge
    src_KurrentDB_SchemaRegistry --> src_KurrentDB_SchemaRegistry_Protocol
    src_KurrentDB_Logging --> src_KurrentDB_Common
    src_KurrentDB_Transport_Tcp --> src_KurrentDB_BufferManagement
    src_KurrentDB_Transport_Tcp --> src_KurrentDB_Common
    src_KurrentDB_SecondaryIndexing --> src_KurrentDB_Common
    src_KurrentDB_SecondaryIndexing --> src_KurrentDB_Core
    src_KurrentDB_Core --> src_KurrentDB_Common
    src_KurrentDB_Core --> src_KurrentDB_DuckDB
    src_KurrentDB_Core --> src_KurrentDB_Licensing
    src_KurrentDB_Core --> src_KurrentDB_Logging
    src_KurrentDB_Core --> src_KurrentDB_LogV3
    src_KurrentDB_Core --> src_KurrentDB_Native
    src_KurrentDB_Core --> src_KurrentDB_Plugins
    src_KurrentDB_Core --> src_KurrentDB_Transport_Http
    src_KurrentDB_Core --> src_KurrentDB_Transport_Tcp
    src_KurrentDB_Core --> src_KurrentDB_NETCore_Compatibility
    src_KurrentDB_POC_IO_Core --> src_KurrentDB_Core
    src_KurrentDB_TcpPlugin --> src_KurrentDB_Core
```

## data infrastructure

```mermaid
graph LR
    subgraph Applications
        src_KurrentDB_Plugins_Api_V2["KurrentDB.Plugins.Api.V2"]
        src_KurrentDB_Diagnostics_LogsEndpointPlugin["KurrentDB.Diagnostics.LogsEndpointPlugin"]
        src_KurrentDB_Security_EncryptionAtRest["KurrentDB.Security.EncryptionAtRest"]
        src_KurrentDB_Api_V2["KurrentDB.Api.V2"]
        src_KurrentDB_Auth_OAuth["KurrentDB.Auth.OAuth"]
        src_KurrentDB_MicroBenchmarks["KurrentDB.MicroBenchmarks"]
        src_KurrentDB_Plugins_SchemaRegistry["KurrentDB.Plugins.SchemaRegistry"]
        src_KurrentDB_Auth_Ldaps["KurrentDB.Auth.Ldaps"]
        src_KurrentDB_ClusterNode_Web["KurrentDB.ClusterNode.Web"]
        src_KurrentDB_Auth_LegacyAuthorizationWithStreamAuthorizationDisabled["KurrentDB.Auth.LegacyAuthorizationWithStreamAuthorizationDisabled"]
        src_KurrentDB_Auth_UserCertificates["KurrentDB.Auth.UserCertificates"]
        src_KurrentDB["KurrentDB"]
    end
    subgraph DataSources
        datasource_src_Kafka_Consumer[("Kafka.Consumer")]
        datasource_src_Redis_Read[("Redis.Read")]
        datasource_src_Redis_Write[("Redis.Write")]
        datasource_src_Kafka_Topic[("Kafka.Topic")]
        datasource_src_Dapper_Execute[("Dapper.Execute")]
        datasource_src_MongoDB_Read[("MongoDB.Read")]
        datasource_src_Kafka_Producer[("Kafka.Producer")]
        datasource_src_SQL_CreateTable[("SQL.CreateTable")]
        datasource_src_SQL_Select[("SQL.Select")]
        datasource_src_SQL_Insert[("SQL.Insert")]
        datasource_src_SQL_Delete[("SQL.Delete")]
        datasource_src_Dapper_Query[("Dapper.Query")]
        datasource_src_MongoDB_Write[("MongoDB.Write")]
    end
```

## data flow

```mermaid
graph LR
    subgraph Projects["Services & Projects"]
        KurrentDB["KurrentDB"]
        KurrentDB_Auth_OAuth_Tests["KurrentDB.Auth.OAuth.Tests"]
        KurrentDB_Auth_UserCertificates_Tests["KurrentDB.Auth.UserCertificates.Tests"]
        KurrentDB_AutoScavenge["KurrentDB.AutoScavenge"]
        KurrentDB_AutoScavenge_Tests["KurrentDB.AutoScavenge.Tests"]
        KurrentDB_Core["KurrentDB.Core"]
        KurrentDB_Core_Tests["KurrentDB.Core.Tests"]
        KurrentDB_Core_XUnit_Tests["KurrentDB.Core.XUnit.Tests"]
        KurrentDB_Licensing["KurrentDB.Licensing"]
        KurrentDB_Licensing_Tests["KurrentDB.Licensing.Tests"]
        KurrentDB_SchemaRegistry["KurrentDB.SchemaRegistry"]
        KurrentDB_SchemaRegistry_Tests["KurrentDB.SchemaRegistry.Tests"]
        KurrentDB_SecondaryIndexing["KurrentDB.SecondaryIndexing"]
        KurrentDB_SecondaryIndexing_LoadTesting["KurrentDB.SecondaryIndexing.LoadTesting"]
        KurrentDB_SecondaryIndexing_Tests["KurrentDB.SecondaryIndexing.Tests"]
    end
    subgraph Database["Database / Storage"]
        table_schema_versions[("schema_versions")]
        table_schemas[("schemas")]
        table_idx_all[("idx_all")]
        table_inflight[("inflight")]
    end
    subgraph APIs["API Routes"]
        route__test(["/test"])
        route__my_controller(["/my-controller"])
        route_protected(["protected"])
        route_unprotected(["unprotected"])
        url__ping__(["/ping^\"])
        url__ping_format_json(["/ping?format=json"])
        url__ping_format_xml(["/ping?format=xml"])
        url__ping_format_text(["/ping?format=text"])
        url__license(["/license"])
        url__test(["/test"])
        route__license(["/license"])
        route__enabled(["/enabled"])
        route__status(["/status"])
        route__resume(["/resume"])
        route__pause(["/pause"])
        route__configure(["/configure"])
        route__auto_scavenge(["/auto-scavenge"])
        url__auto_scavenge_enabled(["/auto-scavenge/enabled"])
        url__auto_scavenge_status(["/auto-scavenge/status"])
        url__metrics(["/metrics"])
        url_https___localhost_2113_health_live(["https://localhost:2113/health/live"])
        url__streams__all(["/streams/$all"])
        url__streams_a_stream(["/streams/a-stream"])
        url__streams__systemstream(["/streams/$systemstream"])
        route__health(["/health"])
    end
    KurrentDB_SchemaRegistry ==>|write| table_schema_versions
    table_schema_versions -.->|read| KurrentDB_SchemaRegistry
    table_schema_versions -.->|read| KurrentDB_SchemaRegistry_Tests
    KurrentDB_SchemaRegistry ==>|write| table_schemas
    table_schemas -.->|read| KurrentDB_SchemaRegistry
    table_schemas -.->|read| KurrentDB_SchemaRegistry_Tests
    table_idx_all -.->|read| KurrentDB
    table_idx_all -.->|read| KurrentDB_SecondaryIndexing
    table_idx_all -.->|read| KurrentDB_SecondaryIndexing_LoadTesting
    table_idx_all -.->|read| KurrentDB_SecondaryIndexing_Tests
    table_inflight -.->|read| KurrentDB
    KurrentDB_Auth_UserCertificates_Tests ==>|expose| route__test
    KurrentDB_Core_Tests ==>|expose| route__test
    KurrentDB_Core_Tests ==>|expose| route__my_controller
    KurrentDB_Core_Tests ==>|expose| route_protected
    KurrentDB_Core_Tests ==>|expose| route_unprotected
    url__ping__ -.->|consume| KurrentDB_Core_Tests
    url__ping_format_json -.->|consume| KurrentDB_Core_Tests
    url__ping_format_xml -.->|consume| KurrentDB_Core_Tests
    url__ping_format_text -.->|consume| KurrentDB_Core_Tests
    url__license -.->|consume| KurrentDB_Licensing_Tests
    url__test -.->|consume| KurrentDB_Auth_UserCertificates_Tests
    KurrentDB_Licensing ==>|expose| route__license
    KurrentDB_AutoScavenge ==>|expose| route__enabled
    KurrentDB_AutoScavenge ==>|expose| route__status
    KurrentDB_AutoScavenge ==>|expose| route__resume
    KurrentDB_AutoScavenge ==>|expose| route__pause
    KurrentDB_AutoScavenge ==>|expose| route__configure
    KurrentDB_AutoScavenge ==>|expose| route__auto_scavenge
    url__auto_scavenge_enabled -.->|consume| KurrentDB_AutoScavenge_Tests
    url__auto_scavenge_status -.->|consume| KurrentDB_AutoScavenge_Tests
    url__metrics -.->|consume| KurrentDB_Core_XUnit_Tests
    url_https___localhost_2113_health_live -.->|consume| KurrentDB_Auth_OAuth_Tests
    url__streams__all -.->|consume| KurrentDB_Auth_OAuth_Tests
    url__streams_a_stream -.->|consume| KurrentDB_Auth_OAuth_Tests
    url__streams__systemstream -.->|consume| KurrentDB_Auth_OAuth_Tests
    KurrentDB_Core ==>|expose| route__health
```

## nuget groups

```mermaid
graph LR
    subgraph Microsoft["Microsoft"]
        nuget_Microsoft_OpenApi_Readers["Microsoft.OpenApi.Readers<br/>"]
        nuget_Microsoft_AspNetCore_TestHost["Microsoft.AspNetCore.TestHost<br/>"]
        nuget_Microsoft_Extensions_Diagnostics_Testing["Microsoft.Extensions.Diagnostics.Testing<br/>"]
        nuget_Microsoft_AspNetCore_Grpc_JsonTranscoding["Microsoft.AspNetCore.Grpc.JsonTranscoding<br/>"]
        nuget_Microsoft_Extensions_TimeProvider_Testing["Microsoft.Extensions.TimeProvider.Testing<br/>"]
        nuget_Microsoft_Extensions_Configuration_EnvironmentVariables["Microsoft.Extensions.Configuration.EnvironmentVariables<br/>"]
        nuget_Microsoft_Extensions_Hosting_Abstractions["Microsoft.Extensions.Hosting.Abstractions<br/>"]
        nuget_Microsoft_AspNetCore_Mvc_Testing["Microsoft.AspNetCore.Mvc.Testing<br/>"]
        Microsoft_more["... +21 more"]
    end
    subgraph Serilog["Serilog"]
        nuget_Serilog["Serilog<br/>"]
        nuget_Serilog_Sinks_OpenTelemetry["Serilog.Sinks.OpenTelemetry<br/>"]
        nuget_Serilog_Sinks_InMemory["Serilog.Sinks.InMemory<br/>"]
        nuget_Serilog_AspNetCore["Serilog.AspNetCore<br/>"]
        nuget_Serilog_Sinks_TextWriter["Serilog.Sinks.TextWriter<br/>"]
        nuget_Serilog_Enrichers_Thread["Serilog.Enrichers.Thread<br/>"]
        nuget_Serilog_Enrichers_Environment["Serilog.Enrichers.Environment<br/>"]
        nuget_Serilog_Enrichers_Process["Serilog.Enrichers.Process<br/>"]
        Serilog_more["... +15 more"]
    end
    subgraph Kurrent["Kurrent"]
        nuget_Kurrent_Surge["Kurrent.Surge<br/>"]
        nuget_Kurrent_Surge_Core["Kurrent.Surge.Core<br/>"]
        nuget_Kurrent_Quack["Kurrent.Quack<br/>"]
        nuget_Kurrent_Surge_DuckDB["Kurrent.Surge.DuckDB<br/>"]
        nuget_Kurrent_Surge_DataProtection["Kurrent.Surge.DataProtection<br/>"]
        nuget_Kurrent_Connectors_Elasticsearch["Kurrent.Connectors.Elasticsearch<br/>"]
        nuget_Kurrent_Connectors_Http["Kurrent.Connectors.Http<br/>"]
        nuget_Kurrent_Connectors_Kafka["Kurrent.Connectors.Kafka<br/>"]
        Kurrent_more["... +4 more"]
    end
    subgraph System["System"]
        nuget_System_Linq_Async["System.Linq.Async<br/>"]
        nuget_System_Diagnostics_PerformanceCounter["System.Diagnostics.PerformanceCounter<br/>"]
        nuget_System_ComponentModel_Composition["System.ComponentModel.Composition<br/>"]
        nuget_System_Reactive["System.Reactive<br/>"]
        nuget_System_IdentityModel_Tokens_Jwt["System.IdentityModel.Tokens.Jwt<br/>"]
        nuget_System_ServiceModel_Http["System.ServiceModel.Http<br/>"]
        nuget_System_Security_Cryptography_Pkcs["System.Security.Cryptography.Pkcs<br/>"]
        nuget_System_Security_Cryptography_Xml["System.Security.Cryptography.Xml<br/>"]
        System_more["... +1 more"]
    end
    subgraph Grpc["Grpc"]
        nuget_Grpc_Net_Client["Grpc.Net.Client<br/>"]
        nuget_Grpc_StatusProto["Grpc.StatusProto<br/>"]
        nuget_Grpc_Tools["Grpc.Tools<br/>"]
        nuget_Grpc_AspNetCore["Grpc.AspNetCore<br/>"]
        nuget_Grpc_AspNetCore_Web["Grpc.AspNetCore.Web<br/>"]
        nuget_Grpc_Net_Common["Grpc.Net.Common<br/>"]
        nuget_Grpc_Net_ClientFactory["Grpc.Net.ClientFactory<br/>"]
    end
    subgraph OpenTelemetry["OpenTelemetry"]
        nuget_OpenTelemetry_Exporter_OpenTelemetryProtocol["OpenTelemetry.Exporter.OpenTelemetryProtocol<br/>"]
        nuget_OpenTelemetry_Extensions_Hosting["OpenTelemetry.Extensions.Hosting<br/>"]
        nuget_OpenTelemetry["OpenTelemetry<br/>"]
        nuget_OpenTelemetry_Exporter_Prometheus_AspNetCore["OpenTelemetry.Exporter.Prometheus.AspNetCore<br/>"]
        nuget_OpenTelemetry_Instrumentation_AspNetCore["OpenTelemetry.Instrumentation.AspNetCore<br/>"]
    end
    subgraph DotNext["DotNext"]
        nuget_DotNext["DotNext<br/>"]
        nuget_DotNext_IO["DotNext.IO<br/>"]
        nuget_DotNext_Threading["DotNext.Threading<br/>"]
        nuget_DotNext_Unsafe["DotNext.Unsafe<br/>"]
    end
    subgraph Eventuous["Eventuous"]
        nuget_Eventuous_Testing["Eventuous.Testing<br/>"]
        nuget_Eventuous_Application["Eventuous.Application<br/>"]
        nuget_Eventuous_Extensions_AspNetCore["Eventuous.Extensions.AspNetCore<br/>"]
        nuget_Eventuous_Extensions_DependencyInjection["Eventuous.Extensions.DependencyInjection<br/>"]
    end
    subgraph Google["Google"]
        nuget_Google_Protobuf["Google.Protobuf<br/>"]
        nuget_Google_Cloud_Storage_V1["Google.Cloud.Storage.V1<br/>"]
        nuget_Google_Api_CommonProtos["Google.Api.CommonProtos<br/>"]
    end
    subgraph EventStore["EventStore"]
        nuget_EventStore_Client["EventStore.Client<br/>"]
        nuget_EventStore_Client_Grpc_Streams["EventStore.Client.Grpc.Streams<br/>"]
    end
    subgraph FluentAssertions["FluentAssertions"]
        nuget_FluentAssertions["FluentAssertions<br/>"]
        nuget_FluentAssertions_Analyzers["FluentAssertions.Analyzers<br/>"]
    end
    subgraph Polly["Polly"]
        nuget_Polly["Polly<br/>"]
        nuget_Polly_Core["Polly.Core<br/>"]
    end
    subgraph TestableIO["TestableIO"]
        nuget_TestableIO_System_IO_Abstractions["TestableIO.System.IO.Abstractions<br/>"]
        nuget_TestableIO_System_IO_Abstractions_TestingHelpers["TestableIO.System.IO.Abstractions.TestingHelpers<br/>"]
    end
    subgraph MudBlazor["MudBlazor"]
        nuget_MudBlazor["MudBlazor<br/>"]
        nuget_MudBlazor_Markdown["MudBlazor.Markdown<br/>"]
    end
    subgraph FluentStorage["FluentStorage"]
        nuget_FluentStorage["FluentStorage<br/>"]
        nuget_FluentStorage_AWS["FluentStorage.AWS<br/>"]
    end
```

## business layers

```mermaid
graph TD
    layer_Presentation["Presentation (1)"]
    layer_Service["Service (20)"]
    layer_DataAccess["DataAccess (17)"]
    layer_Infrastructure["Infrastructure (20)"]
    layer_Unclassified["Unclassified (26)"]
    layer_Unclassified -->|16 refs| layer_Infrastructure
    layer_DataAccess -->|12 refs| layer_Unclassified
    layer_Service -->|10 refs| layer_Unclassified
    layer_Unclassified -->|9 refs| layer_DataAccess
    layer_Unclassified -->|9 refs| layer_Service
    layer_DataAccess -->|8 refs| layer_Service
    layer_Infrastructure -->|7 refs| layer_Unclassified
    layer_DataAccess -->|6 refs| layer_Infrastructure
    layer_Service -->|5 refs| layer_DataAccess
    layer_Infrastructure -->|4 refs| layer_Service
    layer_Service -->|4 refs| layer_Infrastructure
    layer_Infrastructure -->|2 refs| layer_DataAccess
    layer_Unclassified -->|1 refs| layer_Presentation
```

## e2e flows

```mermaid
graph TD
    no_data[No end-to-end flow paths found]
```
