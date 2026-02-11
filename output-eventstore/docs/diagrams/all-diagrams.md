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
        datasource_src_Dapper[("Dapper")]
        datasource_src_Kafka[("Kafka")]
        datasource_src_RabbitMQ[("RabbitMQ")]
    end
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
