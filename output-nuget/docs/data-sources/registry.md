# Data Source Registry

## Summary

| Type | Occurrences |
|------|-------------|
| storage | 1472 |
| cache | 912 |
| database | 526 |
| ui | 92 |
| pattern | 47 |
| api | 32 |
| messaging | 13 |
| connector | 11 |

## Connection Strings Found

| File | Repo | Connection Name | Value |
|------|------|----------------|-------|
| `test/EndToEnd/ProjectTemplates/WebApplicationProject40.zip/Web.config` | NuGet.Client | ApplicationServices | `data source=.\SQLEXPRESS;Integrated Security=SSPI;AttachDBFilename=\|DataDirector` |

## Storage

### File.Write (941 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetPackageUpdateTests.cs` | 63 | `File.WriteAllText(testContext.NuGetConfig, string.Format(Nug` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetPackageUpdateTests.cs` | 82 | `File.WriteAllText(csprojPath, csprojContents);` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetPackageUpdateTests.cs` | 103 | `File.WriteAllText(testContext.NuGetConfig, string.Format(Nug` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetPackageUpdateTests.cs` | 122 | `File.WriteAllText(csprojPath, csprojContents);` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetPackageUpdateTests.cs` | 135 | `File.WriteAllText(packagesPropsPath, packagesPropsContents);` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetPackageUpdateTests.cs` | 159 | `File.WriteAllText(testContext.NuGetConfig, string.Format(Nug` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetPackageUpdateTests.cs` | 178 | `File.WriteAllText(csprojPath, csprojContents);` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetPackageUpdateTests.cs` | 199 | `File.WriteAllText(testContext.NuGetConfig, string.Format(Nug` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetPackageUpdateTests.cs` | 218 | `File.WriteAllText(csprojPath, csprojContents);` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetPackageUpdateTests.cs` | 242 | `File.WriteAllText(testContext.NuGetConfig, string.Format(Nug` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetPackageUpdateTests.cs` | 261 | `File.WriteAllText(csprojPath, csprojContents);` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetPackageUpdateTests.cs` | 287 | `File.WriteAllText(csprojPath, csprojContents);` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetPackageUpdateTests.cs` | 307 | `File.WriteAllText(testContext.NuGetConfig, string.Format(Nug` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 275 | `File.WriteAllText(Path.Combine(projectADirectory, "NuGet.Con` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 338 | `File.WriteAllText(Path.Combine(projectADirectory, "NuGet.Con` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 403 | `File.WriteAllText(Path.Combine(projectADirectory, "NuGet.Con` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 467 | `File.WriteAllText(Path.Combine(projectADirectory, "NuGet.Con` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 535 | `File.WriteAllText(Path.Combine(projectADirectory, "NuGet.Con` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 598 | `File.WriteAllText(Path.Combine(projectADirectory, "NuGet.Con` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 713 | `File.WriteAllText(Path.Combine(pathContext.SolutionRoot, "Di` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 762 | `File.WriteAllText(Path.Combine(pathContext.SolutionRoot, "Di` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 809 | `File.WriteAllText(Path.Combine(pathContext.SolutionRoot, "Di` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 860 | `File.WriteAllText(Path.Combine(pathContext.SolutionRoot, "Di` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 912 | `File.WriteAllText(Path.Combine(pathContext.SolutionRoot, "Di` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 966 | `File.WriteAllText(Path.Combine(pathContext.SolutionRoot, "Di` |

*... and 916 more*

**Repos:** NuGet.Client

