# ADR-008: Client portal and admin panel on React with Next.js

**Status**: Accepted · **Date**: 2026-11-26 · **Deciders**: Jacob Tellez · **Supersedes**: [ADR-006](0006-separate-public-site-blazor-portal-admin.md)

## Context

ADR-006 split the web presence by subdomain and chose Blazor for the client portal and the admin panel, arguing that everything touching sensitive data should share C# with the backend. On review, that argument is weak: health and payment data are protected by the backend API (ADR-001, ADR-002), which authorizes, encrypts and audits every request. The front end only displays what the API returns, so its language does not change the security model.

The long-term factors point the other way: the public site vitalcarecr.com is already built with Next.js, the React ecosystem is much larger, and React skills are easier to find and reuse.

## Decision drivers

- Long-term maintainability and access to developers.
- A large ecosystem for data-heavy screens: calendars, tables, forms, charts.
- One design system shared by the public site, the portal and the admin panel.
- Security stays enforced in the API, independent of the front-end technology.

## Considered options

| Option | Pros | Cons |
| --- | --- | --- |
| React with Next.js (TypeScript) | Largest ecosystem and talent pool; same stack as the public site; shared components and branding | API types must be generated from OpenAPI to stay in sync |
| Blazor (ADR-006) | Shares C# models with the backend | Smaller ecosystem and talent pool; heavy WebAssembly download or a permanent server connection |
| Flutter Web | Reuses mobile code | Weaker for data-heavy admin screens, accessibility and SEO |

## Decision

Build the client portal and the admin panel as **two separate Next.js (React, TypeScript) applications**. The backend stays on ASP.NET Core (ADR-001). The subdomain split from ADR-006 is kept:

| Subdomain | App | Technology | Hosting | Data |
| --- | --- | --- | --- | --- |
| vitalcarecr.com | Public site | Next.js (existing) | Vercel | No patient data |
| app.vitalcarecr.com | Client portal | Next.js | Azure App Service | Clients and patients, through the API |
| admin.vitalcarecr.com | Provider and platform admin panel | Next.js | Azure App Service | Admin roles only, mandatory MFA |
| api.vitalcarecr.com | Backend API | ASP.NET Core | Azure App Service | The only component that talks to the database |

Rules:

- The portal and the admin panel are hosted on Azure, not Vercel, so health data is processed by a single cloud provider (ADR-007).
- A shared UI package (design system) is used by the public site, the portal and the admin panel.
- The TypeScript API client is generated from the backend OpenAPI contract in CI; no hand-written request types.
- Session tokens live in `HttpOnly`, `Secure`, `SameSite` cookies, never in `localStorage`.
- Server-only code (tokens, API calls with credentials) is marked with the `server-only` package so it can never be bundled into client components.
- Strict security headers, including a Content Security Policy, on both apps.
- The API remains the only authority for authorization; hiding a screen in the UI is never a security control.

## Consequences

- Positive: one web stack (TypeScript) across the public site, portal and admin panel, with shared components and branding.
- Positive: access to the React ecosystem and a larger pool of developers.
- Negative: two languages on the server side of the web (TypeScript in Next.js, C# in the API); keep business rules in the API, not in Next.js.
- Negative: generated API types must be regenerated on every API contract change; CI fails if they are out of date.
