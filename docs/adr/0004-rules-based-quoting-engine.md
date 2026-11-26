# ADR-004: Rules-based quoting engine, no AI in the MVP

**Status**: Accepted · **Date**: 2026-11-26 · **Deciders**: Jacob Tellez

## Context

Clients must get an approximate quote right after describing their needs. Prices depend on the care level (Verde, Amarillo, Rojo), hours per shift, days per week, the holiday policy and discounts. The quote is approximate until the provider confirms it, and it is delivered as a branded PDF.

## Decision drivers

- Every quote must be explainable and reproducible: same inputs, same price.
- No health data sent to third-party AI services.
- Provider admins must change prices without a code release.
- Low running cost.

## Considered options

| Option | Pros | Cons |
| --- | --- | --- |
| Rules engine with configurable price tables | Deterministic, testable, free to run, auditable | Needs a guided form to capture needs correctly |
| LLM assistant reading price documents | Conversational experience | Can produce wrong prices, sends sensitive data to a third party, ongoing cost, hard to audit |

## Decision

Implement a **deterministic quoting engine** in the Quoting module:

1. A guided intake form maps the patient's needs to a care level (Verde, Amarillo, Rojo).
2. Price tables, holiday rules and discounts are stored as versioned configuration with an effective date, editable from the admin panel.
3. The engine computes the quote line by line (level x hours x days, holiday adjustment, discounts) and stores the inputs, the price-table version used and the result.
4. A PDF is rendered from a template with the provider's logo (for example with QuestPDF) and marked "approximate until confirmed".
5. A provider admin confirms or adjusts the quote; adjustments keep the original and the reason.

## Consequences

- Positive: quotes are auditable and fully covered by unit tests on the calculation.
- Positive: each provider in the future marketplace can own its own price tables.
- Negative: an unusual case falls outside the form; the admin adjusts it manually and the case feeds future rules.
- Revisit: an AI assistant can be added later as an optional layer that only fills the form, never sets the price.
