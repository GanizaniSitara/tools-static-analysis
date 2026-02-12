# Project State — Dependency Mapper Python

**Date**: 2026-02-11
**Version**: v0.2 (data flow tracing)

## Pipeline

Three-stage static analysis pipeline for .NET solutions:

```
analyze.py  →  visualize.py  →  generate_docs.py
(scan & extract)  (Mermaid/GraphViz)  (viewer.html + markdown)
```

| File | Lines | Purpose |
|------|-------|---------|
| `analyze.py` | 1,120 | Scans .csproj/.sln files, extracts NuGet deps, project refs, data patterns with direction & endpoints, builds data flow graph |
| `visualize.py` | 716 | Generates Mermaid (.mmd) and GraphViz (.dot) diagrams including data flow diagram |
| `generate_docs.py` | 1,437 | Generates `viewer.html` (interactive single-page app) and markdown docs |

## Output Structure

Each run produces `output-{name}/` containing:

```
output-{name}/
├── viewer.html           # Interactive HTML viewer (serves via HTTP)
├── dependencies.csv      # NuGet package dependencies
├── project-refs.csv      # Project-to-project references
├── project-meta.json     # Project metadata (name, category, path)
├── data-sources.json     # Data access pattern findings (with direction, endpoint, project)
├── data-flow.json        # Data flow graph (nodes, edges, implied deps, infra groups)
├── configs.json          # Connection strings and config files
├── graph.json            # Full dependency graph
├── repos.json            # Repository info
├── diagrams/             # .mmd and .dot diagram files
│   └── all-diagrams.md
└── docs/                 # Generated markdown documentation
    └── diagrams/
        └── all-diagrams.md
```

**Important**: `viewer.html` must be served via HTTP (`python3 -m http.server`) because it uses `fetch()` to load JSON/CSV data files. It will not work from `file://`.

## Viewer Tabs

| Tab | Content |
|-----|---------|
| **Overview** | Category-level Mermaid diagram (Library, WebApp, Service, etc.) |
| **Per-category** | One tab per category showing project-level dependency diagram |
| **Data Flow** | Projects connected through shared data infrastructure (DB tables, message topics, API routes) |
| **Data Sources** | Searchable table of all data access pattern findings |
| **Implied Dependencies** | Cross-project dependencies derived from shared data infrastructure |
| **Connection Strings** | Connection strings extracted from config files |
| **All Projects** | Searchable table of all projects with metadata |

## Data Flow Tracing (v0.2)

### Enhanced Pattern Detection

57 patterns across 8 infrastructure types, each with direction and optional endpoint extraction:

| Category | Patterns | Direction | Endpoints Extracted |
|----------|----------|-----------|-------------------|
| **SQL** | Select, Insert, Update, Delete, CreateTable | read/write | Table names from SQL keywords |
| **EF/ORM** | DbContext, DbSet, EntityFramework | both | Entity type names |
| **Dapper** | Query, Execute | read/write | — |
| **MongoDB** | Read, Write, Collection | read/write | Collection names |
| **Kafka** | Producer, Consumer, Topic | write/read | Topic names (context-aware) |
| **RabbitMQ** | Publish, Consume, Queue, Exchange | write/read | Queue/exchange names |
| **API** | HttpGet/Post/Put/Delete, Route, MapGet/Post/Put/Delete, Controller | expose | Route paths |
| **gRPC** | Server, Client | expose/consume | — |
| **HTTP Client** | GetAsync, PostAsync, PutAsync, DeleteAsync, New, Injection, BaseAddress | consume | URL fragments |
| **WebSocket** | WebSocket | consume | — |
| **Redis** | Read, Write | read/write | — |
| **File** | Read, Write | read/write | — |
| **Other** | ConnectionString, Repository, DataAccess, FTP, IMessageAdapter, SqlConnection, SqlClient | various | — |

Each finding includes: `file`, `repo`, `line`, `project`, `pattern`, `type`, `direction`, `endpoint`, `endpointType`, `match`, `context`, `confidence`.

### SQL False Positive Filtering

Table name extraction from SQL uses a blocklist (`_SQL_KEYWORDS`) of ~60 SQL keywords and common false positives (IF, THE, CTE, T1, etc.) plus a minimum 4-character length filter.

### Data Flow Graph (`data-flow.json`)

