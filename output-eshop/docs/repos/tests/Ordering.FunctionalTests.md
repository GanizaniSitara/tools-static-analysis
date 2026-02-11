# Ordering.FunctionalTests

## Overview

| Property | Value |
|----------|-------|
| Category | Test |
| Repository | tests |
| Path | `Ordering.FunctionalTests/Ordering.FunctionalTests.csproj` |
| Project References | 4 |
| NuGet Dependencies | 5 |
| Consumers | 0 |

## Dependency Diagram

```mermaid
graph TD
    Ordering_FunctionalTests["<strong>Ordering.FunctionalTests</strong>"]
    Ordering_API["Ordering.API"]
    Ordering_FunctionalTests --> Ordering_API
    Identity_API["Identity.API"]
    Ordering_FunctionalTests --> Identity_API
    Ordering_Domain["Ordering.Domain"]
    Ordering_FunctionalTests --> Ordering_Domain
    Ordering_Infrastructure["Ordering.Infrastructure"]
    Ordering_FunctionalTests --> Ordering_Infrastructure
```

## Project References
- Ordering.API
- Identity.API
- Ordering.Domain
- Ordering.Infrastructure

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
| `tests/Ordering.FunctionalTests/OrderingApiFixture.cs` | 17 | `private string _postgresConnectionString;` |
| `tests/Ordering.FunctionalTests/OrderingApiFixture.cs` | 35 | `{ $"ConnectionStrings:{Postgres.Resource.Name}", _postgresConnectionSt` |
| `tests/Ordering.FunctionalTests/OrderingApiFixture.cs` | 63 | `_postgresConnectionString = await Postgres.Resource.GetConnectionStrin` |

### HttpClient.GetAsync
| File | Line | Context |
|------|------|---------||
| `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 30 | `var response = await _httpClient.GetAsync("api/orders", TestContext.Cu` |
| `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 101 | `var response = await _httpClient.GetAsync("api/orders/cardtypes", Test` |
| `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 113 | `var response = await _httpClient.GetAsync("api/orders/1", TestContext.` |

### HttpClient.PostAsync
| File | Line | Context |
|------|------|---------||
| `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 128 | `var response = await _httpClient.PostAsync("api/orders", content, Test` |
| `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 155 | `var response = await _httpClient.PostAsync("api/orders", content, Test` |
| `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 181 | `var response = await _httpClient.PostAsync("api/orders/draft", content` |
| `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 196 | `var response = await _httpClient.PostAsync("api/orders/draft", content` |

### HttpClient.PutAsync
| File | Line | Context |
|------|------|---------||
| `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 46 | `var response = await _httpClient.PutAsync("/api/orders/cancel", conten` |
| `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 61 | `var response = await _httpClient.PutAsync("api/orders/cancel", content` |
| `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 76 | `var response = await _httpClient.PutAsync("api/orders/ship", content, ` |
| `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 91 | `var response = await _httpClient.PutAsync("api/orders/ship", content, ` |

### Redis.Read
| File | Line | Context |
|------|------|---------||
| `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 30 | `var response = await _httpClient.GetAsync("api/orders", TestContext.Cu` |
| `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 101 | `var response = await _httpClient.GetAsync("api/orders/cardtypes", Test` |
| `tests/Ordering.FunctionalTests/OrderingApiTests.cs` | 113 | `var response = await _httpClient.GetAsync("api/orders/1", TestContext.` |


---

*[Back to Index](../../index.md)*
