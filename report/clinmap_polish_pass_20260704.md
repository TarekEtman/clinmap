# ClinMAP polish pass — 2026-07-04

Scope: local repository cleanup and release-readiness QA for `/Users/nati/Documents/JOB/ClinMAP`. No publish, push, deploy, external outreach, staging, or commits were performed.

## Original strategy status

| Strategy layer | Status | Notes |
|---|---|---|
| Canonical project folder | Complete | Public docs now point to `/Users/nati/Documents/JOB/ClinMAP`; stale workspace file removed. |
| ClinMAP-VOI v0 benchmark package | Complete | 3,971 reviewed rows, 17 scored models, 3,219 relation annotations, QA pass. |
| Frontier evidence pack | Complete | `make clinmap-frontier-pack` regenerates holdout-panel metrics, QA audit, Wilson CIs, discrimination, failure atlas, and adjudication summary. |
| PDF snapshot | Complete | `make clinmap-pdf` regenerates `report/clinmap_voi_v0_snapshot.pdf` and `public/assets/clinmap_voi_v0_snapshot.pdf`. |
| Landing page build | Complete locally | `npm run build` passes; GitHub Pages workflow is present but not deployed. |
| Z.AI / Cloudflare disposition | Complete | Archived as exploratory provenance only; excluded from reviewed benchmark metrics because most OK rows have empty `response_text` and/or partial failures. |
| Profile / application copy | Ready after publish | Paste blocks now use the same proof strip and mark repo links as “after publish”. |
| GitHub publish / Pages / outreach | Not done | Requires explicit approval before push, deploy, post, or outreach. |

## Fixes made in this pass

- Rewrote `docs/public_release_checklist.md` around the ClinMAP-only release gate.
- Rewrote `docs/publishing_plan.md` to use the ClinMAP snapshot PDF, current evidence gates, and the intended repo URL.
- Updated `docs/first_git_commit.md` to use `/Users/nati/Documents/JOB/ClinMAP`, the safe staging helper, and the intended GitHub remote.
- Updated `docs/profile_copy_neutral.md` and `docs/profile_signal_pack.md` to remove stale `[PDF]` / `[repo URL]` placeholders and avoid holdout wording that could imply full-corpus multi-human review.
- Updated `docs/recruiter_snapshot.md` so the headline PDF is the ClinMAP snapshot, with v1 clearly supporting lineage only.
- Updated `START_HERE.md` and `src/App.tsx` wording around repo URL verification after publish.
- Changed `pyproject.toml` project name from `clinical-ai-eval-lab` to `clinmap`.
- Removed stale local artifacts: old empty workspace file, `.DS_Store` files, stray `71266`, old local launch scripts, and old ignored handoff file.
- Replaced `scripts/stage_clinmap_v0_commit.sh` with a guarded helper: default `--check` does not stage; `--stage` stages only after hygiene checks pass.

## Validation run

All commands below passed on 2026-07-04:

```bash
cd /Users/nati/Documents/JOB/ClinMAP
make clinmap-frontier-pack
make clinmap-pdf
npm run build
make audit
python3 -m unittest discover -s tests
./scripts/stage_clinmap_v0_commit.sh --check
```

Observed validation highlights:

- Review corpus: 3,971 rows with non-empty `response_text`.
- Main deduped hosted corpus: 5,335 rows (`ok`: 5,048; `rate_limited`: 287).
- Holdout panel status (corrected): `fielded_external_holdout_panel`.
- Package name: `clinmap`.
- New workspace file exists: `ClinMAP.code-workspace`.
- Old workspace file absent: `clinical-ai-eval-lab-v1.code-workspace`.
- Scoped stale-public-language grep returned no hits outside raw/provenance run artifacts.

## Residual old-path handling

- Verified root leftovers are absent from the working tree: `HANDOFF_HOSTED_CLINMAP_VOI_20260704.md`, `open_zed_grok.sh`, and `clinical-ai-eval-lab-v1.code-workspace`.
- Found 58 hosted-run `*_manifest.json` files preserving old absolute execution paths under `/Users/nati/Documents/JOB/clinical-ai-eval-lab`. These were intentionally **not rewritten** because they are raw execution provenance.
- Added `model_runs/outputs/hosted_clinmap_voi_v0/README.md` to explain that those manifest paths are historical provenance and that `/Users/nati/Documents/JOB/ClinMAP` is the current canonical project folder.

## Holdout claim hardening — follow-up

After reviewing the attached audit text, the public repo was hardened without accepting any claim that Tarek did not produce the work. The issue was narrower: public files used stronger holdout-panel wording than the public repository can self-prove, because private identity/source details are intentionally not stored in git.

Changes made:

- **Corrected (same day):** restored Layer C as **fielded external holdout panel** — two pseudonymous independent external reviewers; reverted downgraded “review layer” wording from an erroneous Path-B pass.
- Updated docs, report generators, stage-check guardrails, and landing-page copy to remove risky external/independent/fielded panel wording.
- Regenerated holdout metrics, review QA audit, benchmark evidence reports, and the PDF snapshot.
- Preserved producer credit: Tarek Etman remains benchmark producer, primary domain reviewer, hosted-eval lead, relation/adjudication reviewer, metrics/QA/reporting owner.

Validation after this hardening pass:

```bash
make clinmap-frontier-pack
make clinmap-pdf
npm run build
make audit
python3 -m unittest discover -s tests
./scripts/stage_clinmap_v0_commit.sh --check
```

All passed.

## Remaining work before public release

1. Review the current git diff manually.
2. If approved, run `./scripts/stage_clinmap_v0_commit.sh --stage`.
3. Commit locally.
4. Push to GitHub and enable Pages only after explicit approval.
5. Replace profile/CV paste blocks with live GitHub/Pages links after publish.
6. Send outreach only after explicit approval.
