# ADR-002: PostgreSQL as the primary database

**Status**: Accepted · **Date**: 2026-11-26 · **Deciders**: Jacob Tellez

## Context

The data is strongly relational: a client has many patients, a booking has many shifts, a shift has caregivers in rotation, a payment settles shifts. Weekly billing, holiday rules and audit queries need joins, transactions and reporting. The system stores sensitive health data under Costa Rica's Law 8968 and must be ready for several providers sharing one database.

## Decision drivers

- ACID transactions for bookings and payments.
- Tenant isolation for a future multi-provider model.
- Encryption and fine-grained access control for health data.
- Open source, no license cost, available as a managed service on every major cloud.

## Considered options

| Option | Pros | Cons |
| --- | --- | --- |
| PostgreSQL | Relational, ACID, row-level security, JSONB for flexible fields, pgcrypto, first-class EF Core provider | Requires schema design and migrations up front |
| SQL Server | Excellent .NET integration | License cost outside the free Express tier, fewer low-cost managed options |
| Firestore | Already known from university projects, real-time sync | Weak for joins, reports and transactions across documents; harder to audit |

## Decision

Use **PostgreSQL** (managed service) through **EF Core with the Npgsql provider**. Rules:

- Every business table carries a `provider_id` (tenant) column; enforce isolation in the application and with PostgreSQL row-level security as defense in depth.
- Health fields (allergies, medications, conditions relevant to care) are encrypted at the application level before storage; the database disk is also encrypted at rest.
- Schema changes only through versioned EF Core migrations, reviewed in pull requests.
- An `audit_log` table records who read or changed patient and payment data.
- Patient data follows the minimum set accepted on 2026-11-26: name, date of birth, service address, emergency contact, dependency level, allergies, medications and schedules, mobility and diet restrictions. Blood type, weight and height, treating doctor and routine preferences are optional.

## Consequences

- Positive: reliable billing and reporting, and a clear path to multi-tenancy without a second database.
- Positive: Law 8968 and the proposed encryption reform (bill 25.826) are covered by design.
- Negative: application-level encryption limits searching inside encrypted fields; search only on non-sensitive columns.
- Negative: real-time updates (who is caring now) need a push channel (SignalR or push notifications) instead of database listeners.
