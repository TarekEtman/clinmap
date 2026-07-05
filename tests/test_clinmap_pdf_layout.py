"""Layout contract for ClinMAP editorial PDFs."""
from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "report" / "clinmap_voi_v0_snapshot.pdf"
BRIEF = ROOT / "docs" / "pdf_layout_brief.md"


class ClinmapPdfLayoutTests(unittest.TestCase):
    def test_layout_brief_exists(self) -> None:
        self.assertTrue(BRIEF.is_file(), "docs/pdf_layout_brief.md is the user layout contract")

    def test_pdf_generates_without_overflow(self) -> None:
        proc = subprocess.run(
            ["python3", "report/make_clinmap_voi_v0_snapshot_pdf.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
        self.assertTrue(PDF.is_file())

    def test_pdf_two_pages_with_content(self) -> None:
        try:
            import fitz
        except ImportError:
            self.skipTest("PyMuPDF not installed")

        if not PDF.is_file():
            subprocess.run(["python3", "report/make_clinmap_voi_v0_snapshot_pdf.py"], cwd=ROOT, check=True)

        doc = fitz.open(PDF)
        self.assertEqual(doc.page_count, 2)
        for i, page in enumerate(doc):
            text = page.get_text()
            self.assertIn("TAREK ETMAN", text)
            self.assertGreater(len(text.strip()), 400, f"page {i + 1} looks empty")
            blocks = page.get_text("dict")["blocks"]
            ys: list[float] = []
            for b in blocks:
                if "lines" not in b:
                    continue
                for ln in b["lines"]:
                    for sp in ln["spans"]:
                        ys.append(sp["bbox"][1])
            if ys:
                span = max(ys) - min(ys)
                self.assertGreater(span, 400, f"page {i + 1} vertical fill too sparse ({span:.0f}pt)")
        doc.close()


if __name__ == "__main__":
    unittest.main()