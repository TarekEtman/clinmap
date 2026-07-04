# Profile signal pack — skills, words, proof

**Use this file** when updating LinkedIn, CV, applications, bios, and Featured links.  
**Old CV shows:** reviewer throughput (850+ responses, rationales, RLHF gigs).  
**ClinMAP shows:** you **produced** a versioned benchmark — design → hosted eval → review → relations → audit → evidence.

---

## Identity shift (say this, not that)

| Old signal (CV alone) | New signal (CV + ClinMAP) |
|----------------------|---------------------------|
| Medical AI annotator | **Benchmark producer & lead domain reviewer** |
| I review responses | I **design probes, run hosted evals, and ship inspectable benchmarks** |
| RLHF contractor | **Evaluation systems + human data quality for healthcare AI** |
| Strong rationales | **Frozen queue, metamorphic relations, QA gates, reproducible metrics** |
| Clinical background | **Domain judgment encoded into rubrics, relations, and audit-safe claims** |

**One-line creator line:**  
*Licensed dentist and Global Health MPP who produced **ClinMAP-VOI v0** — a hosted metamorphic healthcare benchmark with 3,971 reviewed responses, relation annotations, QA audit pass, and frontier evidence pack.*

**Tagline (CV / hero):**  
*Hired to catch the AI answer that sounds right and isn’t — now at benchmark scale.*

---

## Proof strip (paste on LinkedIn, CV page 1, forms, email sig)

```
ClinMAP-VOI v0 · Producer: Tarek Etman
3,971 human-reviewed hosted responses · 17 models · 3,219 metamorphic relations
QA audit PASS · pseudonymous holdout panel + inspectable disagreement vignettes
40 families / 320 variants / 280 relations · synthetic only · not clinical validation
PDF: report/clinmap_voi_v0_snapshot.pdf · Repo after publish: https://github.com/TarekEtman/clinmap
```

---

## Skills your old CV does NOT show (add these)

### Evaluation systems & engineering
- Metamorphic probe design (decision families, variant types, pairwise relation constraints)
- Evaluation spec authoring (`eval_spec/`, schemas, claim boundaries)
- Hosted multi-provider model collection (run IDs, dedupe, rate-limit handling, corpus manifests)
- Review queue design (policy labels, 6 dimension scores, evidence spans, adjudication hooks)
- Relation annotation & metamorphic consistency checking (3,219 rows)
- Metrics pipeline (per-model accuracy, metamorphic pass rate, aggregate reporting)
- QA audit gates (holdout accuracy, κ vs blind protocol QC, relation integrity)
- Benchmark evidence pack (Wilson CIs, discrimination, failure atlas, gold independence)
- Holdout methodology design (dual blinded coding reads, disagreement vignettes)
- Reproducibility (validation scripts, `make audit`, run manifest + corpus SHA256)
- Publication readiness (evaluation card, dataset card, limitations docs)

### Human data quality & review ops
- Primary domain review at scale (3,971 rows, named reviewer in provenance)
- Rubric-grounded policy labeling (not vibes scoring)
- Blind protocol QC layer (κ ~0.84 vs primary — realistic band, not κ=1 theater)
- Adjudication workflow
- Reviewer rationale discipline (evidence-linked, auditable)
- Throughput with consistency (queue complete, integrity gates pass)

### Clinical-safety evaluation (domain)
- False reassurance & under-escalation detection
- Value-of-information / missing-context probes
- Medication-context & contraindication language review
- User-pressure & follow-up-correction metamorphic variants
- Scope control & uncertainty handling
- Failure taxonomy application (`taxonomy/medical_ai_failure_modes_v2.md`)
- Pharmacovigilance-informed read (BHBIA / Bioprojet training)

### Tools & stack (public-safe)
- Python (eval pipelines, ingest, metrics, PDF reports)
- JSONL/CSV data modeling, schema validation
- ReportLab / reproducible report generation
- Make-based reproducible workflows
- TypeScript / Vite (portfolio landing — modify later, not headline)
- Git hygiene, neutrality audit, public boundary discipline

