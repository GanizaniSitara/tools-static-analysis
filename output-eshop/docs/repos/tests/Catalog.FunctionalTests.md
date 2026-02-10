# Catalog.FunctionalTests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | tests |
| Path | `Catalog.FunctionalTests/Catalog.FunctionalTests.csproj` |
| Project References | 1 |
| NuGet Dependencies | 5 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Catalog_FunctionalTests["<strong>Catalog.FunctionalTests</strong>"]
    Catalog_API["Catalog.API"]
    Catalog_FunctionalTests --> Catalog_API
```

## Project References
- Catalog.API

## External NuGet Packages
| Package | Version |
|---------|---------||
| Asp.Versioning.Http.Client |  |
| Aspire.Hosting.PostgreSQL |  |
| Microsoft.AspNetCore.Mvc.Testing |  |
| Microsoft.AspNetCore.TestHost |  |
| xunit.v3.mtp-v2 |  |

## Data Access Patterns
### ConnectionString
| File | Line | Context |
|------|------|---------||
| `tests/Catalog.FunctionalTests/CatalogApiFixture.cs` | 15 | `private string _postgresConnectionString;` |
| `tests/Catalog.FunctionalTests/CatalogApiFixture.cs` | 33 | `{ $"ConnectionStrings:{Postgres.Resource.Name}", _postgresConnectionSt` |
| `tests/Catalog.FunctionalTests/CatalogApiFixture.cs` | 56 | `_postgresConnectionString = await Postgres.Resource.GetConnectionStrin` |


---

*[Back to Index](../../index.md)*
