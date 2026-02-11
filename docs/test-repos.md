# Test Repository Catalog

## Current Test Datasets

| Dataset | Projects | Refs | Edges | Size Tier | Notes |
|---------|----------|------|-------|-----------|-------|
| eShop | 24 | 46 | ~50 | Small | Microsoft reference microservices app |
| Lean | 23 | 117 | ~120 | Small | QuantConnect algorithmic trading engine |
| StockSharp | 140 | 200 | ~270 | Medium | Trading platform, 62 samples + 40 localizations (skipped) |
| OrchardCore | 230 | 1,208 | ~1,300 | Large | CMS framework, 192 libraries share `OrchardCore.*` prefix |

## Planned Stress-Test Repos

These were identified to test the two-level viewer with heterogeneous, platform-style repos
(diverse naming, no common prefix) that better mimic a real container platform with ~100+
projects added organically over time.

### Tier 1: Platform-like (~100 projects, heterogeneous naming)

| Repo | .csproj count | GitHub | Why |
|------|--------------|--------|-----|
| **akka.net** | 109 | akkadotnet/akka.net | Actor framework with core/remoting/persistence/streams/cluster/tests — diverse naming, good category mix |
| **NuGet.Client** | 115 | NuGet/NuGet.Client | Package manager platform: CLI, server, protocol, resolver, restore, signing — varied project names |
| **EventStore** | 84 | EventStore/EventStore | Event-sourcing server: projections, clients, gRPC, plugins, tests — platform with add-ons |

These are the best analogues for a ~100-project container platform where projects don't
share a common prefix and represent different services/tools added over time.

### Tier 2: Large frameworks (stress testing Mermaid limits)

| Repo | .csproj count | GitHub | Why |
|------|--------------|--------|-----|
| **dotnet/aspire** | 391 | dotnet/aspire | Cloud-native platform, varied components (dashboards, integrations, hosting) |
| **dotnet/roslyn** | 304 | dotnet/roslyn | C# compiler, analyzers, workspaces — monolithic but large |
| **abpframework/abp** | 641 | abpframework/abp | Modular app framework, hundreds of modules |
| **dotnet/aspnetcore** | 600 | dotnet/aspnetcore | Web framework, very diverse project types |

### Tier 3: Extreme scale

| Repo | .csproj count | GitHub | Why |
|------|--------------|--------|-----|
| **Azure/azure-sdk-for-net** | 1,134 | Azure/azure-sdk-for-net | Every Azure service as a separate project, ultimate heterogeneous stress test |
| **dotnet/runtime** | 5,787 | dotnet/runtime | .NET runtime itself, massive — tests grouping at extreme scale |

## Other Repos Evaluated (not selected)

| Repo | .csproj | Notes |
|------|---------|-------|
| bitwarden/server | 55 | Too small |
| jellyfin/jellyfin | 42 | Too small |
| SteeltoeOSS/Steeltoe | 70 | Microservices toolkit, possible future candidate |
| dotnet/tye | 81 | Container orchestrator, decent but archived |
| MassTransit/MassTransit | 59 | Message bus, decent mix but small |
| dotnet/maui | 134 | UI framework, less platform-like |
| nopCommerce | 37 | Too small |

## Known Mermaid Limits

Discovered during OrchardCore testing:

- **Edge limit**: Mermaid v11 defaults to max 500 edges. Manifests as misleading "Syntax error in text" message. Set `maxEdges` in `mermaid.initialize()` to override.
- **Text size limit**: Default 50,000 chars. Set `maxTextSize` to override.
- **SVG sizing**: Mermaid sets `width="100%"` on SVGs. For large diagrams this squeezes everything into the container. Must override with natural viewBox width post-render.
- **Grouped diagram edge filtering**: When a category has >50 projects, we group by name prefix and auto-filter low-count edges to stay under 400 edges. Currently this drops edges silently — TODO: add a visible note showing how many edges were filtered.
