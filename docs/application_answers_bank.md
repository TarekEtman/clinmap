# Application Answers Bank - AI Evaluation / Human Data / Clinical Safety Roles

Use these answers as modular copy. Keep the link target neutral: `Clinical Model Behavior Evaluation Lab`.

## 1. Short profile summary

Licensed dentist and Global Health MPP focused on healthcare-domain model evaluation: clinical safety review, response ranking, rubric calibration, missing-context analysis, and concise evaluator rationales. I built a neutral synthetic proof system that turns ambiguous healthcare prompts into structured evaluation data: cases, responses, annotations, adjudications, metrics, and a reviewer-facing snapshot.

## 2. Why this role

I am strongest where model evaluation requires more than fluency review. In healthcare-domain prompts, the dangerous answer often sounds calm and reasonable while missing context, under-escalating risk, approving medication too casually, or inventing certainty. My clinical background helps me catch that failure pattern, and my evaluation experience helps me convert the judgment into consistent scores, rankings, and rationales.

## 3. Relevant evaluation experience

I have reviewed medical AI responses, ranked LLM outputs, written structured rationales, and worked with rubric-based scoring. My focus is clinical-safety judgment: false reassurance, escalation omissions, medication-context gaps, unsupported claims, scope overreach, and rationales that do not actually support the score. I also built a public synthetic evaluation lab showing separated cases, responses, annotations, adjudications, metrics, charts, and an evaluation card.

## 4. Healthcare-domain evaluator answer

My fit is healthcare-domain evaluation rather than generic annotation. As a licensed dentist with global health training, I am comfortable identifying risk-changing context, unsafe certainty, and patient-facing phrasing that sounds helpful but is not safe. I do not position myself as a physician or as a source of patient-specific medical advice; the value I bring is model-output review, rubric calibration, and safety-aware response ranking.

## 5. Rubric calibration answer

I approach rubric calibration by separating the surface quality of an answer from its safety behavior. A fluent response can still fail if it reassures too early, omits escalation, approves medication without context, or cites details absent from the prompt. I use explicit dimensions, severity caps, failure tags, and concise rationales so another reviewer can understand the decision without re-deriving it from scratch.

## 6. RLHF / response-ranking answer

For pairwise response ranking, I first identify the highest-impact failure mode: safety, factuality, missing context, scope control, or usefulness. I do not automatically prefer the longest or most empathetic response. I prefer the response that handles uncertainty honestly, avoids overclaiming, routes appropriately when risk is present, and remains useful when the prompt is low acuity.

## 7. Evaluation systems / engineering-adjacent answer

I produce evaluation systems, not one-off labels. For **ClinMAP-VOI v0** I designed metamorphic decision families (40/320/280), ran hosted multi-model collection with versioned manifests, built the review queue schema, led primary review on 3,971 responses, relation annotations (3,219), adjudication, QA audit (pass), and a frontier evidence pack (Wilson CIs, discrimination, failure atlas). Supporting v1 demo: separated objects, validation scripts, charts, CI/audit checks, PDF snapshot. Goal: make expert judgment inspectable, frozen, and reproducible under explicit claim boundaries.

## 8. Strengths answer

My strongest strengths are clinical safety judgment, precision under ambiguity, and concise rationales. I am good at spotting the answer that sounds plausible but silently changes the question, lowers risk without evidence, or gives a clean explanation for a conclusion the prompt does not support.

## 9. Weakness / limitation answer

I am careful not to overclaim medical authority. My background is dentistry and global health, not physician practice across all specialties. For general medical evaluation, I focus on response safety, missing context, escalation boundaries, evidence quality, and rubric application. When a task requires specialist physician judgment, I would escalate or defer according to the project protocol.

## 10. Portfolio link description

**ClinMAP-VOI v0** (producer: Tarek Etman): hosted metamorphic healthcare benchmark — 40 families / 320 variants / 280 relations; 3,971 reviewed responses across 17 models; relation annotations; QA audit pass; pseudonymous external holdout panel (two independent reviewers) + disagreement vignettes; frontier evidence pack. Two-page reviewer PDF + reproducible repo. Synthetic only; not clinical validation. Supporting 48-case v1 demo (explorer, harness).

## 11. Ultra-short version

Licensed dentist + Global Health MPP specializing in healthcare-domain AI evaluation: clinical safety review, RLHF response ranking, rubric calibration, false reassurance detection, missing-context analysis, and concise evaluator rationales. Built a synthetic evaluation lab with structured data, validation, metrics, charts, and a reviewer snapshot.

## 12. Frontier-eval positioning version

I am interested in model evaluation work where human judgment becomes structured evidence: metamorphic probe design, hosted runs, policy labeling, relation consistency, rubric calibration, and honest limitations. ClinMAP-VOI v0 shows that end-to-end on synthetic healthcare probes with public metrics and audit gates—not clinical validation claims.
