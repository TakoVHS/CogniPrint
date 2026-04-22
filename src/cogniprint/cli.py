"""Command-line interface for the CogniPrint local workstation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core.analyzer import get_analyzer
from .core.profile_manager import ProfileManager
from .experiment.runner import run_experiment
from .reporting.markdown import generate_markdown_report
from .reporting.pdf import generate_pdf_report
from .study import collect_study_samples, create_study
from .workstation import collect_samples, create_run, ensure_workspace


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "handler"):
        parser.print_help()
        return 2
    return args.handler(args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cogniprint",
        description=(
            "CogniPrint local research workstation. Outputs are analytical signals "
            "for profile analysis, comparison, and reproducible experiment notes."
        ),
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path("workspace"),
        help="Workspace directory containing input, runs, reports, notes, exports, and studies.",
    )

    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init-workspace", help="Create the local research workspace directories.")
    init_parser.set_defaults(handler=_handle_init)

    run_parser = subparsers.add_parser("run", help="Analyze one or more text inputs and write a run bundle.")
    _add_input_args(run_parser)
    run_parser.add_argument("--label", help="Optional human-readable run label.")
    run_parser.add_argument("--run-id", help="Optional explicit run directory name for exact reproducibility.")
    run_parser.set_defaults(handler=_handle_run)

    compare_parser = subparsers.add_parser("compare", help="Compare a baseline text with one or more variants.")
    compare_parser.add_argument("--baseline-text", help="Inline baseline text.")
    compare_parser.add_argument("--baseline-file", type=Path, help="Baseline text file.")
    compare_parser.add_argument("--variant-text", action="append", default=[], help="Inline variant text. Repeatable.")
    compare_parser.add_argument("--variant-file", action="append", type=Path, default=[], help="Variant text file. Repeatable.")
    compare_parser.add_argument("--variant-folder", action="append", type=Path, default=[], help="Folder of variant text files. Repeatable.")
    compare_parser.add_argument(
        "--metric",
        choices=["all", "cosine", "euclidean", "manhattan", "mahalanobis", "wasserstein", "jensen-shannon"],
        default="all",
        help="Optional selected metric to highlight in comparison outputs.",
    )
    compare_parser.add_argument("--label", help="Optional human-readable run label.")
    compare_parser.add_argument("--run-id", help="Optional explicit run directory name for exact reproducibility.")
    compare_parser.set_defaults(handler=_handle_compare)

    study_parser = subparsers.add_parser("study", help="Run a named baseline-and-variants study with aggregated outputs.")
    study_parser.add_argument("--name", required=True, help="Human-readable study name.")
    study_parser.add_argument("--study-id", help="Optional explicit study directory name for scripted workflows.")
    study_parser.add_argument("--baseline-text", help="Inline baseline text.")
    study_parser.add_argument("--baseline-file", type=Path, help="Baseline text file.")
    study_parser.add_argument("--variant-text", action="append", default=[], help="Inline variant text. Repeatable.")
    study_parser.add_argument("--variant-file", action="append", type=Path, default=[], help="Variant text file. Repeatable.")
    study_parser.add_argument("--variant-folder", action="append", type=Path, default=[], help="Folder of variant text files. Repeatable.")
    study_parser.set_defaults(handler=_handle_study)

    profile_parser = subparsers.add_parser("profile", help="Compute one text profile and write JSON to stdout or file.")
    profile_sources = profile_parser.add_mutually_exclusive_group(required=True)
    profile_sources.add_argument("--text", help="Inline text to profile.")
    profile_sources.add_argument("--file", type=Path, help="Text file to profile.")
    profile_parser.add_argument("--output", "-o", type=Path, help="Optional JSON output path.")
    profile_parser.add_argument("--save", action="store_true", help="Also save the profile under workspace/profiles.")
    profile_parser.add_argument("--label", help="Label used when saving the profile.")
    profile_parser.add_argument("--similar-threshold", type=float, help="Find saved profiles at or above this cosine similarity.")
    profile_parser.set_defaults(handler=_handle_profile)

    corpus_parser = subparsers.add_parser("corpus", help="Batch profile a directory of text files.")
    corpus_parser.add_argument("--input-dir", type=Path, required=True, help="Directory containing text files.")
    corpus_parser.add_argument("--output-dir", type=Path, default=None, help="Directory for per-file JSON profile artifacts.")
    corpus_parser.add_argument("--pattern", default="*.txt", help="Glob pattern for input files.")
    corpus_parser.set_defaults(handler=_handle_corpus)

    report_parser = subparsers.add_parser("report", help="Generate a human-readable report from a study directory.")
    report_parser.add_argument("--study-dir", type=Path, required=True, help="Study artifact directory.")
    report_parser.add_argument("--format", choices=["md", "pdf"], default="md", help="Report output format.")
    report_parser.add_argument("--output", "-o", type=Path, help="Report output path.")
    report_parser.set_defaults(handler=_handle_report)

    experiment_parser = subparsers.add_parser("experiment", help="Run YAML-configured experiment workflows.")
    experiment_subparsers = experiment_parser.add_subparsers(dest="experiment_command")
    experiment_run_parser = experiment_subparsers.add_parser("run", help="Run an experiment from a YAML config file.")
    experiment_run_parser.add_argument("--config", type=Path, required=True, help="YAML experiment configuration file.")
    experiment_run_parser.set_defaults(handler=_handle_experiment_run)

    return parser


def _add_input_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--text", action="append", default=[], help="Inline text input. Repeatable.")
    parser.add_argument("--file", action="append", type=Path, default=[], help="Text file input. Repeatable.")
    parser.add_argument("--folder", action="append", type=Path, default=[], help="Folder of text files. Repeatable.")


def _handle_init(args: argparse.Namespace) -> int:
    ensure_workspace(args.workspace)
    print(f"Workspace ready: {args.workspace.resolve()}")
    return 0


def _handle_run(args: argparse.Namespace) -> int:
    samples = collect_samples(texts=args.text, files=args.file, folders=args.folder)
    run_dir = create_run(
        samples=samples,
        workspace=args.workspace,
        command_name="run",
        run_label=args.label,
        run_id=args.run_id,
        cli_args=vars(args),
    )
    print(f"Run bundle written: {run_dir.resolve()}")
    return 0


def _handle_compare(args: argparse.Namespace) -> int:
    baseline_sources = [source for source in [args.baseline_text, args.baseline_file] if source]
    if len(baseline_sources) != 1:
        raise SystemExit("Provide exactly one baseline input with --baseline-text or --baseline-file.")

    baseline = collect_samples(
        texts=[args.baseline_text] if args.baseline_text else [],
        files=[args.baseline_file] if args.baseline_file else [],
    )
    variants = collect_samples(texts=args.variant_text, files=args.variant_file, folders=args.variant_folder)
    if not variants:
        raise SystemExit("Provide at least one variant with --variant-text, --variant-file, or --variant-folder.")
    run_dir = create_run(
        samples=baseline + variants,
        workspace=args.workspace,
        command_name="compare",
        run_label=args.label,
        run_id=args.run_id,
        baseline_index=0,
        cli_args=vars(args),
        metric=args.metric,
    )
    print(f"Comparison bundle written: {run_dir.resolve()}")
    return 0


def _handle_study(args: argparse.Namespace) -> int:
    try:
        baseline, variants = collect_study_samples(
            baseline_text=args.baseline_text,
            baseline_file=args.baseline_file,
            variant_texts=args.variant_text,
            variant_files=args.variant_file,
            variant_folders=args.variant_folder,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    study_dir = create_study(
        workspace=args.workspace,
        name=args.name,
        study_id=args.study_id,
        baseline=baseline,
        variants=variants,
        cli_args=vars(args),
    )
    print(f"Study bundle written: {study_dir.resolve()}")
    return 0


def _handle_profile(args: argparse.Namespace) -> int:
    text = args.text if args.text is not None else args.file.read_text(encoding="utf-8")
    payload = get_analyzer().analyze(text)
    payload["source"] = {"type": "inline" if args.text is not None else "file", "ref": "inline" if args.text is not None else str(args.file)}
    if args.save:
        manager = ProfileManager(args.workspace / "profiles")
        label = args.label or (args.file.stem if args.file else "profile")
        saved_path = manager.save(payload, label)
        payload["saved_profile"] = str(saved_path)
    if args.similar_threshold is not None:
        manager = ProfileManager(args.workspace / "profiles")
        payload["similar_profiles"] = manager.find_similar(payload["fingerprint_vector"], args.similar_threshold)
    output = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"Profile JSON written: {args.output.resolve()}")
    else:
        print(output, end="")
    return 0


def _handle_corpus(args: argparse.Namespace) -> int:
    input_dir = args.input_dir.expanduser().resolve()
    if not input_dir.is_dir():
        raise SystemExit(f"Input directory not found: {input_dir}")
    output_dir = args.output_dir or (args.workspace / "corpus" / input_dir.name)
    output_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(path for path in input_dir.glob(args.pattern) if path.is_file())
    analyzer = get_analyzer()
    results = analyzer.analyze_batch([path.read_text(encoding="utf-8") for path in files])
    for path, payload in zip(files, results):
        payload["source"] = {"type": "file", "ref": str(path.resolve()), "name": path.name}
        out_path = output_dir / f"{path.stem}.profile.json"
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = {
        "input_dir": str(input_dir),
        "output_dir": str(output_dir.resolve()),
        "pattern": args.pattern,
        "file_count": len(files),
        "files": [str(path.resolve()) for path in files],
    }
    (output_dir / "corpus-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Corpus profiles written: {output_dir.resolve()} ({len(files)} files)")
    return 0


def _handle_report(args: argparse.Namespace) -> int:
    study_dir = args.study_dir.expanduser().resolve()
    if not study_dir.is_dir():
        raise SystemExit(f"Study directory not found: {study_dir}")
    output = args.output or Path(f"{study_dir.name}-report.{args.format}")
    if args.format == "md":
        generate_markdown_report(study_dir, output)
    else:
        generate_pdf_report(study_dir, output)
    print(f"Report written: {output.resolve()}")
    return 0


def _handle_experiment_run(args: argparse.Namespace) -> int:
    payload = _load_yaml(args.config)
    experiment_dir = run_experiment(payload, config_path=args.config.expanduser().resolve(), workspace=args.workspace)
    print(f"Experiment written: {experiment_dir.resolve()}")
    return 0


def _load_yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise SystemExit("PyYAML is required for experiment configs. Run `pip install -e .`.") from exc
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    if not isinstance(payload, dict):
        raise SystemExit("Experiment config must be a YAML mapping.")
    return payload
