# First git commit (v1 repo)

After `make install-deps`, `make clinmap-pdf`, `npm run build`, and `make audit` pass:

```bash
cd /Users/nati/Documents/JOB/clinical-ai-eval-lab-v1
git add -A
git status   # confirm no .env, node_modules, .review_private, model_runs/logs, model_runs/tmp
git commit -m "ClinMAP-VOI v0: hosted benchmark, review artifacts, methodology, and landing"
```

Push (replace remote URL):

```bash
git remote add origin <your-github-repo-url>
git push -u origin main
```

Optional: deploy `dist/` to static hosting (GitHub Pages, etc.) after `npm run build`.