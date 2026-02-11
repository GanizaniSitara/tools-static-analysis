# Dependency Visualizations

## landscape

```mermaid
graph LR
    subgraph Tests
        StockSharp_Algo_Testing["Algo.Testing"]
        StockSharp_Tests["Tests"]
        StockSharp_04_Testing_HistoryConsole["04_Testing.HistoryConsole"]
        StockSharp_04_Testing_HistoryConsole_fromsrc["04_Testing.HistoryConsole_fromsrc"]
        StockSharp_02_Testing_Optimization["02_Testing.Optimization"]
        StockSharp_02_Testing_Optimization_fromsrc["02_Testing.Optimization_fromsrc"]
        StockSharp_01_Testing_History["01_Testing.History"]
        StockSharp_01_Testing_History_fromsrc["01_Testing.History_fromsrc"]
        StockSharp_03_Testing_RealTime_fromsrc["03_Testing.RealTime_fromsrc"]
        StockSharp_03_Testing_RealTime["03_Testing.RealTime"]
    end
    subgraph Librarys
        StockSharp_Media_Names["Media.Names"]
        StockSharp_Configuration["Configuration"]
        StockSharp_Charting_Interfaces["Charting.Interfaces"]
        StockSharp_Algo_Indicators["Algo.Indicators"]
        StockSharp_Diagram_Core["Diagram.Core"]
        StockSharp_Reporting["Reporting"]
        StockSharp_Algo_Import["Algo.Import"]
        StockSharp_Algo_Analytics_CSharp["Algo.Analytics.CSharp"]
        StockSharp_BusinessEntities["BusinessEntities"]
        StockSharp_Messages["Messages"]
        StockSharp_Algo_Strategies["Algo.Strategies"]
        StockSharp_Algo_Export["Algo.Export"]
        StockSharp_Alerts_Interfaces["Alerts.Interfaces"]
        StockSharp_Algo_Analytics["Algo.Analytics"]
        StockSharp_Algo_Compilation["Algo.Compilation"]
        StockSharp_Algo_Gpu["Algo.Gpu"]
        StockSharp_Algo["Algo"]
    end
    subgraph Tools
        StockSharp_Localization_Extractor["Localization.Extractor"]
        StockSharp_Localization_Generator["Localization.Generator"]
        StockSharp_Media_Generator["Media.Generator"]
    end
    subgraph Desktopapps
        StockSharp_Media["Media"]
    end
    subgraph Connectors
        StockSharp_Coinbase["Coinbase"]
        StockSharp_Bitexbook["Bitexbook"]
        StockSharp_Tinkoff["Tinkoff"]
        StockSharp_BitStamp["BitStamp"]
        StockSharp_Bitalong["Bitalong"]
        StockSharp_Btce["Btce"]
        StockSharp_FTX["FTX"]
    end
    StockSharp_Algo_Testing --> StockSharp_Algo
    StockSharp_Media_Names --> StockSharp_Media_Generator
    StockSharp_Configuration --> StockSharp_Messages
    StockSharp_Charting_Interfaces --> StockSharp_BusinessEntities
    StockSharp_Algo_Indicators --> StockSharp_Algo
    StockSharp_Diagram_Core --> StockSharp_Alerts_Interfaces
    StockSharp_Diagram_Core --> StockSharp_Algo_Strategies
    StockSharp_Diagram_Core --> StockSharp_Algo_Indicators
    StockSharp_Reporting --> StockSharp_Messages
    StockSharp_Algo_Import --> StockSharp_Algo
    StockSharp_Algo_Analytics_CSharp --> StockSharp_Algo_Analytics
    StockSharp_Tests --> StockSharp_Algo_Analytics
    StockSharp_Tests --> StockSharp_Algo_Compilation
    StockSharp_Tests --> StockSharp_Algo_Export
    StockSharp_Tests --> StockSharp_Algo_Import
    StockSharp_Tests --> StockSharp_Algo_Gpu
    StockSharp_Tests --> StockSharp_Algo_Indicators
    StockSharp_Tests --> StockSharp_Algo_Strategies
    StockSharp_Tests --> StockSharp_Algo_Testing
    StockSharp_Tests --> StockSharp_Diagram_Core
    StockSharp_Tests --> StockSharp_Alerts_Interfaces
    StockSharp_BusinessEntities --> StockSharp_Messages
    StockSharp_Algo_Strategies --> StockSharp_Alerts_Interfaces
    StockSharp_Algo_Strategies --> StockSharp_Algo_Testing
    StockSharp_Algo_Export --> StockSharp_Algo_Indicators
    StockSharp_Alerts_Interfaces --> StockSharp_BusinessEntities
    StockSharp_Algo_Analytics --> StockSharp_Algo_Indicators
    StockSharp_Algo_Compilation --> StockSharp_Configuration
    StockSharp_Algo_Gpu --> StockSharp_Algo_Indicators
    StockSharp_04_Testing_HistoryConsole -.-> StockSharp_Algo
    StockSharp_04_Testing_HistoryConsole --> StockSharp_Algo_Indicators
    StockSharp_04_Testing_HistoryConsole --> StockSharp_Algo_Strategies
    StockSharp_04_Testing_HistoryConsole_fromsrc -.-> StockSharp_Algo
    StockSharp_04_Testing_HistoryConsole_fromsrc --> StockSharp_Algo_Indicators
    StockSharp_04_Testing_HistoryConsole_fromsrc --> StockSharp_Algo_Strategies
    StockSharp_02_Testing_Optimization -.-> StockSharp_Algo
    StockSharp_02_Testing_Optimization_fromsrc -.-> StockSharp_Algo
    StockSharp_01_Testing_History -.-> StockSharp_Algo
    StockSharp_01_Testing_History_fromsrc -.-> StockSharp_Algo
    StockSharp_03_Testing_RealTime_fromsrc -.-> StockSharp_Algo
    StockSharp_03_Testing_RealTime -.-> StockSharp_Algo
    StockSharp_Coinbase --> StockSharp_Messages
    StockSharp_Coinbase --> StockSharp_Media_Names
    StockSharp_Bitexbook --> StockSharp_Messages
    StockSharp_Bitexbook --> StockSharp_Media_Names
    StockSharp_Tinkoff --> StockSharp_Messages
    StockSharp_Tinkoff --> StockSharp_Media_Names
    StockSharp_BitStamp --> StockSharp_Messages
    StockSharp_BitStamp --> StockSharp_Media_Names
    StockSharp_Bitalong --> StockSharp_Messages
    StockSharp_Bitalong --> StockSharp_Media_Names
    StockSharp_Btce --> StockSharp_Messages
    StockSharp_Btce --> StockSharp_Media_Names
    StockSharp_FTX --> StockSharp_Messages
    StockSharp_FTX --> StockSharp_Media_Names
    StockSharp_Algo --> StockSharp_Reporting
    StockSharp_Algo --> StockSharp_Charting_Interfaces
    StockSharp_Algo --> StockSharp_Configuration
```

