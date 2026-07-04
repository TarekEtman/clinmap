# Publishing Plan — ClinMAP

This plan prepares the repository for public release. Do not publish, push, deploy, post, or send outreach until Tarek explicitly approves the external action.

## Release goal

Publish a neutral public proof system centered on **ClinMAP-VOI v0**: synthetic metamorphic healthcare probes, hosted multi-model outputs, human domain review, relation annotations, QA audit, holdout-panel evidence, and explicit claim boundaries. The older synthetic v1 demo remains supporting lineage only.

## Public surfaces

1. **GitHub repository**  
   Primary proof: `README.md` → ClinMAP metrics, audit, queue, methodology index (`docs/deliverables_index.md`).

2. **Landing page**  
   Static Vite build (`src/` → `dist/`) with ClinMAP headline stats and links to the PDF, metrics, evidence pack, and repository.

3. **Technical specifications**  
   - Headline: `eval_spec/clinmap_voi_eval_spec_v0.md`, `docs/clinmap_voi_annotation_protocol_v0.md`  
   - Supporting lineage: `eval_spec/clinical_model_behavior_eval_spec_v1.md`

4. **PDF snapshot**  
   Current public handout: `report/clinmap_voi_v0_snapshot.pdf` and landing-page copy at `public/assets/clinmap_voi_v0_snapshot.pdf`.

## Pre-publish checklist

Run locally:

```bash
cd /Users/nati/Documents/JOB/ClinMAP
make clinmap-frontier-pack
make clinmap-pdf
npm run build
make audit
python3 -m unittest discover -s tests
```

Must pass:

- TypeScript/Vite production build.
- Unit tests.
- Public neutrality scan.
- ClinMAP framework validation.
- Review queue / secondary pass verification.
- Holdout panel metrics from frozen panel labels.
- Benchmark evidence reports.
- PDF generation.

Manual checks:

- Open the local Vite site and inspect desktop/mobile.
- Open `report/clinmap_voi_v0_snapshot.pdf` and confirm no clipping.
- Confirm README and landing page match the current data state.
- Confirm no target-company names or outreach routing appear in public files.
- Confirm all examples are synthetic.
- Confirm Z.AI/Cloudflare are archive/provenance only, not benchmark-scored evidence.
- Confirm claim boundary is clear everywhere.

## GitHub Pages deployment recommendation

Use GitHub Actions or Pages configured for a Vite build artifact. Do not use raw-root Pages publishing with the source `index.html`, because the raw Vite entry points to `/src/main.tsx` and is not a production artifact.

The included workflow is `.github/workflows/deploy-pages.yml`. It runs `npm ci`, `npm run build`, uploads `dist/`, and uses `VITE_BASE_PATH` for project-page routing.

## Suggested GitHub publishing commands

Only run after explicit approval:

```bash
cd /Users/nati/Documents/JOB/ClinMAP
./scripts/stage_clinmap_v0_commit.sh --stage
git commit -m "ClinMAP-VOI v0: hosted benchmark, review artifacts, methodology, and landing"
git branch -M main
git remote add origin git@github.com:tareketman/clinmap.git
git push -u origin main
```

If the remote already exists, use:

```bash
git remote set-url origin git@github.com:tareketman/clinmap.git
```

## Post-publish profile links

Use the landing page as the primary public link. Use the GitHub repo when the reviewer is technical. Use the PDF snapshot for upload fields or referral attachments.

Canonical proof links after publishing:

- Repo: `https://github.com/tareketman/clinmap`
- PDF in repo: `https://github.com/tareketman/clinmap/blob/main/report/clinmap_voi_v0_snapshot.pdf`
- Pages URL: use the GitHub Pages URL shown after deployment.

## Do not publish if

- Any required gate fails.
- The landing page is visually crowded or hard to scan.
- The PDF render has clipped text.
- The repo contains target-company names, private routing language, secrets, PHI, or private reviewer identity/contact details.
- Any example could be mistaken for real patient data.
- Any language implies clinical deployment, patient-care use, peer-reviewed validation, or production safety certification.
- The README claims metrics that the current data cannot support.
- Z.AI/Cloudflare archived probes are mixed into public model-comparison claims.
