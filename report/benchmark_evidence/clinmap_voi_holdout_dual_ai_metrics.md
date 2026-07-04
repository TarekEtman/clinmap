# Holdout dual AI protocol metrics

**Disclosure:** Both raters are documented AI protocols (`rater_type: ai_protocol`), not human clinicians.

- Holdout items: **720**
- κ(contract, escalation): **0.5021**
- Agreement(contract, escalation): **0.5986**
- κ(contract, primary): **0.7678**
- κ(escalation, primary): **0.513**
- Agreement(contract, primary): **0.8167**
- Agreement(escalation, primary): **0.6139**

Source: `data/clinmap_voi_v0/panel_holdout_reviews.jsonl`

Methodologies:
- `ai_protocol_contract_v0` — contract-first evidence override
- `ai_protocol_escalation_v0` — escalation-behavioral response fit (no row gold anchor)
