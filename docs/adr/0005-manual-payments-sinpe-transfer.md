# ADR-005: Manual payments via SINPE Móvil and bank transfer

**Status**: Accepted · **Date**: 2026-11-26 · **Deciders**: Jacob Tellez

## Context

Clients are billed weekly for completed shifts. The company is not yet formally registered, which complicates contracting a card payment gateway, and SINPE Móvil and transfers are the most common way to pay in Costa Rica.

## Decision drivers

- Launch without a payment gateway contract or card-data compliance scope (PCI DSS).
- Keep a reliable record of balances and who approved each payment.
- Leave room to add a gateway later without redesigning billing.

## Considered options

| Option | Pros | Cons |
| --- | --- | --- |
| Manual SINPE / transfer with proof upload and admin verification | No gateway contract, no card data, zero fees from the platform | Manual verification work, risk of fake or duplicated proofs |
| Card payment gateway | Automatic confirmation | Requires a registered company and contract, fees, PCI scope |

## Decision

The Payments module records **manual payments** with this lifecycle:

1. **Pending**: the weekly statement lists completed shifts and the balance; the app shows the company's SINPE number and IBAN accounts.
2. **Proof submitted**: the client uploads the receipt image and the reference number.
3. **Verified** or **Rejected**: a provider admin checks it against the bank statement; the system records who decided, when, and why.
4. Duplicate reference numbers are blocked automatically; a weekly reconciliation report lists unmatched payments.

Payments are modeled behind an `IPaymentMethod` abstraction so a gateway can be added as a new method in Release 2.

## Consequences

- Positive: no card data ever touches the system, which keeps PCI DSS out of scope.
- Negative: confirmation is not instant; target verification within one business day.
- Negative: receipt images may contain personal data; store them encrypted with restricted access and a retention period.
