# ADR-006: Separate public site, Blazor client portal and Blazor admin panel

**Status**: Superseded by [ADR-008](0008-react-typescript-spa-portal-and-admin.md) · **Date**: 2026-11-26 · **Deciders**: Jacob Tellez

> The subdomain split below still applies. The choice of Blazor for the client portal and admin panel was replaced by React + TypeScript SPAs in ADR-008.

## Context

vitalcarecr.com already exists as a public Next.js site that only shows the services; it handles no client data. The platform also needs a logged-in web portal for clients and a back office for provider admins. Both handle health and payment data.

## Decision drivers

- Keep health data out of the marketing site's attack surface.
- SEO for the public site; rich interactivity for the portal and back office.
- One language (C#) for everything that touches sensitive data.
- Independent deployments: a marketing change must never redeploy the portal.

## Considered options

| Option | Pros | Cons |
| --- | --- | --- |
| Next.js public site + Blazor portal + Blazor admin | Public site keeps SEO; sensitive apps share C# with the backend; separate deploys | Two web technologies to maintain |
| Everything in Next.js | One web stack, reuses current site | Sensitive logic split between TypeScript and C#; marketing and portal coupled |
| Flutter Web for portal and admin | Reuses mobile code | Weaker for data-heavy admin screens and accessibility |

## Decision

Split the web presence by subdomain:

| Subdomain | App | Technology | Data |
| --- | --- | --- | --- |
| vitalcarecr.com | Public site, services | Next.js (existing) | No patient data |
| app.vitalcarecr.com | Client portal | Blazor | Clients and patients, through the API |
| admin.vitalcarecr.com | Provider and platform admin panel | Blazor | Admin roles only, mandatory MFA |
| api.vitalcarecr.com | Backend API (ADR-001) | ASP.NET Core | The only component that talks to the database |

The public site links to the portal ("Cotizar" / "Iniciar sesión") and to the app stores. A WhatsApp chatbot is not part of the MVP; if one is added later, it must go through the API like any other client.

## Consequences

- Positive: a breach or bug in the marketing site cannot reach patient data; cookies and sessions are scoped per subdomain.
- Positive: the admin panel can get stricter controls (mandatory MFA, shorter sessions, optional IP allow list) without affecting clients.
- Negative: two Blazor apps share components; put them in a shared Razor class library to avoid duplication.