---

## Skills OLD CV already shows (keep, don’t bury)

- 850+ medical AI responses reviewed (Outlier / Scale)
- 500+ structured rationales · 94% adoption · 31 reference standards
- 1,600+ general LLM rankings (DataAnnotation)
- Red-flag taxonomy → team rubric adoption
- Prompt stress tests (short patient-style history)
- Licensed dentist · 5 yrs practice · clinic management
- Global Health MPP (Sciences Po)
- Python · pandas · evidence tools · Tableau · VOSviewer
- Arabic / English / French

**Bridge sentence:**  
*Contract review taught me the failure modes; ClinMAP-VOI v0 proves I can **encode that judgment into a reproducible benchmark** other reviewers can audit.*

---

## LinkedIn — paste blocks

### Headline (recommended)
```
Healthcare-Domain AI Evaluation · ClinMAP-VOI v0 Producer (3,971 reviewed) · Metamorphic Benchmarks · Rubrics · QA Audit
```

### About — block 1 (hook)
```
The dangerous healthcare AI answer is rarely obviously wrong. It is calm, fluent, and confident too early: false reassurance, missed escalation, missing context, medication gaps, or a rationale that does not support the score.

I catch that failure mode — and I build systems that make the judgment inspectable.
```

### About — block 2 (proof)
```
I produced ClinMAP-VOI v0: a hosted metamorphic healthcare benchmark (40 families / 320 variants / 280 relations). I led primary domain review on 3,971 hosted model responses across 17 models, relation annotations, adjudication, and a post-review QA audit (PASS). Holdout panel metrics and worked disagreement vignettes are public. Synthetic probes only — not clinical validation.
```

### About — block 3 (what you do — verbs)
```
Metamorphic probe design · hosted model evaluation · rubric-based policy labeling · dimension scoring · metamorphic relation review · blind protocol QC · metrics & Wilson/evidence reporting · claim boundaries · reviewer-facing artifacts
```

### About — block 4 (fit + CTA)
```
Strongest fit: model behavior evaluation, human data quality, clinical safety evals, rubric calibration, RLHF response ranking, evaluation operations, applied eval systems (healthcare domain).

Featured after publish: ClinMAP snapshot PDF + GitHub/Pages. Open to frontier labs and expert evaluation networks.
```

### Featured titles
1. `ClinMAP-VOI v0 — Reviewer Snapshot (PDF)`
2. `Clinical Model Behavior Evaluation Lab (GitHub)`
3. `QA Audit & Holdout Methodology` (link repo docs path on GitHub)

### Experience entry (add as project)
```
ClinMAP-VOI v0 — Lead Evaluator & Framework Producer · 2026
· Designed 40 synthetic decision families and 280 metamorphic relations
· Ran hosted multi-model collection; deduped corpus; versioned run manifest
· Primary review: 3,971 responses (policy labels, 6 dimensions, rationales)
· Relation annotations (3,219) · adjudication · QA audit PASS
· Frontier evidence: Wilson CIs, discrimination, failure atlas, holdout κ
· Explicit non-clinical claim boundary throughout
```

### Skills to pin (LinkedIn)
```
Model Evaluation · Human Data Quality · Clinical Safety (AI) · Rubric Design · RLHF · Response Ranking · Metamorphic Testing · Annotation QA · Python · Evaluation Systems · Healthcare AI · Failure Mode Analysis · Data Provenance · Reproducible Research
```

---

## CV — page 1 addition (above or beside old gigs)

```
TECHNICAL PROOF — CLINMAP-VOI v0 (Producer: Tarek Etman)
Hosted metamorphic healthcare benchmark · 3,971 reviewed · 17 models · QA audit pass
PDF: report/clinmap_voi_v0_snapshot.pdf · GitHub after publish: https://github.com/TarekEtman/clinmap

· Framework: 40 families, 320 variants, 280 metamorphic relations
· Hosted eval ops, corpus dedupe, frozen review queue, relation integrity 1.0
· Blind protocol QC κ ~0.84 · pseudonymous holdout panel with inspectable disagreement cases
· Synthetic only — evaluation engineering, not clinical validation
```

