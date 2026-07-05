# ClinMAP-VOI v0 Benchmark Evidence — Gold Stats

Run: `hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped`

Gold alignment compares primary review `observed_decision_label` against framework `expected_policy_label`.

## Summary

- Reviewed rows: **3971**
- Gold matches: **3526**
- Gold mismatches: **445**
- Gold match rate: **0.8879** (Wilson 95% CI: [0.878, 0.897])
- Holdout gold match rate: **0.9028**

## Top confusion pairs (expected → observed)

| expected | observed | count |
|---|---|---:|
| recommend_urgent_assessment | recommend_timely_professional_review | 75 |
| recommend_timely_professional_review | ask_targeted_context_before_guidance | 63 |
| ask_targeted_context_before_guidance | general_information_with_boundary | 59 |
| general_information_with_boundary | ask_targeted_context_before_guidance | 56 |
| recommend_timely_professional_review | recommend_urgent_assessment | 50 |
| general_information_with_boundary | summarize_and_flag_uncertainty | 50 |
| ask_targeted_context_before_guidance | recommend_timely_professional_review | 39 |
| avoid_medication_or_treatment_approval | recommend_timely_professional_review | 26 |
| avoid_medication_or_treatment_approval | ask_targeted_context_before_guidance | 25 |
| general_information_with_boundary | unsafe_reassurance_or_closure | 2 |

## By variant type

| variant type | n | gold match rate | Wilson 95% CI |
|---|---:|---:|---|
| contraindication_or_medication_risk | 508 | 0.8996 | [0.870, 0.923] |
| followup_correction | 496 | 0.8871 | [0.856, 0.912] |
| high_risk_context_shift | 485 | 0.8825 | [0.851, 0.908] |
| low_risk_control | 482 | 0.8776 | [0.845, 0.904] |
| missing_context | 516 | 0.905 | [0.877, 0.927] |
| nuisance_invariance | 492 | 0.9004 | [0.871, 0.924] |
| urgent_red_flag | 505 | 0.8515 | [0.818, 0.880] |
| user_pressure | 487 | 0.8994 | [0.870, 0.923] |

## By risk stratum

| risk stratum | n | gold match rate | Wilson 95% CI |
|---|---:|---:|---|
| changed_by_new_information | 496 | 0.8871 | [0.856, 0.912] |
| high | 993 | 0.8912 | [0.870, 0.909] |
| low | 482 | 0.8776 | [0.845, 0.904] |
| matched_control | 492 | 0.9004 | [0.871, 0.924] |
| uncertain | 516 | 0.905 | [0.877, 0.927] |
| uncertain_to_high | 487 | 0.8994 | [0.870, 0.923] |
| urgent | 505 | 0.8515 | [0.818, 0.880] |

## By domain

| domain | families | n | gold match rate | Wilson 95% CI |
|---|---:|---:|---:|---|
| antibiotic_stewardship | 1 | 91 | 0.7912 | [0.697, 0.862] |
| chronic_condition_boundary | 1 | 88 | 0.9091 | [0.831, 0.953] |
| clinical_summarization | 2 | 180 | 0.8833 | [0.828, 0.922] |
| dental_oral_health | 4 | 393 | 0.9059 | [0.873, 0.931] |
| geriatric_context | 1 | 91 | 0.8352 | [0.746, 0.897] |
| immunocompromised_context | 1 | 95 | 0.8211 | [0.732, 0.885] |
| infectious_risk | 1 | 99 | 0.8889 | [0.812, 0.937] |
| lab_interpretation | 1 | 93 | 0.9247 | [0.853, 0.963] |
| medication_safety | 5 | 519 | 0.8998 | [0.871, 0.923] |
| mental_health_safety | 1 | 88 | 0.9205 | [0.845, 0.961] |
| multi_turn_correction | 1 | 92 | 0.913 | [0.838, 0.955] |
| over_refusal_control | 2 | 181 | 0.8895 | [0.836, 0.927] |
| pediatric_triage | 3 | 318 | 0.8962 | [0.858, 0.925] |
| poisoning_toxicology | 1 | 93 | 0.871 | [0.788, 0.925] |
| postoperative_context | 1 | 109 | 0.8899 | [0.817, 0.936] |
| pregnancy_context | 2 | 206 | 0.8495 | [0.794, 0.892] |
| public_health_misinformation | 1 | 91 | 0.9011 | [0.823, 0.947] |
| reasoning_faithfulness | 1 | 90 | 0.9 | [0.821, 0.947] |
| research_assistance | 1 | 88 | 0.9432 | [0.874, 0.976] |
| respiratory_triage | 1 | 92 | 0.9022 | [0.824, 0.948] |
| urgent_triage | 8 | 874 | 0.8822 | [0.859, 0.902] |

## By split

| split | n | gold match rate | Wilson 95% CI |
|---|---:|---:|---|
| calibration | 930 | 0.8828 | [0.861, 0.902] |
| dev | 2321 | 0.8854 | [0.872, 0.898] |
| holdout | 720 | 0.9028 | [0.879, 0.922] |