## core libraries

```mermaid
graph TD
    StockSharp_Media_Names["Media.Names"]
    StockSharp_Configuration["Configuration"]
    StockSharp_Charting_Interfaces["Charting.Interfaces"]
    StockSharp_Algo_Indicators["Algo.Indicators"]
    StockSharp_Diagram_Core["Diagram.Core"]
    StockSharp_Reporting["Reporting"]
    StockSharp_Algo_Import["Algo.Import"]
    StockSharp_Algo_Analytics_CSharp["Algo.Analytics.CSharp"]
    StockSharp_BusinessEntities["BusinessEntities"]
    StockSharp_Messages["Messages"]
    StockSharp_Algo_Strategies["Algo.Strategies"]
    StockSharp_Algo_Export["Algo.Export"]
    StockSharp_Alerts_Interfaces["Alerts.Interfaces"]
    StockSharp_Algo_Analytics["Algo.Analytics"]
    StockSharp_Algo_Compilation["Algo.Compilation"]
    StockSharp_Algo_Gpu["Algo.Gpu"]
    StockSharp_Algo["Algo"]
    StockSharp_Configuration --> StockSharp_Messages
    StockSharp_Charting_Interfaces --> StockSharp_BusinessEntities
    StockSharp_Algo_Indicators --> StockSharp_Algo
    StockSharp_Diagram_Core --> StockSharp_Alerts_Interfaces
    StockSharp_Diagram_Core --> StockSharp_Algo_Strategies
    StockSharp_Diagram_Core --> StockSharp_Algo_Indicators
    StockSharp_Reporting --> StockSharp_Messages
    StockSharp_Algo_Import --> StockSharp_Algo
    StockSharp_Algo_Analytics_CSharp --> StockSharp_Algo_Analytics
    StockSharp_BusinessEntities --> StockSharp_Messages
    StockSharp_Algo_Strategies --> StockSharp_Alerts_Interfaces
    StockSharp_Algo_Export --> StockSharp_Algo_Indicators
    StockSharp_Alerts_Interfaces --> StockSharp_BusinessEntities
    StockSharp_Algo_Analytics --> StockSharp_Algo_Indicators
    StockSharp_Algo_Compilation --> StockSharp_Configuration
    StockSharp_Algo_Gpu --> StockSharp_Algo_Indicators
    StockSharp_Algo --> StockSharp_Reporting
    StockSharp_Algo --> StockSharp_Charting_Interfaces
    StockSharp_Algo --> StockSharp_Configuration
```

