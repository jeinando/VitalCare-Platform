# ADR-007: Azure as the cloud provider

**Status**: Accepted · **Date**: 2026-11-26 · **Deciders**: Jacob Tellez

## Context

The API, the two Blazor apps, PostgreSQL, file storage for receipts and quote PDFs, and secrets need a host. One person operates everything, so managed backups, patching and monitoring matter more than the lowest possible price. The public Next.js site already targets Vercel.

## Decision drivers

- First-class support for ASP.NET Core and Blazor deployments.
- Managed PostgreSQL with automatic backups and encryption at rest.
- A secrets store and managed identities, so no credentials live in code or config files.
- Simple CI/CD from GitHub.

## Considered options

| Option | Pros | Cons |
| --- | --- | --- |
| Azure | Native .NET tooling, managed PostgreSQL, Key Vault, managed identities, GitHub Actions integration | Costs grow if resources are oversized; needs budget alerts |
| AWS | Broadest service catalog | Less natural fit for .NET tooling; more setup for one person |
| VPS with Docker | Lowest monthly cost | Backups, OS patching, TLS and hardening are all manual; higher security risk |

## Decision

Host the platform on **Azure**, with the public site staying on Vercel:

| Component | Azure service |
| --- | --- |
| Backend API, client portal, admin panel | Azure App Service (Linux), one app per subdomain |
| Database | Azure Database for PostgreSQL, Flexible Server |
| Receipts and quote PDFs | Azure Blob Storage, private containers |
| Secrets and encryption keys | Azure Key Vault, accessed through managed identity |
| Logs, metrics, alerts | Application Insights and Azure Monitor |
| Transactional email | Azure Communication Services (or an external email provider) |
| Push notifications | Firebase Cloud Messaging, called from the API |

Rules: infrastructure defined as code (Bicep), two environments (staging and production), budget alerts from the first day, and the region chosen after confirming that every service is available there.

## Consequences

- Positive: backups, patching and TLS certificates are managed by the platform.
- Positive: Key Vault and managed identities remove passwords from configuration.
- Negative: data is stored outside Costa Rica (no Azure region in the country); the privacy policy and consent must disclose the international transfer under Law 8968.
- Negative: costs must be watched; start on the smallest tiers and scale only with real usage.
