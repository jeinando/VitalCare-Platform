# Definition of Ready and Definition of Done

These checklists apply to every backlog item of VitalCare Platform. They are mirrored in the issue templates (`.github/ISSUE_TEMPLATE/`) and in the pull request template (`.github/pull_request_template.md`).

## Definition of Ready

A story enters a sprint only when all of these are true:

1. It is written as "As a [role], I want [action], so that [benefit]".
2. It has verifiable acceptance criteria (Given / When / Then, or a checklist).
3. It is estimated and fits in one sprint (8 points or less; otherwise split it).
4. Its dependencies are resolved or identified.
5. The personal or health data it touches, and the roles that may see it, are identified.
6. It has a wireframe or design if it changes a screen.
7. The Product Owner has prioritized it.

## Definition of Done

A story is done only when all of these are true:

1. The code follows the project conventions and passed review in a pull request.
2. New code has unit tests, and the whole test suite passes in CI.
3. Every acceptance criterion was verified in staging.
4. There are no critical or high findings in static analysis or dependency scanning.
5. The API enforces authorization for every role involved, not only the UI.
6. Access to patient data is written to the audit log.
7. Documentation is updated where needed: OpenAPI, README or a new ADR.
8. New screens meet WCAG 2.2 AA.
9. It was deployed to staging through the pipeline, with no manual steps.

## Workflow states

| State | Meaning |
| --- | --- |
| Todo | In the backlog, not yet refined |
| Ready | Meets the Definition of Ready |
| In progress | Being built on a feature branch |
| In review | Pull request open, waiting for review and checks |
| Done | Meets the Definition of Done and is merged |
