"""CLI entry point for the AI response evaluation pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.evaluator import evaluate_response
from src.report import save_markdown_report, save_report


ROOT = Path(__file__).resolve().parent


def _resolve_path(path: Path) -> Path:
    """Resolve relative paths from the repository root."""
    return path if path.is_absolute() else ROOT / path


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(
        description="Evaluate AI responses using a deterministic rubric."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/sample_responses.json"),
        help="Path to the JSON evaluation dataset.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/evaluation_report.json"),
        help="Path for the JSON report.",
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=Path("reports/evaluation_report.md"),
        help="Path for the Markdown report.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=70.0,
        help="Pass threshold from 0 to 100.",
    )
    return parser.parse_args()


def main() -> None:
    """Load data, evaluate responses, and save reports."""
    args = parse_args()
    input_path = _resolve_path(args.input)
    json_output = _resolve_path(args.output)
    markdown_output = _resolve_path(args.markdown_output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input dataset not found: {input_path}")

    with input_path.open("r", encoding="utf-8") as file:
        samples = json.load(file)

    if not isinstance(samples, list):
        raise ValueError("Input dataset must contain a JSON list of samples.")

    evaluations = []

    for sample in samples:
        if not isinstance(sample, dict):
            raise ValueError("Each dataset item must be a JSON object.")
        if "response" not in sample:
            raise ValueError("Each dataset item must contain 'response'.")

        result = evaluate_response(
            sample["response"],
            required_phrases=sample.get("required_phrases"),
            required_sections=sample.get("required_sections"),
            pass_threshold=args.threshold,
            sample_id=sample.get("id"),
        )
        evaluations.append(result)

        print(
            f"{sample.get('id', 'unknown')}: "
            f"score={result.overall_score:.2f}, "
            f"passed={result.passed}"
        )

    json_path = save_report(evaluations, json_output)
    markdown_path = save_markdown_report(evaluations, markdown_output)

    print(f"\nJSON report: {json_path}")
    print(f"Markdown report: {markdown_path}")


if __name__ == "__main__":
    main()
