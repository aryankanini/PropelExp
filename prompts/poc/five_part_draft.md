# Five-Part POC Draft

Generate a plan of correction using only the supplied deficiency revision. Do not
use facts from another deficiency or infer missing facility facts.

Return structured JSON containing exactly five sections in this order:

1. `affected_residents`
2. `others_at_risk`
3. `corrective_measures`
4. `monitoring`
5. `completion_date`

Each section must contain at least one non-empty statement. Do not add sections,
metadata, commentary, or provider-specific fields.