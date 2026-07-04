# Public Release Checklist

This checklist must pass before publishing the repository or sharing the landing page.

## Neutrality

- [ ] Public files do not mention target platforms or hiring campaigns.
- [ ] Public files do not include internal routing language.
- [ ] The project is positioned as neutral evaluation engineering proof-of-work.

## Clinical and privacy safety

- [ ] All examples are synthetic.
- [ ] No patient data, PHI, clinical screenshots, employer tasks, client content, or proprietary rubrics.
- [ ] The scope states this is not medical advice, diagnosis, triage, treatment guidance, clinical validation, or production safety certification.
- [ ] Medication-related material is framed as evaluating AI response behavior, not giving medication instructions.

## Evidence quality

- [ ] `make audit` passes.
- [ ] `python3 -m unittest tests.test_clinmap_hosted_review_pipeline` passes.
- [ ] Scripts run without private API keys.
- [ ] **ClinMAP-VOI v0:** review queue, relation annotations, performance metrics, and QA audit are linked from README.
- [ ] ClinMAP metrics use audit claim boundary (not clinical validation / safety certification).
- [ ] Synthetic v1 demo metrics are labeled illustration-only where shown.
- [ ] Synthetic cases are specific and failure-focused.
- [ ] At least one borderline/review case is included.
- [ ] At least one over-refusal or low-acuity control case is included.
- [ ] Reasoning faithfulness is represented.

## Reviewer usability

- [ ] README explains the project in under 60 seconds.
- [ ] Landing page has clear links to repo, snapshot, and cases.
- [ ] PDF snapshot is readable and under 3 pages.
- [ ] Contact information is visible.
- [ ] Case studies use concise reviewer-style language.

## Anti-overbuild standard

- [ ] No unnecessary dashboards.
- [ ] No fake model leaderboard.
- [ ] No claims of production readiness.
- [ ] No complex app unless the repo evidence is already strong.
