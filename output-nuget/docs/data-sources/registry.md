# Data Source Registry

## Summary

| Type | Occurrences |
|------|-------------|
| storage | 210 |
| database | 156 |
| pattern | 47 |
| api | 29 |
| connector | 11 |

## Connection Strings Found

| File | Repo | Connection Name | Value |
|------|------|----------------|-------|
| `test/EndToEnd/ProjectTemplates/WebApplicationProject40.zip/Web.config` | NuGet.Client | ApplicationServices | `data source=.\SQLEXPRESS;Integrated Security=SSPI;AttachDBFilename=\|DataDirector` |

## Storage

### FileStorage (210 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/PackCommandTests.cs` | 5590 | `using (var stream = File.Create(projectFile))` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/PackCommandTests.cs` | 5641 | `using (var stream = File.Create(projectFile))` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/PackCommandTests.cs` | 6205 | `using (var stream = File.Open(projectFile, FileMode.Open, Fi` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/PackCommandTests.cs` | 6279 | `using (var stream = File.Open(projectFile, FileMode.Open, Fi` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/PackCommandTests.cs` | 6347 | `using (var stream = File.Open(projectFile, FileMode.Open, Fi` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 118 | `using (var stream = File.Open(projectFile, FileMode.Open, Fi` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 157 | `using (FileStream stream = File.Open(projectFile, FileMode.O` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 220 | `using (var stream = File.Open(projectFile, FileMode.Open, Fi` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 303 | `using (var stream = File.Open(projectFile, FileMode.Open, Fi` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 374 | `using (FileStream stream = File.Open(projectFile, FileMode.O` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 449 | `using (FileStream stream = File.Open(projectFile, FileMode.O` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 530 | `using (FileStream stream = File.Open(projectFile, FileMode.O` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 611 | `using (FileStream stream = File.Open(projectFile, FileMode.O` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 672 | `using (var stream = File.Open(projectFile, FileMode.Open, Fi` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 758 | `using (var stream = File.Open(projectFile1, FileMode.Open, F` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 913 | `using (var stream = File.Open(projectFile1, FileMode.Open, F` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 1338 | `using (var stream = File.Open(projectFile1, FileMode.Open, F` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 1397 | `using (var stream = File.Open(projectFile1, FileMode.Open, F` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 1555 | `using (var stream = File.Open(projectFilePath, FileMode.Open` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 1618 | `using (var stream = File.Open(p2pProjectFilePath, FileMode.O` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 1628 | `using (var stream = File.Open(projectFilePath, FileMode.Open` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 1682 | `using (var stream = File.Open(libraryProjectFilePath, FileMo` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 1704 | `using (var stream = File.Open(consumerProjectFilePath, FileM` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 1859 | `using (var stream = File.Open(projectFile, FileMode.Open, Fi` |
| NuGet.Client | `test/NuGet.Core.FuncTests/Dotnet.Integration.Test/DotnetRestoreTests.cs` | 1916 | `using (var stream = File.Open(projectFile, FileMode.Open, Fi` |

*... and 185 more*

**Repos:** NuGet.Client

## Database

### Dapper (150 occurrences)

| Repo | File | Line | Context |
|------|------|------|---------||
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
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/ListPackageTests.cs` | 116 | `var result = testApp.Execute(argList.ToArray());` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/ListPackageTests.cs` | 146 | `var result = testApp.Execute(argList.ToArray());` |
| NuGet.Client | `test/NuGet.Core.FuncTests/NuGet.XPlat.FuncTest/ListPackageTests.cs` | 177 | `Assert.Throws<AggregateException>(() => testApp.Execute(argL` |

*... and 125 more*

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
