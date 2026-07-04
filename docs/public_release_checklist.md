# Public Release Checklist — ClinMAP

This checklist must pass before publishing the repository or sharing the landing page. Publication here means **portfolio / evaluation-engineering release**, not clinical validation.

## Canonical workspace

- [ ] Work only from `/Users/nati/Documents/JOB/ClinMAP`.
- [ ] Do not use sibling mock/rehearsal folders for claims, paths, PDFs, or reports.
- [ ] `ClinMAP.code-workspace` opens the repo root; no stale workspace files are used.

## Required local gates

Run from repo root:

```bash
cd /Users/nati/Documents/JOB/ClinMAP
make clinmap-frontier-pack
make clinmap-pdf
npm run build
make audit
python3 -m unittest discover -s tests
```

Required outcomes:

- [ ] `make clinmap-frontier-pack` regenerates benchmark evidence, holdout panel metrics, and QA audit.
- [ ] `make clinmap-pdf` refreshes `report/clinmap_voi_v0_snapshot.pdf` and `public/assets/clinmap_voi_v0_snapshot.pdf`.
- [ ] `npm run build` succeeds.
- [ ] `make audit` succeeds.
- [ ] Unit tests succeed.

## Evidence quality

- [ ] README leads with **ClinMAP-VOI v0** as the headline benchmark.
- [ ] `docs/deliverables_index.md` links the full evidence map.
- [ ] Review queue is complete for 3,971 reviewed rows.
- [ ] Metrics use the reviewed corpus only, not archived exploratory probes.
- [ ] Relation annotations and adjudications are linked and reproducible.
- [ ] Holdout panel status is `fielded_external_holdout_panel`.
- [ ] Holdout reviewer identities/contact information are not stored in git.
- [ ] Z.AI and Cloudflare supplementary probes are documented as **archive/provenance only** and excluded from benchmark scoring.

## Neutrality and privacy

- [ ] Public files do not mention target platforms, hiring campaigns, private routing, or outreach targets.
- [ ] Public files do not include patient data, PHI, clinical screenshots, employer/client content, proprietary prompts, or proprietary rubrics.
- [ ] All examples are synthetic.
- [ ] Scope states: not medical advice, diagnosis, triage, treatment guidance, clinical validation, production safety certification, or patient-care benchmark.
- [ ] Medication-related material is framed as evaluating AI response behavior, not giving medication instructions.

## Reviewer usability

- [ ] README explains the project in under 60 seconds.
- [ ] Landing page links to the repo, ClinMAP snapshot PDF, metrics, and evidence pack.
- [ ] PDF snapshot is readable and two pages.
- [ ] Profile/CV copy uses the same proof strip and does not overclaim.
- [ ] Case studies use concise reviewer-style language.

## Anti-overclaim standard

- [ ] No fake clinical leaderboard.
- [ ] No production-readiness claim.
- [ ] No peer-reviewed or clinical-validation language.
- [ ] No claim that the full corpus had multi-human review; the external panel is holdout families CMVOI-033–040 only.
- [ ] No claim that archived Z.AI/Cloudflare rows are model-performance evidence.
