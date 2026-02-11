# Dependency Visualizations

## landscape

```mermaid
graph LR
    subgraph Webapps
        Lean_QuantConnect_Api["QuantConnect.Api"]
    end
    subgraph Librarys
        Lean_QuantConnect_Configuration["QuantConnect.Configuration"]
        Lean_QuantConnect_Compression["QuantConnect.Compression"]
        Lean_QuantConnect_Messaging["QuantConnect.Messaging"]
        Lean_QuantConnect_Research["QuantConnect.Research"]
        Lean_QuantConnect_Brokerages["QuantConnect.Brokerages"]
        Lean_QuantConnect_Algorithm_CSharp["QuantConnect.Algorithm.CSharp"]
        Lean_QuantConnect_Algorithm_Framework["QuantConnect.Algorithm.Framework"]
        Lean_QuantConnect_Lean_Engine["QuantConnect.Lean.Engine"]
        Lean_QuantConnect_Queues["QuantConnect.Queues"]
        Lean_QuantConnect_AlgorithmFactory["QuantConnect.AlgorithmFactory"]
        Lean_QuantConnect["QuantConnect"]
        Lean_QuantConnect_Indicators["QuantConnect.Indicators"]
        Lean_QuantConnect_Optimizer["QuantConnect.Optimizer"]
        Lean_QuantConnect_Algorithm_Python["QuantConnect.Algorithm.Python"]
        Lean_QuantConnect_Logging["QuantConnect.Logging"]
        Lean_QuantConnect_Algorithm["QuantConnect.Algorithm"]
    end
    subgraph Applications
        Lean_QuantConnect_Optimizer_Launcher["QuantConnect.Optimizer.Launcher"]
        Lean_QuantConnect_DownloaderDataProvider_Launcher["QuantConnect.DownloaderDataProvider.Launcher"]
        Lean_QuantConnect_Lean_Launcher["QuantConnect.Lean.Launcher"]
        Lean_QuantConnect_Report["QuantConnect.Report"]
    end
    subgraph Tools
        Lean_QuantConnect_ToolBox["QuantConnect.ToolBox"]
    end
    subgraph Tests
        Lean_QuantConnect_Tests["QuantConnect.Tests"]
    end
    Lean_QuantConnect_Api --> Lean_QuantConnect
    Lean_QuantConnect_Api --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Api --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Configuration --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Compression --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Optimizer_Launcher --> Lean_QuantConnect
    Lean_QuantConnect_Optimizer_Launcher --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Optimizer_Launcher --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Optimizer_Launcher --> Lean_QuantConnect_Optimizer
    Lean_QuantConnect_Messaging --> Lean_QuantConnect
    Lean_QuantConnect_Messaging --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Messaging --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Research --> Lean_QuantConnect_Algorithm_Framework
    Lean_QuantConnect_Research --> Lean_QuantConnect_Algorithm
    Lean_QuantConnect_Research --> Lean_QuantConnect_Api
    Lean_QuantConnect_Research --> Lean_QuantConnect
    Lean_QuantConnect_Research --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Research --> Lean_QuantConnect_Lean_Engine
    Lean_QuantConnect_Research --> Lean_QuantConnect_Indicators
    Lean_QuantConnect_Research --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Research --> Lean_QuantConnect_Queues
    Lean_QuantConnect_Brokerages --> Lean_QuantConnect_Api
    Lean_QuantConnect_Brokerages --> Lean_QuantConnect
    Lean_QuantConnect_Brokerages --> Lean_QuantConnect_Compression
    Lean_QuantConnect_Brokerages --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Brokerages --> Lean_QuantConnect_Logging
    Lean_QuantConnect_DownloaderDataProvider_Launcher --> Lean_QuantConnect
    Lean_QuantConnect_DownloaderDataProvider_Launcher --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_DownloaderDataProvider_Launcher --> Lean_QuantConnect_Lean_Engine
    Lean_QuantConnect_DownloaderDataProvider_Launcher --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Algorithm_CSharp --> Lean_QuantConnect_Algorithm_Framework
    Lean_QuantConnect_Algorithm_CSharp --> Lean_QuantConnect_Algorithm
    Lean_QuantConnect_Algorithm_CSharp --> Lean_QuantConnect
    Lean_QuantConnect_Algorithm_CSharp --> Lean_QuantConnect_Indicators
    Lean_QuantConnect_Algorithm_Framework --> Lean_QuantConnect_Algorithm
    Lean_QuantConnect_Algorithm_Framework --> Lean_QuantConnect
    Lean_QuantConnect_Algorithm_Framework --> Lean_QuantConnect_Indicators
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect_Algorithm_CSharp
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect_AlgorithmFactory
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect_Algorithm
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect_Api
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect_Brokerages
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect_Compression
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect_Indicators
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Queues --> Lean_QuantConnect_Brokerages
    Lean_QuantConnect_Queues --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Queues --> Lean_QuantConnect
    Lean_QuantConnect_Queues --> Lean_QuantConnect_Logging
    Lean_QuantConnect_AlgorithmFactory --> Lean_QuantConnect_Algorithm
    Lean_QuantConnect_AlgorithmFactory --> Lean_QuantConnect
    Lean_QuantConnect_AlgorithmFactory --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_AlgorithmFactory --> Lean_QuantConnect_Logging
    Lean_QuantConnect_ToolBox --> Lean_QuantConnect_Lean_Engine
    Lean_QuantConnect --> Lean_QuantConnect_Compression
    Lean_QuantConnect --> Lean_QuantConnect_Configuration
    Lean_QuantConnect --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Tests --> Lean_QuantConnect_Algorithm_CSharp
    Lean_QuantConnect_Tests --> Lean_QuantConnect_Algorithm_Framework
    Lean_QuantConnect_Tests --> Lean_QuantConnect_AlgorithmFactory
    Lean_QuantConnect_Tests --> Lean_QuantConnect_Algorithm
    Lean_QuantConnect_Tests --> Lean_QuantConnect_Api
    Lean_QuantConnect_Tests --> Lean_QuantConnect_Brokerages
    Lean_QuantConnect_Tests --> Lean_QuantConnect
    Lean_QuantConnect_Tests --> Lean_QuantConnect_Compression
    Lean_QuantConnect_Tests --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Tests --> Lean_QuantConnect_DownloaderDataProvider_Launcher
    Lean_QuantConnect_Tests --> Lean_QuantConnect_Lean_Engine
    Lean_QuantConnect_Tests --> Lean_QuantConnect_Indicators
    Lean_QuantConnect_Tests --> Lean_QuantConnect_Optimizer
    Lean_QuantConnect_Tests --> Lean_QuantConnect_Research
    Lean_QuantConnect_Tests --> Lean_QuantConnect_Lean_Launcher
    Lean_QuantConnect_Tests --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Tests --> Lean_QuantConnect_Messaging
    Lean_QuantConnect_Tests --> Lean_QuantConnect_Queues
    Lean_QuantConnect_Tests --> Lean_QuantConnect_Report
    Lean_QuantConnect_Tests --> Lean_QuantConnect_ToolBox
    Lean_QuantConnect_Indicators --> Lean_QuantConnect
    Lean_QuantConnect_Indicators --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Optimizer --> Lean_QuantConnect
    Lean_QuantConnect_Optimizer --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Optimizer --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Algorithm_Python --> Lean_QuantConnect_Algorithm
    Lean_QuantConnect_Algorithm_Python --> Lean_QuantConnect
    Lean_QuantConnect_Algorithm_Python --> Lean_QuantConnect_Indicators
    Lean_QuantConnect_Lean_Launcher --> Lean_QuantConnect_Algorithm_CSharp
    Lean_QuantConnect_Lean_Launcher --> Lean_QuantConnect_AlgorithmFactory
    Lean_QuantConnect_Lean_Launcher --> Lean_QuantConnect_Algorithm
    Lean_QuantConnect_Lean_Launcher --> Lean_QuantConnect_Api
    Lean_QuantConnect_Lean_Launcher --> Lean_QuantConnect_Brokerages
    Lean_QuantConnect_Lean_Launcher --> Lean_QuantConnect_Compression
    Lean_QuantConnect_Lean_Launcher --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Lean_Launcher --> Lean_QuantConnect_DownloaderDataProvider_Launcher
    Lean_QuantConnect_Lean_Launcher --> Lean_QuantConnect_Lean_Engine
    Lean_QuantConnect_Lean_Launcher --> Lean_QuantConnect_Indicators
    Lean_QuantConnect_Lean_Launcher --> Lean_QuantConnect
    Lean_QuantConnect_Lean_Launcher --> Lean_QuantConnect_Optimizer_Launcher
    Lean_QuantConnect_Lean_Launcher --> Lean_QuantConnect_Research
    Lean_QuantConnect_Lean_Launcher --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Lean_Launcher --> Lean_QuantConnect_Messaging
    Lean_QuantConnect_Lean_Launcher --> Lean_QuantConnect_Queues
    Lean_QuantConnect_Lean_Launcher --> Lean_QuantConnect_ToolBox
    Lean_QuantConnect_Report --> Lean_QuantConnect_Algorithm
    Lean_QuantConnect_Report --> Lean_QuantConnect_Api
    Lean_QuantConnect_Report --> Lean_QuantConnect_Brokerages
    Lean_QuantConnect_Report --> Lean_QuantConnect
    Lean_QuantConnect_Report --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Report --> Lean_QuantConnect_Lean_Engine
    Lean_QuantConnect_Report --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Report --> Lean_QuantConnect_Messaging
    Lean_QuantConnect_Report --> Lean_QuantConnect_ToolBox
    Lean_QuantConnect_Algorithm --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Algorithm --> Lean_QuantConnect_Indicators
    Lean_QuantConnect_Algorithm --> Lean_QuantConnect
    Lean_QuantConnect_Algorithm --> Lean_QuantConnect_Logging
```

