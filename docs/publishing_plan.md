# Publishing Plan

This plan prepares the repository for public release. Do not publish or send outreach until the final release audit passes and Tarek explicitly approves the external action.

## Release goal

Publish a neutral public proof system and landing page centered on **ClinMAP-VOI v0** (hosted benchmark, review complete): metamorphic probes, hosted outputs, human review queue, relation metrics, QA audit, and explicit claim boundaries. The synthetic **v1 demo** remains supporting lineage (explorer, PDF snapshot).

## Public surfaces

1. **GitHub repository**  
   Primary proof: `README.md` → ClinMAP metrics, audit, queue, methodology index (`docs/deliverables_index.md`).

2. **Landing page**  
   Recruiter / hiring-manager front door (`src/` → `dist/`) with ClinMAP headline stats and links to metrics report / repo.

3. **Technical specifications**  
   - **Headline:** `eval_spec/clinmap_voi_eval_spec_v0.md`, `docs/clinmap_voi_annotation_protocol_v0.md`  
   - **Lineage:** `eval_spec/clinical_model_behavior_eval_spec_v1.md`

4. **PDF snapshot**  
   Portable v1 demo summary (`report/evaluation_systems_snapshot_v1.pdf`); optional future ClinMAP one-pager.

## Pre-publish checklist

Run locally:

```bash
npm run build
make audit
```

Must pass:

- TypeScript build.
- Unit tests.
- Public neutrality scan.
- Case and score validation.
- Agreement metrics.
- Dimension metrics.
- Chart generation.

Manual checks:

- Open the local Vite site and inspect desktop/mobile.
- Open the PDF snapshot after it is regenerated.
- Confirm no target-company names appear in public-facing files.
- Confirm all examples are synthetic.
- Confirm the scope statement is clear.
- Confirm the README and landing page match the current data state.

## GitHub Pages deployment recommendation

Use GitHub Actions or Pages configured for a Vite build artifact. Do not use `/root` branch publishing with the raw `index.html`, because the raw Vite entry points to `/src/main.tsx` and is not a static production artifact.

Recommended approach:

1. Push repository to GitHub.
2. Configure Pages source as GitHub Actions.
3. Add a deploy workflow that runs `npm ci`, `npm run build`, and uploads `dist/`.

## Suggested GitHub publishing commands

Only run after explicit approval:

```bash
git add .
git commit -m "Initial clinical model behavior evaluation lab"
git branch -M main
git remote add origin git@github.com:USERNAME/clinical-ai-eval-lab.git
git push -u origin main
```

## Post-publish profile links

Use the landing page as the primary public link. Use the GitHub repo when the reviewer is technical. Use the PDF snapshot for upload fields or referral attachments after it is regenerated and visually QA'd.

## Do not publish if

- `npm run build` or `make audit` fails.
- The landing page is visually crowded or hard to scan.
- The PDF render has clipped text.
- The repo contains target-company names or routing language.
- Any example could be mistaken for real patient data.
- Any language implies clinical deployment or patient-care use.
- The README claims metrics that the current data cannot support.
