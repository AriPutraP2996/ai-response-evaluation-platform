"""Reporting utilities for evaluation results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .evaluator import EvaluationResult


def build_report(
    evaluations: list[EvaluationResult],
) -> dict[str, Any]:
    """Build a structured report from evaluation results."""
    if not evaluations:
        return {
            "count": 0,
            "average_overall_score": 0.0,
            "pass_rate": 0.0,
            "evaluations": [],
        }

    average_score = round(
        sum(item.overall_score for item in evaluations)
        / len(evaluations),
        2,
    )

    passed_count = sum(item.passed for item in evaluations)

    pass_rate = round(
        (passed_count / len(evaluations)) * 100,
        2,
    )

    return {
        "count": len(evaluations),
        "average_overall_score": average_score,
        "pass_rate": pass_rate,
        "evaluations": [
            item.to_dict()
            for item in evaluations
        ],
    }


def save_report(
    evaluations: list[EvaluationResult],
    output_path: str | Path,
) -> Path:
    """Build and save a JSON report."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    report = build_report(evaluations)

    path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    return path