```json
{
  "dataNodes": [
    {"id": "table:orders", "name": "orders", "type": "table",
     "infrastructure": "database",
     "writers": ["OrderService"], "readers": ["ReportService"],
     "exposers": [], "consumers": []}
  ],
  "dataEdges": [
    {"from": "OrderService", "to": "table:orders",
     "direction": "write", "endpointType": "table"}
  ],
  "impliedDependencies": [
    {"from": "OrderService", "to": "ReportService",
     "via": "orders", "viaType": "database"}
  ],
  "infrastructureGroups": [
    {"pattern": "Kafka.Producer", "type": "messaging",
     "projects": {"OrderService": {"write": 3}}}
  ]
}
```

**Implied dependencies**: When Project A writes to endpoint X and Project B reads from endpoint X, A→B is an implied data dependency.

### Data Flow Diagram (Mermaid)

Distinct shapes by infrastructure type:
- `[(" ")]` cylinder — database (tables, collections)
- `{{ }}` hexagon — messaging (topics, queues)
- `([ ])` stadium — API routes
- `==>` thick arrow — write/expose
- `-.->` dashed arrow — read/consume

Limits: MAX_DATA_NODES=30, MAX_PROJECTS=40 to prevent diagram explosion.

### Edge Click-Through

| Edge Type | Handler | Shows |
|-----------|---------|-------|
| Project ↔ Project | `showEdgeDetail()` | Direct refs, shared NuGets, shared data patterns, shared data flow nodes, implied deps |
| Project ↔ Data Node | `showDataFlowDetail()` | Data node type/infrastructure, writers, readers, exposers, consumers (clicked project highlighted), implied deps through node |

## Test Repos

| Dataset | Projects | Size | Key Data Flow Features |
|---------|----------|------|----------------------|
| **eShop** | 24 | Small | Kafka topics, API routes, EF entities |
| **EventStore** | 84 | Medium | Dapper read/write, gRPC server/client, implied deps via schema tables |
| **akka.net** | 109 | Medium | SQL table names (event_journal, snapshot), persistence patterns |
| **OrchardCore** | 230 | Large | EF DbSet entities, API controllers/routes |
| **StockSharp** | 140 | Medium | IMessageAdapter, Redis, WebSocket, gRPC, Kafka topics |
| **NuGet.Client** | 115 | Medium | HTTP client patterns, file read/write |
| **Lean** | 23 | Small | Dapper, MongoDB, Redis, Kafka, file I/O |

## Commit History

```
c371013 Add click-through detail panel for data flow edges
21a2ab9 Filter SQL false positives and restrict edge detail panel to project-project edges
97efa74 Add data flow tracing: direction-aware patterns, data flow graph, and Data Flow viewer tab
04b964c Add edge click-through detail panel to viewer
6e6171f Add edge hover highlight and tooltip to viewer diagrams
70ebf03 Add edge interaction implementation plan
f4f0126 Switch category detail diagrams to left-to-right layout
609f610 Add edge filter warning and new test repo outputs
88e99f7 Add test repo catalog with stress-test candidates
0464570 Fix edge limit and SVG sizing in viewer diagrams
d091597 Fix Mermaid syntax error and add zoom controls to viewer
49702c9 Add two-level diagram viewer: category overview + per-category detail
b2523d8 Revert Cytoscape.js experiment
f8f9210 Replace Mermaid diagrams with Cytoscape.js in viewer.html
cf9b96f Revert DrawIO changes, restore Mermaid-only viewer
9969faf Add CLAUDE.md with git discipline rules
c277397 Baseline: pre-DrawIO state with Mermaid viewer
```

## Known Limitations

- **Regex-based**: Static analysis via regex cannot trace dynamic endpoint names (variables, string interpolation, config-driven values)
- **Confidence varies**: High for structured patterns (ASP.NET attributes, type names), medium for SQL DML, low for dynamic URLs
- **SQL table extraction**: Despite filtering, some false positives may remain for unusual identifier patterns
- **Kafka topic extraction**: Tightened to require Kafka context keywords to avoid matching arbitrary strings
- **No cross-repo consumer→producer matching**: HTTP client URLs are rarely matchable to API route declarations across projects
- **Mermaid rendering limits**: Large diagrams capped at 30 data nodes / 40 projects; uses maxEdges=5000 and maxTextSize=500000
