# First git commit — ClinMAP repo

After `make clinmap-frontier-pack`, `make clinmap-pdf`, `npm run build`, `make audit`, and `python3 -m unittest discover -s tests` pass:

```bash
cd /Users/nati/Documents/JOB/ClinMAP
./scripts/stage_clinmap_v0_commit.sh --stage
git status   # confirm no .env, node_modules, .review_private, model_runs/logs, model_runs/tmp, private registry, or local CV PDF
git commit -m "ClinMAP-VOI v0: hosted benchmark, review artifacts, methodology, and landing"
```

Push only after explicit approval:

```bash
git branch -M main
git remote add origin git@github.com:TarekEtman/clinmap.git
git push -u origin main
```

If the remote already exists:

```bash
git remote set-url origin git@github.com:TarekEtman/clinmap.git
```

GitHub Pages deployment is handled by `.github/workflows/deploy-pages.yml` after Pages is configured to use GitHub Actions.
