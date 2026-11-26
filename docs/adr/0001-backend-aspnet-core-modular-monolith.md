# ADR-001: Backend on C# / ASP.NET Core as a modular monolith

**Status**: Accepted · **Date**: 2026-11-26 · **Deciders**: Jacob Tellez (Technical Lead)

## Context

VitalCare needs one backend API that serves the Flutter app, the web client and the admin panel. It handles health data, payments and audit trails, and must grow from one provider to a multi-provider marketplace. The team is one developer working part time, with prior .NET experience.

## Decision drivers

- Strong typing and mature tooling for a domain with money, schedules and health data.
- Built-in security: authentication, authorization policies, data protection APIs.
- Low operational cost and complexity for a one-person team.
- Long-term support and an ecosystem for testing and documentation (OpenAPI).

## Considered options

| Option | Pros | Cons |
| --- | --- | --- |
| C# / ASP.NET Core Web API | Team experience, strong typing, EF Core, built-in Identity and policy-based authorization, OpenAPI support, LTS releases | Heavier than Node for small scripts |
| Node.js / Next.js API routes (TypeScript) | Same language as the public site | Weaker structure for a large domain, serverless limits for background jobs |
| Firebase (serverless) | Fast start, already used in university projects | Vendor lock-in, NoSQL fits relational data poorly, harder audit and reporting |

## Decision

Build the backend as an **ASP.NET Core Web API on the current .NET LTS release**, structured as a **modular monolith**: one deployable unit split into modules (Identity, Patients, Catalog, Quoting, Bookings, CareLog, Payments, Notifications, Admin). Each module owns its tables and exposes behavior only through its public interface. Inside each module, use Clean Architecture layers (Domain, Application, Infrastructure, API).

## Consequences

- Positive: one codebase and one deployment keep operations simple; modules can be extracted into services later if the marketplace demands it.
- Positive: EF Core migrations, xUnit tests and Swagger give a documented, testable API from day one.
- Negative: any future integration (for example a WhatsApp chatbot) must call the API, never the database directly.
- Negative: module boundaries need discipline; enforce them with architecture tests (for example NetArchTest).