## core libraries

```mermaid
graph TD
    Lean_QuantConnect_Configuration["QuantConnect.Configuration"]
    Lean_QuantConnect_Compression["QuantConnect.Compression"]
    Lean_QuantConnect_Messaging["QuantConnect.Messaging"]
    Lean_QuantConnect_Research["QuantConnect.Research"]
    Lean_QuantConnect_Brokerages["QuantConnect.Brokerages"]
    Lean_QuantConnect_Algorithm_CSharp["QuantConnect.Algorithm.CSharp"]
    Lean_QuantConnect_Algorithm_Framework["QuantConnect.Algorithm.Framework"]
    Lean_QuantConnect_Lean_Engine["QuantConnect.Lean.Engine"]
    Lean_QuantConnect_Queues["QuantConnect.Queues"]
    Lean_QuantConnect_AlgorithmFactory["QuantConnect.AlgorithmFactory"]
    Lean_QuantConnect["QuantConnect"]
    Lean_QuantConnect_Indicators["QuantConnect.Indicators"]
    Lean_QuantConnect_Optimizer["QuantConnect.Optimizer"]
    Lean_QuantConnect_Algorithm_Python["QuantConnect.Algorithm.Python"]
    Lean_QuantConnect_Logging["QuantConnect.Logging"]
    Lean_QuantConnect_Algorithm["QuantConnect.Algorithm"]
    Lean_QuantConnect_Configuration --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Compression --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Messaging --> Lean_QuantConnect
    Lean_QuantConnect_Messaging --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Messaging --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Research --> Lean_QuantConnect_Algorithm_Framework
    Lean_QuantConnect_Research --> Lean_QuantConnect_Algorithm
    Lean_QuantConnect_Research --> Lean_QuantConnect
    Lean_QuantConnect_Research --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Research --> Lean_QuantConnect_Lean_Engine
    Lean_QuantConnect_Research --> Lean_QuantConnect_Indicators
    Lean_QuantConnect_Research --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Research --> Lean_QuantConnect_Queues
    Lean_QuantConnect_Brokerages --> Lean_QuantConnect
    Lean_QuantConnect_Brokerages --> Lean_QuantConnect_Compression
    Lean_QuantConnect_Brokerages --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Brokerages --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Algorithm_CSharp --> Lean_QuantConnect_Algorithm_Framework
    Lean_QuantConnect_Algorithm_CSharp --> Lean_QuantConnect_Algorithm
    Lean_QuantConnect_Algorithm_CSharp --> Lean_QuantConnect
    Lean_QuantConnect_Algorithm_CSharp --> Lean_QuantConnect_Indicators
    Lean_QuantConnect_Algorithm_Framework --> Lean_QuantConnect_Algorithm
    Lean_QuantConnect_Algorithm_Framework --> Lean_QuantConnect
    Lean_QuantConnect_Algorithm_Framework --> Lean_QuantConnect_Indicators
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect_Algorithm_CSharp
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect_AlgorithmFactory
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect_Algorithm
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect_Brokerages
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect_Compression
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect_Indicators
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect
    Lean_QuantConnect_Lean_Engine --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Queues --> Lean_QuantConnect_Brokerages
    Lean_QuantConnect_Queues --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Queues --> Lean_QuantConnect
    Lean_QuantConnect_Queues --> Lean_QuantConnect_Logging
    Lean_QuantConnect_AlgorithmFactory --> Lean_QuantConnect_Algorithm
    Lean_QuantConnect_AlgorithmFactory --> Lean_QuantConnect
    Lean_QuantConnect_AlgorithmFactory --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_AlgorithmFactory --> Lean_QuantConnect_Logging
    Lean_QuantConnect --> Lean_QuantConnect_Compression
    Lean_QuantConnect --> Lean_QuantConnect_Configuration
    Lean_QuantConnect --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Indicators --> Lean_QuantConnect
    Lean_QuantConnect_Indicators --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Optimizer --> Lean_QuantConnect
    Lean_QuantConnect_Optimizer --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Optimizer --> Lean_QuantConnect_Logging
    Lean_QuantConnect_Algorithm_Python --> Lean_QuantConnect_Algorithm
    Lean_QuantConnect_Algorithm_Python --> Lean_QuantConnect
    Lean_QuantConnect_Algorithm_Python --> Lean_QuantConnect_Indicators
    Lean_QuantConnect_Algorithm --> Lean_QuantConnect_Configuration
    Lean_QuantConnect_Algorithm --> Lean_QuantConnect_Indicators
    Lean_QuantConnect_Algorithm --> Lean_QuantConnect
    Lean_QuantConnect_Algorithm --> Lean_QuantConnect_Logging
```

