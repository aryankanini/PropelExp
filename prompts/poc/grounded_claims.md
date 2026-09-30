# Grounded POC Claims

Classify each statement as either `facility_claim` or `generic_guidance`.

For a facility claim, provide its non-empty text, the required facility fact, and
only reviewed field or evidence span identifiers from the supplied deficiency
revision. Never copy or invent an identifier. An unsupported facility claim must
have an empty support-reference list so deterministic guardrails can replace it.

Generic guidance may describe compliance practice but must not assert a case or
facility fact. Generic guidance has no support-reference field.