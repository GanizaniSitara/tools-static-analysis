# Dependency Map

## Overview

| Metric | Count |
|--------|-------|
| Repositories | 1 |
| Total Projects | 140 |
| NuGet Packages | 50 |
| Project References | 200 |
| Cross-Repo References | 70 |
| Data Access Findings | 1699 |
| Config Files | 1 |

## Project Categories

| Category | Count |
|----------|-------|
| Sample | 62 |
| Localization | 40 |
| Library | 17 |
| Test | 10 |
| Connector | 7 |
| Tool | 3 |
| DesktopApp | 1 |

## Full Landscape

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

## Core Library Hierarchy

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

## Data Infrastructure

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

## NuGet Package Groups

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

## Navigation

### Connector (7)
- [Coinbase](connectors/Coinbase.md)
- [Bitexbook](connectors/Bitexbook.md)
- [Tinkoff](connectors/Tinkoff.md)
- [BitStamp](connectors/BitStamp.md)
- [Bitalong](connectors/Bitalong.md)
- [Btce](connectors/Btce.md)
- [FTX](connectors/FTX.md)

### DesktopApp (1)
- [Media](applications/Media.md)

### Library (17)
- [Media.Names](libraries/Media.Names.md)
- [Configuration](libraries/Configuration.md)
- [Charting.Interfaces](libraries/Charting.Interfaces.md)
- [Algo.Indicators](libraries/Algo.Indicators.md)
- [Diagram.Core](libraries/Diagram.Core.md)
- [Reporting](libraries/Reporting.md)
- [Algo.Import](libraries/Algo.Import.md)
- [Algo.Analytics.CSharp](libraries/Algo.Analytics.CSharp.md)
- [BusinessEntities](libraries/BusinessEntities.md)
- [Messages](libraries/Messages.md)
- [Algo.Strategies](libraries/Algo.Strategies.md)
- [Algo.Export](libraries/Algo.Export.md)
- [Alerts.Interfaces](libraries/Alerts.Interfaces.md)
- [Algo.Analytics](libraries/Algo.Analytics.md)
- [Algo.Compilation](libraries/Algo.Compilation.md)
- [Algo.Gpu](libraries/Algo.Gpu.md)
- [Algo](libraries/Algo.md)

### Localization (40)
- [Localization](applications/Localization.md)
- [Localization.all](applications/Localization.all.md)
- [Localization.my](applications/Localization.my.md)
- [Localization.nl](applications/Localization.nl.md)
- [Localization.he](applications/Localization.he.md)
- [Localization.fi](applications/Localization.fi.md)
- [Localization.el](applications/Localization.el.md)
- [Localization.da](applications/Localization.da.md)
- [Localization.sv](applications/Localization.sv.md)
- [Localization.hi](applications/Localization.hi.md)
- [Localization.no](applications/Localization.no.md)
- [Localization.ko](applications/Localization.ko.md)
- [Localization.ar](applications/Localization.ar.md)
- [Localization.ta](applications/Localization.ta.md)
- [Localization.zh](applications/Localization.zh.md)
- [Localization.pt](applications/Localization.pt.md)
- [Localization.es](applications/Localization.es.md)
- [Localization.jv](applications/Localization.jv.md)
- [Localization.fa](applications/Localization.fa.md)
- [Localization.bn](applications/Localization.bn.md)
- ... +20 more

### Sample (62)
- [01_Candles.Realtime_fromsrc](applications/01_Candles.Realtime_fromsrc.md)
- [01_Candles.Realtime](applications/01_Candles.Realtime.md)
- [02_Candles.CombineHistoryRealtime](applications/02_Candles.CombineHistoryRealtime.md)
- [02_Candles.CombineHistoryRealtime_fromsrc](applications/02_Candles.CombineHistoryRealtime_fromsrc.md)
- [06_Strategies.HistoryQuoting_fromsrc](applications/06_Strategies.HistoryQuoting_fromsrc.md)
- [06_Strategies.HistoryQuoting](applications/06_Strategies.HistoryQuoting.md)
- [04_Strategies.HistoryMarketRule](applications/04_Strategies.HistoryMarketRule.md)
- [04_Strategies.HistoryMarketRule_fromsrc](applications/04_Strategies.HistoryMarketRule_fromsrc.md)
- [08_Strategies.LiveArbitrage_fromsrc](applications/08_Strategies.LiveArbitrage_fromsrc.md)
- [08_Strategies.LiveArbitrage](applications/08_Strategies.LiveArbitrage.md)
- [03_Strategies.HistoryTrend_fromsrc](applications/03_Strategies.HistoryTrend_fromsrc.md)
- [03_Strategies.HistoryTrend](applications/03_Strategies.HistoryTrend.md)
- [05_Strategies.HistoryIndex_fromsrc](applications/05_Strategies.HistoryIndex_fromsrc.md)
- [05_Strategies.HistoryIndex](applications/05_Strategies.HistoryIndex.md)
- [10_Strategies.LiveTerminal](applications/10_Strategies.LiveTerminal.md)
- [10_Strategies.LiveTerminal_fromsrc](applications/10_Strategies.LiveTerminal_fromsrc.md)
- [07_Strategies.LiveSpread](applications/07_Strategies.LiveSpread.md)
- [07_Strategies.LiveSpread_fromsrc](applications/07_Strategies.LiveSpread_fromsrc.md)
- [02_Strategies.HistoryBollingerBands](applications/02_Strategies.HistoryBollingerBands.md)
- [02_Strategies.HistoryBollingerBands_fromsrc](applications/02_Strategies.HistoryBollingerBands_fromsrc.md)
- ... +42 more

### Test (10)
- [Algo.Testing](applications/Algo.Testing.md)
- [Tests](applications/Tests.md)
- [04_Testing.HistoryConsole](applications/04_Testing.HistoryConsole.md)
- [04_Testing.HistoryConsole_fromsrc](applications/04_Testing.HistoryConsole_fromsrc.md)
- [02_Testing.Optimization](applications/02_Testing.Optimization.md)
- [02_Testing.Optimization_fromsrc](applications/02_Testing.Optimization_fromsrc.md)
- [01_Testing.History](applications/01_Testing.History.md)
- [01_Testing.History_fromsrc](applications/01_Testing.History_fromsrc.md)
- [03_Testing.RealTime_fromsrc](applications/03_Testing.RealTime_fromsrc.md)
- [03_Testing.RealTime](applications/03_Testing.RealTime.md)

### Tool (3)
- [Localization.Extractor](applications/Localization.Extractor.md)
- [Localization.Generator](applications/Localization.Generator.md)
- [Media.Generator](applications/Media.Generator.md)

- [Data Source Registry](data-sources/registry.md)

---

*Generated: 2026-02-11*
*Tool: Dependency Mapper (Static Analysis)*
