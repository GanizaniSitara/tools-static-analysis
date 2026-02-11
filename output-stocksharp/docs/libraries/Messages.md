# Messages

## Overview

| Property | Value |
|----------|-------|
| Category | Library |
| Repository | StockSharp |
| Path | `Messages/Messages.csproj` |
| Project References | 1 |
| NuGet Dependencies | 2 |
| Consumers | 10 |

## Dependency Diagram

```mermaid
graph TD
    Messages["<strong>Messages</strong>"]
    Localization["Localization"]
    Messages --> Localization
    Configuration["Configuration"]
    Configuration -.-> Messages
    Reporting["Reporting"]
    Reporting -.-> Messages
    BusinessEntities["BusinessEntities"]
    BusinessEntities -.-> Messages
    Coinbase["Coinbase"]
    Coinbase -.-> Messages
    Bitexbook["Bitexbook"]
    Bitexbook -.-> Messages
    Tinkoff["Tinkoff"]
    Tinkoff -.-> Messages
    BitStamp["BitStamp"]
    BitStamp -.-> Messages
    Bitalong["Bitalong"]
    Bitalong -.-> Messages
    Btce["Btce"]
    Btce -.-> Messages
    FTX["FTX"]
    FTX -.-> Messages
```

## Project References
- Localization

## Consumed By
- Configuration
- Reporting
- BusinessEntities
- Coinbase
- Bitexbook
- Tinkoff
- BitStamp
- Bitalong
- Btce
- FTX

## Internal NuGet Packages
| Package | Version |
|---------|---------|
| Ecng.Logging | 1.0.* |
| Ecng.Linq | 1.0.* |

## Data Access Patterns
### Redis.Write
| File | Line | Context |
|------|------|---------||
| `Messages/WorkingTimePeriod.cs` | 92 | `.Set("Day", p.Key)` |
| `Messages/WorkingTimePeriod.cs` | 93 | `.Set("Periods", p.Value.Select(r => r.ToStorage()).ToArray())` |
| `Messages/MessageAdapter.cs` | 812 | `.Set(nameof(Id), Id)` |
| `Messages/MessageAdapter.cs` | 813 | `.Set(nameof(HeartbeatInterval), HeartbeatInterval)` |
| `Messages/MessageAdapter.cs` | 814 | `.Set(nameof(SupportedInMessages), Do.Invariant(() => SupportedInMessag` |
| `Messages/MessageAdapter.cs` | 815 | `.Set(nameof(ReConnectionSettings), ReConnectionSettings.Save())` |
| `Messages/MessageAdapter.cs` | 816 | `.Set(nameof(EnqueueSubscriptions), EnqueueSubscriptions)` |
| `Messages/MessageAdapter.cs` | 817 | `.Set(nameof(IterationInterval), IterationInterval)` |
| `Messages/MessageAdapter.cs` | 818 | `.Set(nameof(MaxParallelMessages), MaxParallelMessages)` |
| `Messages/MessageAdapter.cs` | 819 | `.Set(nameof(FaultDelay), FaultDelay)` |
| `Messages/AsyncMessageChannel.cs` | 102 | `_processMessageEvt.Set();` |
| `Messages/AsyncMessageChannel.cs` | 179 | `_processMessageEvt.Set();` |
| `Messages/AsyncMessageChannel.cs` | 344 | `_processMessageEvt.Set();` |
| `Messages/WorkingTime.cs` | 169 | `.Set("Day", p.Key)` |
| `Messages/WorkingTime.cs` | 170 | `.Set("Periods", p.Value.Select(p1 => p1.ToStorage()).ToArray())` |

### IMessageAdapter
| File | Line | Context |
|------|------|---------||
| `Messages/ChannelMessageAdapter.cs` | 6 | `public class ChannelMessageAdapter : MessageAdapterWrapper` |
| `Messages/MessageAdapter.cs` | 8 | `public abstract partial class MessageAdapter : BaseLogReceiver, IMessa` |
| `Messages/IMessageAdapterWrapper.cs` | 6 | `public interface IMessageAdapterWrapper : IMessageAdapter` |
| `Messages/Extensions.cs` | 1521 | `where TAdapter : IMessageAdapter` |
| `Messages/Extensions.cs` | 1541 | `where TAdapter : IMessageAdapter` |
| `Messages/HistoricalMessageAdapter.cs` | 10 | `public abstract class HistoricalMessageAdapter(IdGenerator transaction` |


---

*[Back to Index](../index.md)*