### File.Read (531 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/SignCommandTestFixture.cs` | 331 | `var content = File.ReadAllBytes(crlPath);` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 723 | `</ItemGroup", File.ReadAllText(Path.Combine(pathContext.Solu` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 725 | `File.ReadAllText(Path.Combine(projectADirectory, "projectA.c` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 771 | `</ItemGroup", File.ReadAllText(Path.Combine(pathContext.Solu` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 773 | `File.ReadAllText(Path.Combine(projectADirectory, "projectA.c` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 818 | `Assert.Contains(@$"<PackageVersion Include=""X"" Version=""1` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 820 | `var projectFileFromDisk = File.ReadAllText(Path.Combine(proj` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 867 | `Assert.Contains(@$"<PackageVersion Include=""X"" Version=""2` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 869 | `var projectFileFromDisk = File.ReadAllText(Path.Combine(proj` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 872 | `Assert.Contains(@$"Include=""X""", File.ReadAllText(Path.Com` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 919 | `var propsFileFromDisk = File.ReadAllText(Path.Combine(pathCo` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 988 | `</ItemGroup>", File.ReadAllText(Path.Combine(pathContext.Sol` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 991 | `</ItemGroup>", File.ReadAllText(Path.Combine(projectADirecto` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 1050 | `</ItemGroup>", File.ReadAllText(Path.Combine(pathContext.Sol` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 1053 | `</ItemGroup>", File.ReadAllText(Path.Combine(projectADirecto` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 1115 | `var csprojFromDisk = File.ReadAllText(Path.Combine(projectAD` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 1119 | `var assetsFromDisk = File.ReadAllText(Path.Combine(projectAD` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 1182 | `</ItemGroup>", File.ReadAllText(Path.Combine(pathContext.Sol` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 1185 | `</ItemGroup>", File.ReadAllText(Path.Combine(projectADirecto` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 1246 | `</ItemGroup>", File.ReadAllText(Path.Combine(pathContext.Sol` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 1305 | `</ItemGroup>", File.ReadAllText(Path.Combine(pathContext.Sol` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 1308 | `</ItemGroup>", File.ReadAllText(Path.Combine(projectADirecto` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 1366 | `</ItemGroup>", File.ReadAllText(Path.Combine(pathContext.Sol` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 1369 | `</ItemGroup>", File.ReadAllText(Path.Combine(projectADirecto` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetAddPackageTests.cs` | 1431 | `</ItemGroup>", File.ReadAllText(Path.Combine(pathContext.Sol` |

*... and 506 more*

**Repos:** NuGet.Client

## Cache

### Redis.Read (817 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 87 | `doc.Root.Add(new XElement(XName.Get("Target"),` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 88 | `new XAttribute(XName.Get("Name"), "ErrorOnSolutionDir"),` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 89 | `new XAttribute(XName.Get("BeforeTargets"), "CollectPackageRe` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 90 | `new XElement(XName.Get("Error"),` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 91 | `new XAttribute(XName.Get("Text"), $"\|SOLUTION $(SolutionDir)` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 241 | `var configuration = new XElement(XName.Get("configuration"))` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 244 | `var config = new XElement(XName.Get("config"));` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 247 | `var updatePackageLastAccessTime = new XElement(XName.Get("ad` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 248 | `updatePackageLastAccessTime.Add(new XAttribute(XName.Get("ke` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 249 | `updatePackageLastAccessTime.Add(new XAttribute(XName.Get("va` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 322 | `var configuration = new XElement(XName.Get("configuration"))` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 325 | `var config = new XElement(XName.Get("config"));` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 328 | `var signatureValidationMode = new XElement(XName.Get("add"))` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 329 | `signatureValidationMode.Add(new XAttribute(XName.Get("key"),` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 330 | `signatureValidationMode.Add(new XAttribute(XName.Get("value"` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 393 | `var configuration = new XElement(XName.Get("configuration"))` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 396 | `var config = new XElement(XName.Get("config"));` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 399 | `var signatureValidationMode = new XElement(XName.Get("add"))` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 400 | `signatureValidationMode.Add(new XAttribute(XName.Get("key"),` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 401 | `signatureValidationMode.Add(new XAttribute(XName.Get("value"` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 468 | `var configuration = new XElement(XName.Get("configuration"))` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 471 | `var config = new XElement(XName.Get("config"));` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 474 | `var signatureValidationMode = new XElement(XName.Get("add"))` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 475 | `signatureValidationMode.Add(new XAttribute(XName.Get("key"),` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 476 | `signatureValidationMode.Add(new XAttribute(XName.Get("value"` |

*... and 792 more*

**Repos:** NuGet.Client

