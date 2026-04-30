from __future__ import annotations

import unittest
from pathlib import Path


class SiteLinkTests(unittest.TestCase):
    def test_site_pages_reference_evidence_and_review(self) -> None:
        site_root = Path(__file__).resolve().parents[2] / "TakoVHS.github.io"
        if not site_root.exists():
            self.skipTest("Sibling website repo is not available.")

        software = (site_root / "software" / "index.html").read_text(encoding="utf-8")
        evidence = (site_root / "evidence" / "index.html").read_text(encoding="utf-8")
        review = (site_root / "review" / "index.html").read_text(encoding="utf-8")

        for text in (software, evidence, review):
            self.assertIn("/evidence/", text)
            self.assertIn("/review/", text)

        self.assertIn("evidence/public-benchmark-v1", evidence)
        self.assertIn("evidence/statistical-validation-v1", evidence)
        self.assertIn("coverage-summary.md", review)
        self.assertIn("results-summary.md", review)


if __name__ == "__main__":
    unittest.main()
