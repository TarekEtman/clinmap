# Workspace setup

## One folder — use this

```text
/Users/nati/Documents/JOB/ClinMAP
```

Open **only** this folder in Cursor, VS Code, or Grok (not the parent `JOB` folder).

## Quick open (Terminal)

```bash
open /Users/nati/Documents/JOB/ClinMAP
```

## VS Code / Cursor workspace file

Double-click or open:

`ClinMAP/ClinMAP.code-workspace`

## Where things live

| What | Path |
|------|------|
| PDF snapshot | `report/clinmap_voi_v0_snapshot.pdf` |
| QA audit | `report/clinmap_voi_review_quality_audit.md` |
| Producer | `docs/PRODUCER.md` |
| Index | `docs/deliverables_index.md` |
| Landing page | `npm run dev` from repo root |

## Refresh benchmark reports

```bash
cd /Users/nati/Documents/JOB/ClinMAP
make clinmap-frontier-pack
make clinmap-pdf
```