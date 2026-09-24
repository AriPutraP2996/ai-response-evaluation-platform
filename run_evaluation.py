"""Run the sample AI response evaluation pipeline."""

from __future__ import annotations

import json
from pathlib import Path

from src.evaluator import evaluate_response
from src.report import save_report


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "sample_responses.json"
REPORT_PATH = ROOT / "reports" / "evaluation_report.json"


def main() -> None:
    """Evaluate sample responses and save a report."""
    with DATA_PATH.open("r", encoding="utf-8") as file:
        samples = json.load(file)

    evaluations = []

    for sample in samples:
        result = evaluate_response(
            sample["response"],
            required_phrases=sample.get("required_phrases"),
            required_sections=sample.get("required_sections"),
        )

        evaluations.append(result)

        print(
            f'{sample["id"]}: '
            f'score={result.overall_score:.2f}, '
            f'passed={result.passed}'
        )

    output_path = save_report(
        evaluations,
        REPORT_PATH,
    )

    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    main()
