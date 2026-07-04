#!/usr/bin/env python3
"""Public: verify frozen review artifacts and refresh charts. Does not synthesize labels."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    from review_quality_audit import main as audit_main  # noqa: WPS433
    from generate_performance_charts_v0 import main as charts_main  # noqa: WPS433

    code = audit_main()
    charts_main()
    print(
        "ClinMAP public pipeline: artifact verification only. "
        "Review queue and relations are canonical frozen outputs."
    )
    return code


if __name__ == "__main__":
    raise SystemExit(main())