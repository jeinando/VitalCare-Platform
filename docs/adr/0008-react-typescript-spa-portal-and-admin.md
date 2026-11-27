# ADR-008: Client portal and admin panel as React + TypeScript SPAs

**Status**: Accepted · **Date**: 2026-11-26 · **Deciders**: Jacob Tellez · **Supersedes**: [ADR-006](0006-separate-public-site-blazor-portal-admin.md)

## Context

ADR-006 split the web presence by subdomain and chose Blazor for the client portal and the admin panel, arguing that everything touching sensitive data should share C# with the backend. On review, that argument is weak: health and payment data are protected by the backend API (ADR-001, ADR-002), which authorizes, encrypts and audits every request. The front end only displays what the API returns, so its language does not change the security model.

The long-term factors point to React: the public site vitalcarecr.com is already built with React (Next.js), the React ecosystem is much larger, and React skills are easier to find and reuse. Both apps sit behind a login, so they need no SEO or server-side rendering.

## Decision drivers

- Long-term maintainability and access to developers.
- A large ecosystem for data-heavy screens: calendars, tables, forms, charts.
- Type safety for a domain with money, schedules and health data.
- Simple, low-cost hosting with no extra server to patch.
- Security stays enforced in the API, independent of the front-end technology.

## Considered options

| Option | Pros | Cons |
| --- | --- | --- |
| React + TypeScript SPA, built with Vite | Simple to learn and maintain; static hosting; same React components as the public site; types generated from the API | No server layer: cookies, CORS and CSRF must be configured exactly |
| Next.js + TypeScript | Server layer can hold tokens (BFF pattern); same framework as the public site | SEO and SSR are not needed here; more concepts; needs a Node server |
| React + JavaScript | Fastest start | No type checking for money, schedules and health data |
| Blazor (ADR-006) | Shares C# models with the backend | Smaller ecosystem and talent pool; heavy WebAssembly download or a permanent server connection |

## Decision

Build the client portal and the admin panel as **two separate single-page applications with React and TypeScript, built with Vite**. The backend stays on ASP.NET Core (ADR-001). The subdomain split from ADR-006 is kept:

| Subdomain | App | Technology | Hosting | Data |
| --- | --- | --- | --- | --- |
| vitalcarecr.com | Public site | Next.js (existing) | Vercel | No patient data |
| app.vitalcarecr.com | Client portal | React + TypeScript (Vite) | Azure Static Web Apps | Clients and patients, through the API |
| admin.vitalcarecr.com | Provider and platform admin panel | React + TypeScript (Vite) | Azure Static Web Apps | Admin roles only, mandatory MFA |
| api.vitalcarecr.com | Backend API | ASP.NET Core | Azure App Service | The only component that talks to the database |

Rules:

- TypeScript in `strict` mode; no plain JavaScript files in the apps.
- The TypeScript API client is generated from the backend OpenAPI contract in CI; no hand-written request types.
- The API keeps the session in `HttpOnly`, `Secure`, `SameSite=Strict` cookies; tokens are never stored in `localStorage` or readable by JavaScript.
- The API accepts requests only from the portal and admin origins (CORS with credentials) and requires an anti-forgery token on every state-changing request (CSRF protection).
- The admin panel uses its own session with a shorter lifetime and mandatory MFA.
- A shared UI package (design system) is used by the public site, the portal and the admin panel.
- Strict security headers, including a Content Security Policy, set in the Static Web Apps configuration.
- The API remains the only authority for authorization; hiding a screen in the UI is never a security control.

## Consequences

- Positive: simple apps, cheap static hosting, and no front-end server to patch; health data only travels between the browser and the API.
- Positive: one component library (React) across the public site, portal and admin panel, and access to the React ecosystem.
- Negative: with no server layer, the cookie, CORS and CSRF setup must be exact and covered by tests.
- Negative: generated API types must be regenerated on every API contract change; CI fails if they are out of date.
