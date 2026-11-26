# ADR-003: Single Flutter mobile app with role-based navigation

**Status**: Accepted · **Date**: 2026-11-26 · **Deciders**: Jacob Tellez

## Context

Clients (and patients with their own account) and caregivers both need a mobile app on Android and iOS. Clients quote, book, pay and follow the care log; caregivers see assignments, check in and out, and write the care log. One developer must build and maintain it, with automated tests and full control of the source code.

## Decision drivers

- One codebase for Android and iOS.
- Full source control, automated testing and CI, which ruled out FlutterFlow.
- Push notifications and offline tolerance for caregivers with weak signal.
- Reuse of the team's existing Dart and Flutter knowledge.

## Considered options

| Option | Pros | Cons |
| --- | --- | --- |
| Flutter, one app with roles | One codebase, one store listing, shared components, strong testing tools | Larger app; role logic must be well separated |
| Flutter, two apps (client and caregiver) | Smaller apps, separate release cycles | Two store listings, duplicated setup and CI |
| React Native | Large ecosystem, JavaScript skills | Less team experience; no reuse of existing Flutter work |
| FlutterFlow | Very fast prototyping | Limited testing, code ownership and review workflow |

## Decision

Build **one Flutter app** with role-based navigation: after login, the API returns the user's role and the app loads the client or caregiver shell. Guidelines:

- Feature-first folder structure (`features/booking`, `features/care_log`, ...) with a shared `core` package.
- State management and routing chosen in the project setup and recorded as a follow-up ADR; the API client is generated from the backend OpenAPI contract.
- Tokens stored in secure storage (Keychain / Keystore), never in plain preferences.
- Push notifications through Firebase Cloud Messaging for Android and iOS.
- Caregiver care-log entries are saved locally first and synced when the connection returns.

## Consequences

- Positive: one build pipeline and one listing per store; shared UI components and design system.
- Negative: role checks happen in the API, never only in the app; the app hides screens but the backend authorizes every request.
- Negative: if caregivers later need a very different experience, splitting into two apps is possible because features are already isolated.
