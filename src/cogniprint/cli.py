"""Command-line interface for the CogniPrint local workstation."""

from __future__ import annotations

import argparse
from pathlib import Path

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
