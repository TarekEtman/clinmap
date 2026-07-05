# PDF layout brief — fill once, reuse for every ClinMAP PDF

**Purpose:** You own the visual contract. Agents implement `report/clinmap_pdf_layout_v0.py` + `report/clinmap_pdf_style_v0.py`. Generators only place *content* into fixed bands.

**Reference PDF:** `C_Tarek_Etman_V.pdf` (repo root, gitignored)  
**Token file:** `tmp/cv_palette/colors.txt`  
**Debug overlay:** `CLINMAP_PDF_DEBUG=1 make clinmap-pdf` draws band boxes

---

## 1. Your one-time inputs (copy → fill → save)

### Page geometry
- [ ] **Page count:** 2 pages (ClinMAP snapshot) / 1 page (future one-pagers)
- [ ] **Match CV margins:** yes — ~0.45–0.55 in
- [ ] **Column split:** left 2.05 in sidebar · right fluid (CV-style)

### Page 1 band order (top → bottom)
| Band | Content | Your OK? |
|------|---------|----------|
| Header | Running name + doc title + page count | ☐ |
| Title | Name/title + hook \| producer/QA/repo (paired rows) | ☐ |
| Stats | **4** proof numbers (not 5) — see below | ☐ |
| Two-col A | Left: Producer, Corpus · Right: What this is, Methodology | ☐ |
| Two-col B | Left: Scoring dims · Right: Claim boundary, Artifacts, Run ID | ☐ |
| Full | Model table (all models, ruled) | ☐ |
| Full | Review completion line | ☐ |

**Stat strip (pick 4):**  
☐ 3971 reviewed · ☐ 17 models · ☐ 3219 relations · ☐ 0.891 acc · ☐ 0.786 meta  
*If 3219 not in strip, it stays in Corpus band.*

### Page 2 band order
| Band | Content | Your OK? |
|------|---------|----------|
| Two-col A | QA audit table \| Holdout panel table | ☐ |
| Two-col B | QA gates (4 rows) \| QA gates (4 rows) + literature baseline | ☐ |
| Full | **One** pull-quote box (holdout vignette) | ☐ |
| Two-col C | Frontier outputs \| Reproducibility commands | ☐ |
| Full | How to read κ + Limitations | ☐ |

### Typography nits (check any that bother you in current PDF)
- ☐ Title block right column misaligned with left
- ☐ Stat labels wrap awkwardly
- ☐ Left/right columns uneven white space
- ☐ Model table too wide / columns misaligned
- ☐ Page 2 feels like a vertical dump (no structure)
- ☐ Pull-quote boxes too tall
- ☐ Footer too close to body
- ☐ Other: _______________________________

---

## 2. How to give feedback that sticks

**Do this (fast, unblocks forever):**

1. Open `report/clinmap_voi_v0_snapshot.pdf`
2. Reply with **band letters** only, e.g.  
   `P1 title: right column 2pt low` · `P1 two-col A: move Artifacts to right` · `P2: only one vignette box`
3. Or run debug PDF:  
   `CLINMAP_PDF_DEBUG=1 make clinmap-pdf`  
   and cite band labels drawn on the page (`title`, `two_col`, `full`)

**Avoid:** vague “make it prettier” — tie every note to a **band** in the table above.

---

## 3. Engineering rules (do not break)

| Rule | Why |
|------|-----|
| No manual `y -= 4` in generators | spacing lives in `clinmap_pdf_layout_v0.py` |
| Content changes ≠ layout changes | new metrics go in existing bands first |
| `make clinmap-pdf` must pass layout test | `tests/test_clinmap_pdf_layout.py` |
| Colors/fonts only in `clinmap_pdf_style_v0.py` | one palette |
| New PDF types copy band table here first | same engine, new content map |

---

## 4. Files map

| File | Role |
|------|------|
| `docs/pdf_layout_brief.md` | **You edit** — band order + sign-off |
| `tmp/cv_layout_spec.md` | Visual language (colors, voice) |
| `report/clinmap_pdf_style_v0.py` | Draw primitives (text, tables, quotes) |
| `report/clinmap_pdf_layout_v0.py` | Bands, columns, overflow guard |
| `report/make_clinmap_voi_v0_snapshot_pdf.py` | ClinMAP content only |
| `report/make_evaluation_systems_snapshot_v1_pdf.py` | Future: same layout engine |

---

## 5. Sign-off line (paste when happy)

```
PDF layout signed off: [date]
Bands: P1 as table §1, P2 as table §2
Stat strip: [your 4 choices]
Notes: none | [list]
```