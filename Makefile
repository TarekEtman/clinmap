.PHONY: eval agreement dimensions charts v1-build v1-validate v1-schema v1-metrics v1-report v1-charts v1-explorer v1-export-openai v1-pdf v1 clinmap-voi-build clinmap-voi-validate clinmap-voi-metrics clinmap-voi clinmap-pdf install-deps audit clinmap-panel-pack clinmap-holdout-panel clinmap-frontier-pack

eval:
	python3 eval_harness/run_eval.py --cases data/synthetic_cases.jsonl --scores data/scored_examples.csv

agreement:
	python3 eval_harness/agreement_metrics.py --scores data/scored_examples.csv
	python3 eval_harness/dimension_summary.py --dimensions data/dimension_scores.csv
	python3 eval_harness/generate_charts.py --scores data/scored_examples.csv --dimensions data/dimension_scores.csv --outdir report/charts

audit:
	python3 -m unittest discover -s tests
	@! grep -RInE "Micro1|micro1|Mercor|mercor" README.md index.html src cases rubrics taxonomy data eval_harness docs eval_spec site report schemas adapters exports public model_runs clinmap_voi 2>/dev/null || (echo "Target-company mention found" && exit 1)
	python3 eval_harness/run_eval.py --cases data/synthetic_cases.jsonl --scores data/scored_examples.csv
	python3 eval_harness/v1_validate.py
	python3 eval_harness/v1_schema_validate.py
	python3 eval_harness/v1_metrics.py
	python3 eval_harness/v1_generate_charts.py
	python3 eval_harness/build_explorer_data.py
	python3 adapters/openai_evals/export_v1_openai_evals.py
	python3 clinmap_voi/validate_v0.py
	python3 clinmap_voi/metrics_v0.py
	python3 clinmap_voi/review_quality_audit.py
	python3 eval_harness/agreement_metrics.py --scores data/scored_examples.csv
	python3 eval_harness/dimension_summary.py --dimensions data/dimension_scores.csv
	python3 eval_harness/generate_charts.py --scores data/scored_examples.csv --dimensions data/dimension_scores.csv --outdir report/charts


dimensions:
	python3 eval_harness/dimension_summary.py --dimensions data/dimension_scores.csv
	python3 eval_harness/generate_charts.py --scores data/scored_examples.csv --dimensions data/dimension_scores.csv --outdir report/charts

charts:
	python3 eval_harness/generate_charts.py --scores data/scored_examples.csv --dimensions data/dimension_scores.csv --outdir report/charts


v1-build:
	python3 eval_harness/build_v1_demo_dataset.py

v1-validate:
	python3 eval_harness/v1_validate.py

v1-schema:
	python3 eval_harness/v1_schema_validate.py

v1-metrics:
	python3 eval_harness/v1_metrics.py

v1-report:
	python3 eval_harness/v1_generate_report.py

v1-charts:
	python3 eval_harness/v1_generate_charts.py

v1-explorer:
	python3 eval_harness/build_explorer_data.py

v1-export-openai:
	python3 adapters/openai_evals/export_v1_openai_evals.py

v1-pdf:
	python3 report/make_evaluation_systems_snapshot_v1_pdf.py

v1: v1-validate v1-schema v1-metrics v1-report v1-charts v1-explorer v1-export-openai

clinmap-voi-build:
	python3 clinmap_voi/build_decision_families_v0.py

clinmap-voi-validate:
	python3 clinmap_voi/validate_v0.py

clinmap-voi-metrics:
	python3 clinmap_voi/metrics_v0.py

clinmap-voi: clinmap-voi-build clinmap-voi-validate clinmap-voi-metrics

clinmap-review:
	python3 clinmap_voi/run_hosted_review_pipeline_v0.py

clinmap-review-audit:
	python3 clinmap_voi/review_quality_audit.py

clinmap-evidence:
	python3 clinmap_voi/benchmark_evidence_reports_v0.py

clinmap-panel-pack:
	python3 scripts/export_holdout_panel_pack.py

clinmap-holdout-panel:
	python3 clinmap_voi/panel_holdout_metrics_v0.py

clinmap-frontier-pack: clinmap-holdout-panel clinmap-review-audit clinmap-evidence

clinmap-hosted: clinmap-voi clinmap-review

install-deps:
	python3 -m pip install -q -r requirements.txt
	npm install

clinmap-pdf:
	@python3 -c "import reportlab" 2>/dev/null || python3 -m pip install -q -r requirements.txt
	python3 report/make_clinmap_voi_v0_snapshot_pdf.py
