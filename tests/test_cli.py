from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def test_inline_run_creates_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir) / "workspace"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "run",
                    "--run-id",
                    "test-inline-run",
                    "--text",
                    "CogniPrint studies compact statistical profiles of text.",
                ],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            )
            self.assertIn("Run bundle written", result.stdout)
            run_dir = workspace / "runs" / "test-inline-run"
            self.assertTrue((run_dir / "manifest.json").exists())
            self.assertTrue((run_dir / "results.json").exists())
            self.assertTrue((run_dir / "summary.md").exists())
            self.assertTrue((run_dir / "export.csv").exists())

            results = json.loads((run_dir / "results.json").read_text(encoding="utf-8"))
            manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertGreater(results["profiles"][0]["metrics"]["word_count"], 0)
            self.assertIn("not legal conclusions", results["disclaimer"])
            self.assertEqual(manifest["input_mode"], "inline")
            self.assertIn("cli_args", manifest)
            self.assertIn("environment", manifest)

    def test_compare_creates_comparison_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            workspace = temp_path / "workspace"
            baseline = temp_path / "baseline.txt"
            variant = temp_path / "variant.txt"
            baseline.write_text("A short research note with stable wording.", encoding="utf-8")
            variant.write_text("A substantially revised research note with different structure and added detail.", encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "compare",
                    "--run-id",
                    "test-compare-run",
                    "--baseline-file",
                    str(baseline),
                    "--variant-file",
                    str(variant),
                ],
                check=True,
            )
            run_dir = workspace / "runs" / "test-compare-run"
            comparisons = json.loads((run_dir / "comparisons.json").read_text(encoding="utf-8"))
            self.assertTrue(comparisons["comparisons"])
            self.assertIn("cosine_similarity", comparisons["comparisons"][0])

    def test_study_creates_aggregated_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            workspace = temp_path / "workspace"
            baseline = temp_path / "baseline.txt"
            variant = temp_path / "variant.txt"
            baseline.write_text("A baseline note for controlled perturbation analysis.", encoding="utf-8")
            variant.write_text("A revised baseline note for controlled perturbation analysis with added context.", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "study",
                    "--name",
                    "test perturbation study",
                    "--study-id",
                    "test-study",
                    "--baseline-file",
                    str(baseline),
                    "--variant-file",
                    str(variant),
                ],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            )
            self.assertIn("Study bundle written", result.stdout)
            study_dir = workspace / "studies" / "test-study"
            self.assertTrue((study_dir / "study-manifest.json").exists())
            self.assertTrue((study_dir / "aggregated-results.json").exists())
            self.assertTrue((study_dir / "aggregated-results.csv").exists())
            self.assertTrue((study_dir / "study-summary.md").exists())
            self.assertTrue((study_dir / "manuscript-note.md").exists())

            aggregated = json.loads((study_dir / "aggregated-results.json").read_text(encoding="utf-8"))
            self.assertEqual(aggregated["variant_count"], 1)
            self.assertIn("perturbation effect", aggregated["comparison_rows"][0]["interpretation"])

    def test_profile_corpus_report_and_experiment_commands(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            workspace = temp_path / "workspace"
            input_dir = workspace / "input"
            variants_dir = input_dir / "variants"
            variants_dir.mkdir(parents=True)
            original = input_dir / "original.txt"
            edited = input_dir / "edited.txt"
            variant = variants_dir / "strong.txt"
            original.write_text("A baseline research text for profile persistence.", encoding="utf-8")
            edited.write_text("A lightly edited research text for profile persistence checks.", encoding="utf-8")
            variant.write_text("A stronger variant changes length, punctuation, and local structure.", encoding="utf-8")

            profile_out = temp_path / "profile.json"
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "profile",
                    "--file",
                    str(original),
                    "--output",
                    str(profile_out),
                    "--save",
                    "--label",
                    "original",
                ],
                check=True,
            )
            self.assertTrue(profile_out.exists())
            self.assertTrue(list((workspace / "profiles").glob("*.json")))

            corpus_out = temp_path / "corpus"
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "corpus",
                    "--input-dir",
                    str(input_dir),
                    "--output-dir",
                    str(corpus_out),
                    "--pattern",
                    "*.txt",
                ],
                check=True,
            )
            self.assertTrue((corpus_out / "corpus-manifest.json").exists())
            self.assertTrue((corpus_out / "original.profile.json").exists())

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "compare",
                    "--run-id",
                    "metric-compare",
                    "--baseline-file",
                    str(original),
                    "--variant-file",
                    str(edited),
                    "--metric",
                    "mahalanobis",
                ],
                check=True,
            )
            comparison = json.loads((workspace / "runs" / "metric-compare" / "comparisons.json").read_text(encoding="utf-8"))
            self.assertEqual(comparison["comparisons"][0]["selected_metric"]["metric"], "mahalanobis")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "study",
                    "--name",
                    "report study",
                    "--study-id",
                    "report-study",
                    "--baseline-file",
                    str(original),
                    "--variant-file",
                    str(edited),
                    "--variant-folder",
                    str(variants_dir),
                ],
                check=True,
            )
            study_dir = workspace / "studies" / "report-study"
            report_md = temp_path / "report.md"
            report_pdf = temp_path / "report.pdf"
            subprocess.run(
                [sys.executable, "-m", "cogniprint", "--workspace", str(workspace), "report", "--study-dir", str(study_dir), "--format", "md", "--output", str(report_md)],
                check=True,
            )
            subprocess.run(
                [sys.executable, "-m", "cogniprint", "--workspace", str(workspace), "report", "--study-dir", str(study_dir), "--format", "pdf", "--output", str(report_pdf)],
                check=True,
            )
            self.assertIn("CogniPrint Research Report", report_md.read_text(encoding="utf-8"))
            self.assertTrue(report_pdf.read_bytes().startswith(b"%PDF-"))

            config = temp_path / "experiment.yml"
            config.write_text(
                "\n".join(
                    [
                        "name: yaml experiment",
                        f"baseline_file: {original}",
                        "variant_files:",
                        f"  - {edited}",
                        f"variant_folder: {variants_dir}",
                        f"output_dir: {temp_path / 'experiments'}",
                    ]
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [sys.executable, "-m", "cogniprint", "--workspace", str(workspace), "experiment", "run", "--config", str(config)],
                check=True,
            )
            self.assertTrue((temp_path / "experiments" / "yaml-experiment" / "experiment-manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