## data infrastructure

```mermaid
graph LR
    subgraph Applications
        StockSharp_Media["Media"]
    end
    subgraph DataSources
        datasource_StockSharp_Redis_Write[("Redis.Write")]
        datasource_StockSharp_Redis_Read[("Redis.Read")]
        datasource_StockSharp_Kafka_Consumer[("Kafka.Consumer")]
        datasource_StockSharp_MongoDB_Read[("MongoDB.Read")]
        datasource_StockSharp_SqlClient[("SqlClient")]
        datasource_StockSharp_SQL_CreateTable[("SQL.CreateTable")]
        datasource_StockSharp_Kafka_Topic[("Kafka.Topic")]
    end
```

## data flow

```mermaid
graph LR
    subgraph Projects["Services & Projects"]
        Algo_Analytics["Algo.Analytics"]
        Tests["Tests"]
    end
    subgraph Database["Database / Storage"]
        table_to[("to")]
    end
    subgraph APIs["API Routes"]
        url_delete(["delete"])
        url_nonexistent(["nonexistent"])
        url_TestStorage(["TestStorage"])
        url_test_example_com(["test@example.com"])
        url_TEST_EXAMPLE_COM(["TEST@EXAMPLE.COM"])
    end
    Algo_Analytics ==>|write| table_to
    url_delete -.->|consume| Tests
    url_nonexistent -.->|consume| Tests
    url_TestStorage -.->|consume| Tests
    url_test_example_com -.->|consume| Tests
    url_TEST_EXAMPLE_COM -.->|consume| Tests
```

## nuget groups