---

## Signal words (use often)

**Role:** producer · lead reviewer · framework designer · evaluation engineer · domain reviewer  
**Objects:** probes · variants · relations · queue · corpus · manifest · provenance · vignettes  
**Verbs:** designed · hosted · reviewed · annotated · adjudicated · audited · validated · reproduced  
**Quality:** inspectable · frozen · versioned · bounded · reproducible · auditable · calibrated  
**Domain:** false reassurance · escalation · missing context · metamorphic · VOI · policy label  
**Trust:** claim boundary · synthetic only · not clinical validation · QA pass · explicit limits  

## Words to avoid (public)

- “Validated the model” / “clinically proven” / “safe for patients”
- “Multi-human panel on full corpus” (holdout is partial by design)
- “Perfect accuracy” / “oracle” / “100%”
- Target platform names in public repo copy (audit enforced)

---

## Gig-platform paragraph (paste in profile / cover field)

```
I produce evaluation artifacts, not just labels. ClinMAP-VOI v0: 3,971 reviewed hosted responses, named primary reviewer, κ ~0.84 vs blind protocol QC, relation integrity 1.0, evidence-linked rationales, and QA audit pass. I design probes and rubrics where the failure is false reassurance and missing escalation — the answer that sounds right but isn’t. Throughput plus consistency, with public reproducibility.
```

---

## Frontier paragraph (paste in cover / interest field)

```
I build evaluation evidence, not demos. ClinMAP-VOI v0 is a synthetic metamorphic healthcare benchmark: hosted multi-model runs, completed review queue, relation annotations, pseudonymous external holdout panel (two independent reviewers) with worked disagreement vignettes, and a frontier stats pack (Wilson CIs, discrimination, failure atlas). I care about operationalizing ambiguous safety judgment into probes, metrics, and honest limitations — without overclaiming clinical validation.
```

---

## Interview — 60-second producer story

```
I’m a licensed dentist and Global Health MPP. Contract medical-AI review taught me that the dangerous answer sounds fine — it reassures too early or misses escalation.

I wanted that judgment inspectable at scale, so I produced ClinMAP-VOI v0: forty decision families, three hundred twenty variants, two hundred eighty metamorphic relations, hosted outputs from seventeen models, and I led primary review on three thousand nine hundred seventy-one responses. We annotation-checked relations, ran blind protocol QC, passed QA audit, and fielded a pseudonymous external holdout panel where two independent reviewers completed blinded coding over multiple waves — moderate kappa is explained by two legitimate coding methodologies, with vignettes you can read.

It’s synthetic, bounded, and reproducible. That’s the kind of evaluation work I want to do — model behavior, human data quality, and safety evals with real audit trails.
```

---

## Artifact map (when they ask “show me”)

| They want | Send / link |
|-----------|-------------|
| 30-second skim | `report/clinmap_voi_v0_snapshot.pdf` |
| “Is it real?” | `report/clinmap_voi_review_quality_audit.md` |
| Model scores | `report/clinmap_voi_v0_performance_metrics.md` |
| Holdout story | `report/benchmark_evidence/clinmap_voi_holdout_panel_metrics.md` + vignettes JSON |
| What you built | `docs/PRODUCER.md` + `data/clinmap_voi_v0/benchmark_provenance.json` |
| Full repo | GitHub README → `docs/deliverables_index.md` |

---

## Execution order (no landing rebuild yet)

1. Paste LinkedIn blocks from this file  
2. Add CV page-1 proof strip + PDF link  
3. Publish GitHub + PDF  
4. Post `docs/linkedin_technical_post.md` (optional polish)  
5. **Later:** modify your previous landing page (not scratch build)  
6. Outreach only with your explicit OK