### Redis.Write (95 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.Protocol.FuncTest/PluginTests.cs` | 246 | `closedEvent.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Common.Test/ConcurrencyUtilitiesTests.cs` | 145 | `action1HitSem.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Common.Test/ConcurrencyUtilitiesTests.cs` | 152 | `action2Sem.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Common.Test/ConcurrencyUtilitiesTests.cs` | 174 | `action1Sem.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Common.Test/ConcurrencyUtilitiesTests.cs` | 197 | `action1HitSem.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Common.Test/ConcurrencyUtilitiesTests.cs` | 204 | `action2Sem.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Common.Test/ConcurrencyUtilitiesTests.cs` | 226 | `action1Sem.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Packaging.Test/PackageExtractorTests.cs` | 112 | `sem.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Plugins/InboundRequestContextTests.cs` | 143 | `handledEvent.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Plugins/InboundRequestContextTests.cs` | 224 | `sentEvent.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Plugins/InboundRequestContextTests.cs` | 322 | `handledEvent.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Plugins/InboundRequestContextTests.cs` | 368 | `sentEvent.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Plugins/OutboundRequestContextTests.cs` | 98 | `cancelEvent.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Plugins/AutomaticProgressReporterTests.cs` | 182 | `SentEvent.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Plugins/StandardOutputReceiverTests.cs` | 104 | `receivedEvent.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Plugins/StandardOutputReceiverTests.cs` | 148 | `receivedEvent.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Plugins/StandardOutputReceiverTests.cs` | 182 | `faultedEvent.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Plugins/StandardOutputReceiverTests.cs` | 215 | `faultedEvent.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Plugins/StandardOutputReceiverTests.cs` | 248 | `faultedEvent.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Plugins/StandardOutputReceiverTests.cs` | 291 | `faultedEvent.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Plugins/InboundRequestProcessingHandlerTests.cs` | 45 | `Func<Task> task = () => { executed = true; handledEvent.Set(` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Plugins/InboundRequestProcessingHandlerTests.cs` | 61 | `Func<Task> task = () => { executed = true; handledEvent.Set(` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Plugins/InboundRequestProcessingHandlerTests.cs` | 77 | `Func<Task> task = () => { executed = true; handledEvent.Set(` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Plugins/PluginProcessTests.cs` | 38 | `exitedEvent.Set();` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Plugins/PluginProcessTests.cs` | 113 | `exitedEvent.Set();` |

*... and 70 more*

**Repos:** NuGet.Client

## Database

### Dapper.Execute (498 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.Protocol.FuncTest/AuthenticationHandlerTests.cs` | 37 | `await portReserver.ExecuteAsync(async (port, cancellationTok` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.Protocol.FuncTest/AuthenticationHandlerTests.cs` | 104 | `await portReserver.ExecuteAsync(async (port, cancellationTok` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.Protocol.FuncTest/HttpRetryHandlerTests.cs` | 284 | `return await server.ExecuteAsync(async address =>` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XPlatTrustTests.cs` | 122 | `int result = testApp.Execute(argList.ToArray());` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XPlatVerifyTests.cs` | 37 | `var ex = Assert.Throws<AggregateException>(() => testApp.Exe` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XPlatVerifyTests.cs` | 59 | `Assert.Throws<CommandParsingException>(() => testApp.Execute` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XPlatVerifyTests.cs` | 84 | `var result = testApp.Execute(argList.ToArray());` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XplatSignTests.cs` | 44 | `var ex = Assert.Throws<AggregateException>(() => testApp.Exe` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XplatSignTests.cs` | 72 | `var ex = Assert.Throws<AggregateException>(() => testApp.Exe` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XplatSignTests.cs` | 106 | `testApp.Execute(argList.ToArray());` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XplatSignTests.cs` | 131 | `var ex = Assert.Throws<AggregateException>(() => testApp.Exe` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XplatSignTests.cs` | 162 | `testApp.Execute(argList.ToArray());` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XplatSignTests.cs` | 188 | `var ex = Assert.Throws<AggregateException>(() => testApp.Exe` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XplatSignTests.cs` | 221 | `testApp.Execute(argList.ToArray());` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XplatSignTests.cs` | 247 | `var ex = Assert.Throws<AggregateException>(() => testApp.Exe` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XplatSignTests.cs` | 278 | `testApp.Execute(argList.ToArray());` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XplatSignTests.cs` | 304 | `var ex = Assert.Throws<AggregateException>(() => testApp.Exe` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XplatSignTests.cs` | 338 | `testApp.Execute(argList.ToArray());` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XplatSignTests.cs` | 381 | `testApp.Execute(argList.ToArray());` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XplatSignTests.cs` | 423 | `testApp.Execute(argList.ToArray());` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XplatSignTests.cs` | 457 | `var ex = Assert.Throws<AggregateException>(() => testApp.Exe` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XplatSignTests.cs` | 481 | `testApp.Execute(argList.ToArray());` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/ListPackageTests.cs` | 55 | `var result = testApp.Execute(argList.ToArray());` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/ListPackageTests.cs` | 74 | `Assert.Throws<CommandParsingException>(() => testApp.Execute` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/ListPackageTests.cs` | 99 | `var result = testApp.Execute(argList.ToArray());` |

*... and 473 more*

**Repos:** NuGet.Client