```mermaid
graph LR
    subgraph Ecng["Ecng"]
        nuget_Ecng_Configuration["Ecng.Configuration<br/>1.0.*"]
        nuget_Ecng_Serialization["Ecng.Serialization<br/>1.0.*"]
        nuget_Ecng_ComponentModel["Ecng.ComponentModel<br/>1.0.*"]
        nuget_Ecng_Excel["Ecng.Excel<br/>1.0.*"]
        nuget_Ecng_UnitTesting["Ecng.UnitTesting<br/>1.0.*"]
        nuget_Ecng_Excel_OpenXml["Ecng.Excel.OpenXml<br/>1.0.*"]
        nuget_Ecng_Data_Ado["Ecng.Data.Ado<br/>1.0.*"]
        nuget_Ecng_Drawing["Ecng.Drawing<br/>1.0.*"]
        Ecng_more["... +10 more"]
    end
    subgraph StockSharp["StockSharp"]
        nuget_StockSharp_Samples_HistoryData["StockSharp.Samples.HistoryData<br/>5.*"]
        nuget_StockSharp_Binance["StockSharp.Binance<br/>5.*"]
        nuget_StockSharp_Okex["StockSharp.Okex<br/>5.*"]
        nuget_StockSharp_GateIO["StockSharp.GateIO<br/>5.*"]
        nuget_StockSharp_Bitmex["StockSharp.Bitmex<br/>5.*"]
        nuget_StockSharp_Fix["StockSharp.Fix<br/>5.*"]
        nuget_StockSharp_Xaml_Charting["StockSharp.Xaml.Charting<br/>5.*"]
        nuget_StockSharp_Xaml["StockSharp.Xaml<br/>5.*"]
        StockSharp_more["... +3 more"]
    end
    subgraph Microsoft["Microsoft"]
        nuget_Microsoft_NET_Test_Sdk["Microsoft.NET.Test.Sdk<br/>17.13.0"]
        nuget_Microsoft_Data_SqlClient["Microsoft.Data.SqlClient<br/>6.*"]
        nuget_Microsoft_CodeAnalysis_CSharp["Microsoft.CodeAnalysis.CSharp<br/>4.12.0"]
        nuget_Microsoft_CodeAnalysis_Analyzers["Microsoft.CodeAnalysis.Analyzers<br/>3.3.4"]
        nuget_Microsoft_Bcl_AsyncInterfaces["Microsoft.Bcl.AsyncInterfaces<br/>8.*"]
    end
    subgraph MSTest["MSTest"]
        nuget_MSTest_TestAdapter["MSTest.TestAdapter<br/>3.11.1"]
        nuget_MSTest_TestFramework["MSTest.TestFramework<br/>3.11.1"]
    end
    subgraph System["System"]
        nuget_System_Text_Json["System.Text.Json<br/>8.*"]
        nuget_System_Text_Encodings_Web["System.Text.Encodings.Web<br/>8.*"]
    end
    subgraph MathNet["MathNet"]
        nuget_MathNet_Numerics_FSharp["MathNet.Numerics.FSharp<br/>6.0.0-beta2"]
        nuget_MathNet_Numerics["MathNet.Numerics<br/>6.0.0-beta2"]
    end
    subgraph NuGet["NuGet"]
        nuget_NuGet_Configuration["NuGet.Configuration<br/>7.0.1"]
    end
    subgraph Spectre["Spectre"]
        nuget_Spectre_Console_Cli["Spectre.Console.Cli<br/>0.48.0"]
    end
    subgraph Moq["Moq"]
        nuget_Moq["Moq<br/>4.*"]
    end
    subgraph IronPython["IronPython"]
        nuget_IronPython_StdLib["IronPython.StdLib<br/>3.4.2"]
    end
    subgraph NumpyDotNet["NumpyDotNet"]
        nuget_NumpyDotNet["NumpyDotNet<br/>0.9.*"]
    end
    subgraph FSharp["FSharp"]
        nuget_FSharp_Control_TaskSeq["FSharp.Control.TaskSeq<br/>0.*"]
    end
    subgraph FSharpPlus["FSharpPlus"]
        nuget_FSharpPlus["FSharpPlus<br/>1.*"]
    end
    subgraph ILGPU["ILGPU"]
        nuget_ILGPU_Algorithms["ILGPU.Algorithms<br/>1.*"]
    end
    subgraph Grpc["Grpc"]
        nuget_Grpc_Net_Client["Grpc.Net.Client<br/>2.71.0"]
    end
```
