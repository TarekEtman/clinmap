# START HERE — ClinMAP

**Project folder (only this one):**

`/Users/nati/Documents/JOB/ClinMAP`

Do not use sibling mock/rehearsal folders for publication or claims.

## Open these first

| File | What |
|------|------|
| [`report/clinmap_voi_v0_snapshot.pdf`](report/clinmap_voi_v0_snapshot.pdf) | 2-page benchmark summary |
| [`report/clinmap_voi_review_quality_audit.md`](report/clinmap_voi_review_quality_audit.md) | QA pass / metrics |
| [`docs/profile_signal_pack.md`](docs/profile_signal_pack.md) | **Skills + LinkedIn/CV paste blocks** |
| [`docs/PRODUCER.md`](docs/PRODUCER.md) | What Tarek produced |
| [`docs/deliverables_index.md`](docs/deliverables_index.md) | Full map |

## Folders (simple)

- **`report/`** — PDFs and metrics markdown  
- **`docs/`** — protocols, LinkedIn copy, application packet  
- **`data/clinmap_voi_v0/`** — relations, holdout, QC jsonl  
- **`model_runs/review_queues/`** — your 3971-row review CSV  

Finder: **Go to Folder** (⌘⇧G) → paste `/Users/nati/Documents/JOB/ClinMAP/report`

## Publish → signal (execution order)

1. `make clinmap-pdf` · `npm run build` · `make audit`
2. Push repo to GitHub · enable Pages (workflow in `.github/workflows/deploy-pages.yml`)
3. Verify `SITE.repoUrl` in `src/App.tsx` matches the live repo · rebuild if changed
4. LinkedIn / CV — paste from `docs/profile_copy_neutral.md`
5. One post — `docs/linkedin_technical_post.md`
6. Outreach only after you approve (no auto-send)