## data infrastructure

```mermaid
graph LR
    subgraph Applications
        Lean_QuantConnect_Api["QuantConnect.Api"]
        Lean_QuantConnect_Optimizer_Launcher["QuantConnect.Optimizer.Launcher"]
        Lean_QuantConnect_DownloaderDataProvider_Launcher["QuantConnect.DownloaderDataProvider.Launcher"]
        Lean_QuantConnect_Lean_Launcher["QuantConnect.Lean.Launcher"]
        Lean_QuantConnect_Report["QuantConnect.Report"]
    end
    subgraph DataSources
        datasource_Lean_Dapper_Execute[("Dapper.Execute")]
        datasource_Lean_MongoDB_Read[("MongoDB.Read")]
        datasource_Lean_Redis_Read[("Redis.Read")]
        datasource_Lean_Redis_Write[("Redis.Write")]
        datasource_Lean_Kafka_Consumer[("Kafka.Consumer")]
        datasource_Lean_SQL_Select[("SQL.Select")]
    end
```

## data flow

```mermaid
graph LR
    subgraph Projects["Services & Projects"]
        QuantConnect["QuantConnect"]
    end
    subgraph APIs["API Routes"]
        url_https___api_tournament_crunchdao_com_v2_rounds__current(["https://api.tournament.crunchdao.com/v2/rounds/@current"])
    end
    url_https___api_tournament_crunchdao_com_v2_rounds__current -.->|consume| QuantConnect
```

