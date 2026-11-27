# Architecture Decision Records

Each ADR follows the [MADR](https://adr.github.io/madr/) format. An accepted ADR is never edited to change its decision; a new ADR supersedes it.

| ADR | Title | Status |
| --- | --- | --- |
| [ADR-001](0001-backend-aspnet-core-modular-monolith.md) | Backend on C# / ASP.NET Core as a modular monolith | Accepted |
| [ADR-002](0002-postgresql-primary-database.md) | PostgreSQL as the primary database | Accepted |
| [ADR-003](0003-single-flutter-app-with-roles.md) | Single Flutter mobile app with role-based navigation | Accepted |
| [ADR-004](0004-rules-based-quoting-engine.md) | Rules-based quoting engine, no AI in the MVP | Accepted |
| [ADR-005](0005-manual-payments-sinpe-transfer.md) | Manual payments via SINPE Móvil and bank transfer | Accepted |
| [ADR-006](0006-separate-public-site-blazor-portal-admin.md) | Separate public site, Blazor client portal and Blazor admin panel | Superseded by ADR-008 |
| [ADR-007](0007-azure-cloud-provider.md) | Azure as the cloud provider | Accepted |
| [ADR-008](0008-react-typescript-spa-portal-and-admin.md) | Client portal and admin panel as React + TypeScript SPAs | Accepted |

## Follow-up ADRs (during project setup)

- Flutter state management and routing.
- Authentication provider (ASP.NET Core Identity or an external identity service).
- Notification service.

## New ADR

Copy the structure of an existing ADR, number it sequentially (`0009-short-title.md`), and open a pull request.
