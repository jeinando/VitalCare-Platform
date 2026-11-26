# VitalCare Platform

Web and mobile platform to quote, book, pay for and follow home care services in Costa Rica. It starts with a single provider (VitalCareCR) and is designed to grow into a multi-provider marketplace.

## Status

Planning and documentation (Release 1). No application code yet.

## Planned stack

| Part | Technology | Decision |
| --- | --- | --- |
| Backend API | C# / ASP.NET Core, modular monolith | [ADR-001](docs/adr/0001-backend-aspnet-core-modular-monolith.md) |
| Database | PostgreSQL (Azure Flexible Server) | [ADR-002](docs/adr/0002-postgresql-primary-database.md) |
| Mobile app | Flutter, one app with client and caregiver roles | [ADR-003](docs/adr/0003-single-flutter-app-with-roles.md) |
| Client portal and admin panel | Blazor | [ADR-006](docs/adr/0006-separate-public-site-blazor-portal-admin.md) |
| Public site | Next.js (existing vitalcarecr.com) | [ADR-006](docs/adr/0006-separate-public-site-blazor-portal-admin.md) |
| Hosting | Azure | [ADR-007](docs/adr/0007-azure-cloud-provider.md) |

## Documentation

| Document | Path |
| --- | --- |
| Architecture Decision Records | [docs/adr/](docs/adr/README.md) |
| C4 container view | [docs/architecture/c4-containers.md](docs/architecture/c4-containers.md) |
| Definition of Ready and Done | [docs/process/definition-of-ready-and-done.md](docs/process/definition-of-ready-and-done.md) |
| Release 1 backlog seed | [backlog/](backlog/README.md) |

## Way of working

- Work is tracked in GitHub Issues, one issue per user story or technical task, labeled by epic, priority and type.
- Every change goes through a pull request that follows the Definition of Done in the PR template.
- Personal and health data are handled under Costa Rica's Law 8968: encrypted, access-controlled and audited.
