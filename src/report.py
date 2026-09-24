"""Reporting utilities for evaluation results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .evaluator import EvaluationResult


def build_report(evaluations: list[EvaluationResult]) -> dict[str, Any]:
    """Build a structured JSON-ready report from evaluation results."""
    if not evaluations:
        return {
            "count": 0,
            "average_overall_score": 0.0,
            "pass_rate": 0.0,
            "evaluations": [],
        }

    average_score = round(
        sum(item.overall_score for item in evaluations) / len(evaluations),
        2,
    )
    passed_count = sum(item.passed for item in evaluations)
    pass_rate = round((passed_count / len(evaluations)) * 100, 2)

    return {
        "count": len(evaluations),
        "average_overall_score": average_score,
        "pass_rate": pass_rate,
        "evaluations": [item.to_dict() for item in evaluations],
    }


def build_markdown_report(evaluations: list[EvaluationResult]) -> str:
    """Build a human-readable Markdown report."""
    report = build_report(evaluations)

    lines = [
        "# AI Response Evaluation Report",
        "",
        f"- **Samples:** {report['count']}",
        f"- **Average overall score:** {report['average_overall_score']:.2f}",
        f"- **Pass rate:** {report['pass_rate']:.2f}%",
        "",
        "| Sample | Instruction | Completeness | Quality | Overall | Status |",
        "|---|---:|---:|---:|---:|---|",
    ]

    for index, item in enumerate(evaluations, start=1):
        sample = item.sample_id or f"sample-{index:03d}"
        status = "PASS" if item.passed else "FAIL"
        lines.append(
            f"| {sample} | {item.instruction_following:.2f} | "
            f"{item.completeness:.2f} | {item.response_quality:.2f} | "
            f"{item.overall_score:.2f} | {status} |"
        )

    lines.extend(
        [
            "",
            "> This report contains deterministic rubric scores. "
            "The evaluator does not establish factual correctness.",
            "",
        ]
    )

    return "\n".join(lines)


def save_report(
    evaluations: list[EvaluationResult],
    output_path: str | Path,
) -> Path:
    """Build and save a JSON report."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(build_report(evaluations), indent=2),
        encoding="utf-8",
    )
    return path


def save_markdown_report(
    evaluations: list[EvaluationResult],
    output_path: str | Path,
) -> Path:
    """Build and save a Markdown report."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        build_markdown_report(evaluations),
        encoding="utf-8",
    )
    return path
