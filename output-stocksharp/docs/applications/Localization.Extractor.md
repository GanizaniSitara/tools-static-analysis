# Localization.Extractor

## Overview

| Property | Value |
|----------|-------|
| Category | Tool |
| Repository | StockSharp |
| Path | `Localization.Extractor/Localization.Extractor.csproj` |
| Project References | 0 |
| NuGet Dependencies | 2 |
| Consumers | 0 |

## External NuGet Packages
| Package | Version |
|---------|---------||
| Spectre.Console.Cli | 0.48.0 |

## Internal NuGet Packages
| Package | Version |
|---------|---------|
| Ecng.Serialization | 1.0.* |

## Data Access Patterns
### File.Read
| File | Line | Context |
|------|------|---------||
| `Localization.Extractor/Program.cs` | 72 | `var strings = File.ReadAllText(file).DeserializeObject<IDictionary<str` |
| `Localization.Extractor/Program.cs` | 109 | `var translates = File.ReadAllText(settings.JsonFile).DeserializeObject` |
| `Localization.Extractor/Program.cs` | 118 | `strings.AddRange(File.ReadAllText(langFile).DeserializeObject<IDiction` |
| `Localization.Extractor/Program.cs` | 141 | `var lines = File.ReadAllText($@"{_locPath}{_stringsFile}").Deserialize` |
| `Localization.Extractor/Program.cs` | 147 | `var strings = File.ReadAllText(file).DeserializeObject<IDictionary<str` |
| `Localization.Extractor/Program.cs` | 202 | `var dict = File.ReadAllText(file).DeserializeObject<IDictionary<string` |

### File.Write
| File | Line | Context |
|------|------|---------||
| `Localization.Extractor/Program.cs` | 74 | `File.WriteAllText(file, ordered.ToJson());` |
| `Localization.Extractor/Program.cs` | 122 | `File.WriteAllText(langFile, strings.ToJson());` |
| `Localization.Extractor/Program.cs` | 222 | `File.WriteAllText(file, ordered.ToJson());` |


---

*[Back to Index](../index.md)*