## nuget groups

```mermaid
graph LR
    subgraph Accord["Accord"]
        nuget_Accord["Accord<br/>3.6.0"]
        nuget_Accord_Fuzzy["Accord.Fuzzy<br/>3.6.0"]
        nuget_Accord_MachineLearning["Accord.MachineLearning<br/>3.6.0"]
        nuget_Accord_Math["Accord.Math<br/>3.6.0"]
        nuget_Accord_Statistics["Accord.Statistics<br/>3.6.0"]
    end
    subgraph Plotly["Plotly"]
        nuget_Plotly_NET["Plotly.NET<br/>5.1.0"]
        nuget_Plotly_NET_CSharp["Plotly.NET.CSharp<br/>0.13.0"]
        nuget_Plotly_NET_Interactive["Plotly.NET.Interactive<br/>5.0.0"]
    end
    subgraph Microsoft["Microsoft"]
        nuget_Microsoft_IO_RecyclableMemoryStream["Microsoft.IO.RecyclableMemoryStream<br/>3.0.1"]
        nuget_Microsoft_NET_Test_Sdk["Microsoft.NET.Test.Sdk<br/>16.9.4"]
        nuget_Microsoft_TestPlatform_ObjectModel["Microsoft.TestPlatform.ObjectModel<br/>16.9.4"]
    end
    subgraph Common["Common"]
        nuget_Common_Logging["Common.Logging<br/>3.4.1"]
        nuget_Common_Logging_Core["Common.Logging.Core<br/>3.4.1"]
    end
    subgraph Newtonsoft["Newtonsoft"]
        nuget_Newtonsoft_Json["Newtonsoft.Json<br/>13.0.2"]
    end
    subgraph NodaTime["NodaTime"]
        nuget_NodaTime["NodaTime<br/>3.0.5"]
    end
    subgraph RestSharp["RestSharp"]
        nuget_RestSharp["RestSharp<br/>106.12.0"]
    end
    subgraph McMaster["McMaster"]
        nuget_McMaster_Extensions_CommandLineUtils["McMaster.Extensions.CommandLineUtils<br/>2.6.0"]
    end
    subgraph DotNetZip["DotNetZip"]
        nuget_DotNetZip["DotNetZip<br/>1.16.0"]
    end
    subgraph SharpZipLib["SharpZipLib"]
        nuget_SharpZipLib["SharpZipLib<br/>1.3.3"]
    end
    subgraph NetMQ["NetMQ"]
        nuget_NetMQ["NetMQ<br/>4.0.1.6"]
    end
    subgraph QuantConnect["QuantConnect"]
        nuget_QuantConnect_pythonnet["QuantConnect.pythonnet<br/>2.0.52"]
    end
    subgraph CsvHelper["CsvHelper"]
        nuget_CsvHelper["CsvHelper<br/>19.0.0"]
    end
    subgraph DynamicInterop["DynamicInterop"]
        nuget_DynamicInterop["DynamicInterop<br/>0.9.1"]
    end
    subgraph MathNet["MathNet"]
        nuget_MathNet_Numerics["MathNet.Numerics<br/>5.0.0"]
    end
```

## business layers

```mermaid
graph TD
    layer_Engine["Engine (9)"]
    layer_Service["Service (1)"]
    layer_DataAccess["DataAccess (7)"]
    layer_Infrastructure["Infrastructure (2)"]
    layer_Unclassified["Unclassified (4)"]
    layer_DataAccess -->|13 refs| layer_Infrastructure
    layer_Unclassified -->|13 refs| layer_Engine
    layer_Engine -->|11 refs| layer_Infrastructure
    layer_DataAccess -->|9 refs| layer_Engine
    layer_Engine -->|9 refs| layer_DataAccess
    layer_Unclassified -->|7 refs| layer_DataAccess
    layer_Unclassified -->|6 refs| layer_Infrastructure
    layer_Engine -->|4 refs| layer_Unclassified
    layer_Service -->|2 refs| layer_Infrastructure
    layer_DataAccess -->|2 refs| layer_Unclassified
    layer_Unclassified -->|2 refs| layer_Service
    layer_DataAccess -->|2 refs| layer_Service
    layer_Engine -->|2 refs| layer_Service
    layer_Service -->|1 refs| layer_Engine
```

## e2e flows

```mermaid
graph TD
    no_data[No end-to-end flow paths found]
```
