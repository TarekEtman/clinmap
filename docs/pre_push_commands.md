# Pre-push commands (run from repo root)

One-time (or after clone):

```bash
make install-deps
```

Before first public commit (local only — moves hosted review runner; review protocol modules stay public):

```bash
bash scripts/privatize_labeling_pipeline.sh
```

Public `clinmap_voi/` review protocol modules (`review_protocol_engine_v0.py`, `primary_review_policy_v0.py`, `secondary_qc_pass_v0.py`, `contract_consistency_pass_v0.py`) remain in the repo.

Then:

```bash
make clinmap-pdf
python3 -m unittest tests.test_clinmap_hosted_review_pipeline -q
npm run build
make audit
```

If `model_runs/logs/` or `model_runs/tmp/` were previously committed:

```bash
git rm -r --cached model_runs/logs model_runs/tmp HANDOFF_*.md 2>/dev/null || true
```

Then commit `.gitignore` updates and generated `report/clinmap_voi_v0_snapshot.pdf` + `public/assets/clinmap_voi_v0_snapshot.pdf`.