### MongoDB.Read (19 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/XPlatClientCertTests.cs` | 1020 | `X509Certificate2Collection resultCertificates = store.Certif` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Configuration.Test/ClientCertificateProviderTests.cs` | 170 | `X509Certificate2Collection resultCertificates = store.Certif` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.CommandLine.Test/NuGetClientCertCommandTests.cs` | 1006 | `X509Certificate2Collection resultCertificates = store.Certif` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.Indexing.Test/SearchResultsAggregatorTests.cs` | 46 | `var results = await aggregator.AggregateAsync(queryString, r` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.Indexing.Test/SearchResultsAggregatorTests.cs` | 66 | `var results = await aggregator.AggregateAsync(queryString, r` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.Indexing.Test/SearchResultsAggregatorTests.cs` | 84 | `var results = await aggregator.AggregateAsync(queryString, r` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.VisualStudio.Common.Test/Telemetry/PackageSourceTelemetryTests.cs` | 117 | `Assert.Equal(timings.Aggregate(TimeSpan.Zero, (a, b) => a + ` |
| NuGet.Client | `src/NuGet.Clients/NuGet.MSSigning.Extensions/MSSignAbstract.cs` | 99 | `matchingCertCollection = certCollection.Find(X509FindType.Fi` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.VisualStudio/PackageFeeds/MultiSourcePackageFeed.cs` | 273 | `var loadingStatus = aggregated.SourceSearchStatus.Values.Agg` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.VisualStudio/PackageFeeds/MultiSourcePackageFeed.cs` | 334 | `var aggregatedItems = await aggregator.AggregateAsync(` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.VisualStudio/PackageFeeds/MultiSourcePackageFeed.cs` | 339 | `result.RawItemsCount = items.Aggregate(0, (r, next) => r + n` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/PackageItemLoader.cs` | 397 | `return SourceLoadingStatus.Values.Aggregate();` |
| NuGet.Client | `src/NuGet.Core/NuGet.PackageManagement/FileModifiers/XmlTransformer.cs` | 134 | `var mergedFragments = elements.Aggregate(` |
| NuGet.Client | `src/NuGet.Core/NuGet.Commands/SignCommand/CertificateProvider.cs` | 196 | `resultCollection = store.Certificates.Find(X509FindType.Find` |
| NuGet.Client | `src/NuGet.Core/NuGet.Commands/SignCommand/CertificateProvider.cs` | 215 | `resultCollection = store.Certificates.Find(X509FindType.Find` |
| NuGet.Client | `src/NuGet.Core/NuGet.Frameworks/CompatibilityListProvider.cs` | 46 | `.Select(g => g.Aggregate((a, b) => a.Version < b.Version ? a` |
| NuGet.Client | `src/NuGet.Core/NuGet.Protocol/LegacyFeed/V2FeedQueryBuilder.cs` | 237 | `.Aggregate((a, b) => string.Format(CultureInfo.InvariantCult` |
| NuGet.Client | `src/NuGet.Core/NuGet.Protocol/LegacyFeed/V2FeedQueryBuilder.cs` | 305 | `.Aggregate((a, b) => string.Format(CultureInfo.InvariantCult` |
| NuGet.Client | `src/NuGet.Core/NuGet.Configuration/Settings/Items/StoreClientCertItem.cs` | 243 | `X509Certificate2Collection foundCertificates = store.Certifi` |

**Repos:** NuGet.Client

### SqlClient (6 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Resolver.Test/ResolverData.cs` | 250 | `new NuGet.Packaging.Core.PackageDependency("System.Data.SqlC` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Resolver.Test/ResolverData.cs` | 258 | `new NuGet.Packaging.Core.PackageDependency("System.Data.SqlC` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Resolver.Test/ResolverData.cs` | 971 | `packages.Add(new ResolverPackage("System.Data.SqlClient", Nu` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Resolver.Test/ResolverData.cs` | 972 | `packages.Add(new ResolverPackage("System.Data.SqlClient", Nu` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Resolver.Test/ResolverData.cs` | 975 | `packages.Add(new ResolverPackage("System.Data.SqlClient", Nu` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Resolver.Test/ResolverData.cs` | 976 | `packages.Add(new ResolverPackage("System.Data.SqlClient", Nu` |

**Repos:** NuGet.Client

### SQL.Select (2 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 512 | `//Select a different VM which should clear the Versions list` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 1653 | `//Select a different VM which should clear the Versions list` |

**Repos:** NuGet.Client

### SQL.Delete (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `src/NuGet.Clients/NuGet.CommandLine/NuGetCommand.Designer.cs` | 417 | `///   Looks up a localized string similar to Specify the Id ` |

**Repos:** NuGet.Client

## Ui

### WPF.ViewModel (51 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 525 | `private ItemsChangeObservableCollection<DisplayVersion> Vers` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 527 | `return new ItemsChangeObservableCollection<DisplayVersion>()` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 540 | `private ItemsChangeObservableCollection<DisplayVersion> Vers` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 542 | `return new ItemsChangeObservableCollection<DisplayVersion>()` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 554 | `private ItemsChangeObservableCollection<DisplayVersion> Vers` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 556 | `return new ItemsChangeObservableCollection<DisplayVersion>()` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 571 | `private ItemsChangeObservableCollection<DisplayVersion> Vers` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 573 | `return new ItemsChangeObservableCollection<DisplayVersion>()` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 587 | `private ItemsChangeObservableCollection<DisplayVersion> Vers` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 589 | `return new ItemsChangeObservableCollection<DisplayVersion>()` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 731 | `ItemsChangeObservableCollection<DisplayVersion> assertVersio` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 843 | `ItemsChangeObservableCollection<DisplayVersion> assertVersio` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 968 | `ItemsChangeObservableCollection<DisplayVersion> assertVersio` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 1014 | `private ItemsChangeObservableCollection<DisplayVersion> Vers` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 1016 | `return new ItemsChangeObservableCollection<DisplayVersion>()` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 1026 | `private ItemsChangeObservableCollection<DisplayVersion> Vers` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 1028 | `return new ItemsChangeObservableCollection<DisplayVersion>()` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 1040 | `private ItemsChangeObservableCollection<DisplayVersion> Vers` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 1042 | `return new ItemsChangeObservableCollection<DisplayVersion>()` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 1056 | `private ItemsChangeObservableCollection<DisplayVersion> Vers` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 1058 | `return new ItemsChangeObservableCollection<DisplayVersion>()` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 1071 | `private ItemsChangeObservableCollection<DisplayVersion> Vers` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 1073 | `return new ItemsChangeObservableCollection<DisplayVersion>()` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 1175 | `ItemsChangeObservableCollection<DisplayVersion> assertVersio` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.UI.Test/Models/V3DetailControlModelTests.cs` | 1281 | `ItemsChangeObservableCollection<DisplayVersion> assertVersio` |

*... and 26 more*

**Repos:** NuGet.Client

### WPF.Window (24 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `test/EndToEnd/ProjectTemplates/WPFApplication.zip/MainWindow.xaml.cs` | 20 | `public partial class $safeitemrootname$ : Window` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/SolutionView.xaml.cs` | 28 | `public partial class SolutionView : UserControl` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/ProductUpdateBar.xaml.cs` | 13 | `public partial class ProductUpdateBar : UserControl` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/Spinner.xaml.cs` | 75 | `internal partial class Spinner : UserControl` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/InfiniteScrollList.xaml.cs` | 35 | `public partial class InfiniteScrollList : UserControl` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/PackageManagerTopPanel.xaml.cs` | 21 | `public partial class PackageManagerTopPanel : UserControl` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/PackageItemControl.xaml.cs` | 16 | `public partial class PackageItemControl : UserControl` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/AuthorAndDownloadCount.xaml.cs` | 23 | `public partial class AuthorAndDownloadCount : UserControl, I` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/ProjectView.xaml.cs` | 19 | `public partial class ProjectView : UserControl` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/PackageSourceMappingActionControl.xaml.cs` | 13 | `public partial class PackageSourceMappingActionControl : Use` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/DeprecationControl.xaml.cs` | 11 | `public partial class DeprecationControl : UserControl` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/PackageMetadataControl.xaml.cs` | 21 | `public partial class PackageMetadataControl : UserControl` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/LoadingStatusBar.xaml.cs` | 12 | `internal partial class LoadingStatusBar : UserControl` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/PRMigratorBar.xaml.cs` | 27 | `public partial class PRMigratorBar : UserControl, INuGetProj` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/OptionsControl.xaml.cs` | 13 | `public partial class OptionsControl : UserControl` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/DetailControl.xaml.cs` | 25 | `public partial class DetailControl : UserControl` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/PackageDetailsTabControl.xaml.cs` | 16 | `public partial class PackageDetailsTabControl : UserControl,` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/PackageManagerControl.xaml.cs` | 46 | `public partial class PackageManagerControl : UserControl, IV` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/RestartRequestBar.xaml.cs` | 26 | `public partial class RestartRequestBar : UserControl, INuGet` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/PackageRestoreBar.xaml.cs` | 38 | `public partial class PackageRestoreBar : UserControl, INuGet` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/PackageItemDeprecationLabel.xaml.cs` | 16 | `public partial class PackageItemDeprecationLabel : UserContr` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/VulnerabilitiesControl.xaml.cs` | 11 | `public partial class VulnerabilitiesControl : UserControl` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/PackageReadmeControl.xaml.cs` | 25 | `public partial class PackageReadmeControl : UserControl, IDi` |
| NuGet.Client | `src/NuGet.Clients/NuGet.Console/Xamls/ConsoleContainer.xaml.cs` | 28 | `public sealed partial class ConsoleContainer : UserControl, ` |

**Repos:** NuGet.Client

### WPF.Binding (17 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/UserInterfaceService/NuGetUI.cs` | 174 | `DataContext = dataContext` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/UserInterfaceService/NuGetUI.cs` | 195 | `DataContext = packages` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/UserInterfaceService/NuGetUI.cs` | 214 | `packageFormatWindow.DataContext = selectedFormat;` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/UserInterfaceService/NuGetUI.cs` | 327 | `w.DataContext = new PreviewWindowModel(actions);` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/InfiniteScrollList.xaml.cs` | 104 | `DataContext = itemsView;` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/NuGetProjectUpgradeWindow.xaml.cs` | 22 | `DataContext = model;` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/LicenseAcceptanceWindow.xaml.cs` | 45 | `DataContext = licenseFile` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/PackageMetadataControl.xaml.cs` | 43 | `DataContext = new LicenseFileData` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/ClearNuGetLocalResourcesWindow.xaml.cs` | 19 | `DataContext = viewModel;` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/LoadingStatusBar.xaml.cs` | 82 | `DataContext = new LoadingStatusViewModel` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/LoadingStatusBar.xaml.cs` | 91 | `DataContext = new LoadingStatusViewModel` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/LoadingStatusBar.xaml.cs` | 99 | `DataContext = new LoadingStatusViewModel` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/LicenseFileWindow.xaml.cs` | 23 | `DataContext = null;` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/PackageDetailsTabControl.xaml.cs` | 28 | `DataContext = new PackageDetailsTabViewModel();` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/PackageManagerControl.xaml.cs` | 1167 | `_packageDetail.DataContext = _detailModel;` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/PackageManagerControl.xaml.cs` | 1269 | `_topPanel.SourceToolTip.DataContext = SelectedSource.GetTool` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Xamls/PackageRestoreBar.xaml.cs` | 79 | `DataContext = this;` |

**Repos:** NuGet.Client

## Pattern

### Repository (47 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.Packaging.FuncTest/SigningTests/RepositoryCountersignatureTests.cs` | 23 | `public class RepositoryCountersignatureTests` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.Packaging.FuncTest/SigningTests/SignatureTrustAndValidityVerificationProviderTests.cs` | 841 | `public class RepositoryPrimarySignatures` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.Packaging.FuncTest/SigningTests/SignatureTrustAndValidityVerificationProviderTests.cs` | 1169 | `public class RepositoryCountersignatures` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.Protocol.FuncTest/Helpers/MockSourceRepository.cs` | 12 | `internal class MockSourceRepository` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.PackageManagement.Test/SourceRepositoryProviderTests.cs` | 12 | `public class SourceRepositoryProviderTests` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Commands.Test/SourceRepositoryDependencyProviderTests.cs` | 29 | `public class SourceRepositoryDependencyProviderTests` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Commands.Test/SourceRepositoryDependencyProviderTests.cs` | 954 | `private sealed class SourceRepositoryDependencyProviderTest ` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Packaging.Test/SigningTests/RepositorySignatureInfoUtilityTests.cs` | 16 | `public class RepositorySignatureInfoUtilityTests` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Packaging.Test/SigningTests/RepositoryCountersignatureTests.cs` | 17 | `public class RepositoryCountersignatureTests` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Packaging.Test/SigningTests/RepositorySignPackageRequestTests.cs` | 16 | `public class RepositorySignPackageRequestTests` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Packaging.Test/RepositoryMetadataTests.cs` | 11 | `public class RepositoryMetadataTests` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/NuGetv3LocalRepositoryTests.cs` | 23 | `public class NuGetv3LocalRepositoryTests` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/RepositoryTests.cs` | 12 | `public class RepositoryTests` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Providers/RepositorySignatureResourceProviderTests.cs` | 25 | `public class RepositorySignatureResourceProviderTests` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/Resources/RepositorySignatureResourceTests.cs` | 21 | `public class RepositorySignatureResourceTests` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Configuration.Test/SettingsFileParsingTests/RepositoryItemTests.cs` | 14 | `public class RepositoryItemTests` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.VisualStudio.Test/Feeds/SourceRepositoryCreator.cs` | 22 | `public abstract class SourceRepositoryCreator` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.VisualStudio.Test/Feeds/SourceRepositoryExtensionsTests.cs` | 14 | `public class SourceRepositoryExtensionsTests : SourceReposit` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.VisualStudio.Implementation.Test/PreinstalledRepositoryProviderTests.cs` | 18 | `public class PreinstalledRepositoryProviderTests : IDisposab` |
| NuGet.Client | `test/TestUtilities/Microsoft.Internal.NuGet.Testing.SignedPackages/TestRepositoryCertificateInfo.cs` | 13 | `public class TestRepositoryCertificateInfo : IRepositoryCert` |
| NuGet.Client | `test/TestUtilities/Test.Utility/SourceRepository/TestSourceRepositoryUtility.cs` | 17 | `public class TestSourceRepositoryUtility` |
| NuGet.Client | `test/NuGet.Tests.Apex/NuGet.Tests.Apex/NuGetPackageSigningTests/RepositorySignedPackageTestCase.cs` | 19 | `public class RepositorySignedPackageTestCase : SharedVisualS` |
| NuGet.Client | `test/NuGet.Tests.Apex/NuGet.Tests.Apex/NuGetPackageSigningTests/RepositoryCountersignedPackageTestCase.cs` | 20 | `public class RepositoryCountersignedPackageTestCase : Shared` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.VisualStudio/PackageFeeds/SourceRepositoryExtensions.cs` | 24 | `internal static class SourceRepositoryExtensions` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.VisualStudio/IDE/ExtensibleSourceRepositoryProvider.cs` | 22 | `public sealed class ExtensibleSourceRepositoryProvider : ISo` |

*... and 22 more*

**Repos:** NuGet.Client

## Api

### HttpClient.New (29 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.Protocol.FuncTest/HttpRetryHandlerTests.cs` | 35 | `using (var httpClient = new HttpClient())` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.Protocol.FuncTest/HttpRetryHandlerTests.cs` | 82 | `var httpClient = new HttpClient(testHandler);` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.Protocol.FuncTest/HttpRetryHandlerTests.cs` | 201 | `var client = new HttpClient(busyServer);` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.Protocol.FuncTest/HttpRetryHandlerTests.cs` | 248 | `var client = new HttpClient(busyServer);` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.Protocol.FuncTest/HttpRetryHandlerTests.cs` | 299 | `var httpClient = new HttpClient(countingHandler);` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpHandlerResourceV3ProviderTests.cs` | 223 | `var client = new HttpClient(clientHandler);` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpHandlerResourceV3ProviderTests.cs` | 253 | `var client = new HttpClient(clientHandler);` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/HttpSourceAuthenticationHandlerTests.cs` | 362 | `using var client = new HttpClient(handler);` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/HttpSourceAuthenticationHandlerTests.cs` | 444 | `using var client = new HttpClient(handler);` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/HttpSourceAuthenticationHandlerTests.cs` | 563 | `using (var client = new HttpClient(handler))` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/HttpSourceAuthenticationHandlerTests.cs` | 922 | `using (var client = new HttpClient(handler))` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/ProxyAuthenticationHandlerTests.cs` | 282 | `using (var client = new HttpClient(handler))` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/StsAuthenticationHandlerTests.cs` | 216 | `using (var client = new HttpClient(handler))` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/HttpRetryHandlerTests.cs` | 45 | `using (var httpClient = new HttpClient(testHandler))` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/HttpRetryHandlerTests.cs` | 85 | `var httpClient = new HttpClient(testHandler);` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/HttpRetryHandlerTests.cs` | 124 | `var httpClient = new HttpClient(testHandler);` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/HttpRetryHandlerTests.cs` | 157 | `var httpClient = new HttpClient(testHandler);` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/HttpRetryHandlerTests.cs` | 192 | `var httpClient = new HttpClient(testHandler);` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/HttpRetryHandlerTests.cs` | 226 | `var httpClient = new HttpClient(testHandler);` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/HttpRetryHandlerTests.cs` | 269 | `var httpClient = new HttpClient(testHandler);` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/HttpRetryHandlerTests.cs` | 304 | `var httpClient = new HttpClient(testHandler);` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/HttpRetryHandlerTests.cs` | 339 | `var httpClient = new HttpClient(testHandler);` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/HttpRetryHandlerTests.cs` | 378 | `var httpClient = new HttpClient(testHandler);` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/HttpRetryHandlerTests.cs` | 430 | `var httpClient = new HttpClient(testHandler);` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Protocol.Tests/HttpSource/HttpRetryHandlerTests.cs` | 477 | `var httpClient = new HttpClient(testHandler);` |

*... and 4 more*

**Repos:** NuGet.Client

### HttpClient.GetAsync (2 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Packaging.Test/PackageFolderReaderTests.cs` | 187 | `using (var stream = await test.Reader.GetStreamAsync("Aa.nus` |
| NuGet.Client | `test/NuGet.Core.Tests/NuGet.Packaging.Test/PackageArchiveReaderTests.cs` | 563 | `using (var stream = await test.Reader.GetStreamAsync("Aa.nus` |

**Repos:** NuGet.Client

### API.Controller (1 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `test/EndToEnd/ProjectTemplates/NetCoreWebApplication1.0.zip/Controllers/HomeController.cs` | 9 | `public class HomeController : Controller` |

**Repos:** NuGet.Client

## Messaging

### Kafka.Consumer (13 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.VisualStudio.Common.Test/ErrorListTableDataSourceTests.cs` | 204 | `var subscription = source.Subscribe(sink);` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.VisualStudio.Common.Test/ErrorListTableDataSourceTests.cs` | 253 | `var subscription = source.Subscribe(sink);` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.VisualStudio.Common.Test/ErrorListTableDataSourceTests.cs` | 295 | `var subscription = source.Subscribe(null);` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.VisualStudio.Common.Test/ErrorListTableDataSourceTests.cs` | 367 | `var s1 = source.Subscribe(sink);` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.VisualStudio.Common.Test/ErrorListTableDataSourceTests.cs` | 368 | `var s2 = source.Subscribe(sink2);` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.VisualStudio.Common.Test/ErrorListTableDataSourceTests.cs` | 369 | `var s3 = source.Subscribe(sink3);` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.VisualStudio.Common.Test/ErrorListTableDataSourceTests.cs` | 458 | `var s1 = source.Subscribe(sink);` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.VisualStudio.Common.Test/ErrorListTableDataSourceTests.cs` | 459 | `var s2 = source.Subscribe(sink2);` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.VisualStudio.Common.Test/ErrorListTableDataSourceTests.cs` | 460 | `var s3 = source.Subscribe(sink3);` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.VisualStudio.Common.Test/ErrorListTableDataSourceTests.cs` | 535 | `var s1 = source.Subscribe(sink);` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.VisualStudio.Common.Test/ErrorListTableDataSourceTests.cs` | 540 | `var s2 = source.Subscribe(sink2);` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.VisualStudio.Common.Test/ErrorListTableDataSourceTests.cs` | 606 | `var s1 = source.Subscribe(sink);` |
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.VisualStudio.Common.Test/ErrorListTableDataSourceTests.cs` | 607 | `var s2 = source.Subscribe(sink2);` |

**Repos:** NuGet.Client

## Connector

### IMessageAdapter (11 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `test/NuGet.Clients.Tests/NuGet.PackageManagement.VisualStudio.Test/ProjectSystems/TestVSProjectAdapter.cs` | 21 | `internal class TestVSProjectAdapter : IVsProjectAdapter` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.VisualStudio/VsCredentialProviderAdapter.cs` | 19 | `public class VsCredentialProviderAdapter : ICredentialProvid` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.VisualStudio/Projects/VsProjectAdapter.cs` | 24 | `internal class VsProjectAdapter : IVsProjectAdapter` |
| NuGet.Client | `src/NuGet.Clients/NuGet.CommandLine/Credentials/CredentialServiceAdapter.cs` | 18 | `public class CredentialServiceAdapter : CoreV2.NuGet.ICreden` |
| NuGet.Client | `src/NuGet.Clients/NuGet.CommandLine/Credentials/CredentialProviderAdapter.cs` | 16 | `public class CredentialProviderAdapter : ICredentialProvider` |
| NuGet.Client | `src/NuGet.Clients/NuGet.PackageManagement.UI/Models/Package/PackageMetadataRetrievalAdapter.cs` | 13 | `internal class PackageMetadataRetrievalAdapter : IPackageMet` |
| NuGet.Client | `src/NuGet.Core/NuGet.PackageManagement/LoggerAdapter.cs` | 15 | `public class LoggerAdapter : LegacyLoggerAdapter, ILogger` |
| NuGet.Client | `src/NuGet.Core/NuGet.Build.Tasks.Console/RestoreProjectAdapter.cs` | 14 | `internal class RestoreProjectAdapter : IProject` |
| NuGet.Client | `src/NuGet.Core/NuGet.Build.Tasks.Console/TargetFrameworkAdapter.cs` | 12 | `internal class TargetFrameworkAdapter : ITargetFramework` |
| NuGet.Client | `src/NuGet.Core/NuGet.Build.Tasks.Console/ItemAdapter.cs` | 11 | `internal class ItemAdapter : IItem` |
| NuGet.Client | `src/NuGet.Core/NuGet.Common/Logging/LegacyLoggerAdapter.cs` | 13 | `public abstract class LegacyLoggerAdapter : ILogger` |

**Repos:** NuGet.Client


---

*[Back to Index](../index.md)*
