from pathlib import Path

import pytest

from src.evaluator import EvaluationResult, evaluate_response
from src.report import build_markdown_report, build_report, save_markdown_report, save_report


def test_evaluate_response_returns_structured_result():
    result = evaluate_response(
        "Data validation is important because accurate and complete "
        "data supports reliable analysis.",
        required_phrases=["data validation", "accurate", "complete"],
        required_sections=["important", "data"],
        sample_id="response-001",
    )

    assert isinstance(result, EvaluationResult)
    assert result.sample_id == "response-001"
    assert result.instruction_following == 100.0
    assert result.completeness == 100.0
    assert result.overall_score > 0
    assert result.passed is True


def test_missing_required_phrase_reduces_instruction_score():
    result = evaluate_response(
        "This response explains data quality.",
        required_phrases=["data validation", "accurate", "complete"],
    )

    assert result.instruction_following < 100.0


def test_missing_required_section_reduces_completeness():
    result = evaluate_response(
        "The workflow validates incoming data.",
        required_sections=["workflow", "quality", "report"],
    )

    assert result.completeness < 100.0


def test_blank_requirements_are_ignored():
    result = evaluate_response(
        "Data validation improves accuracy.",
        required_phrases=["data validation", "", "  "],
        required_sections=["accuracy", ""],
    )

    assert result.instruction_following == 100.0
    assert result.completeness == 100.0


def test_empty_response_scores_zero():
    result = evaluate_response("")

    assert result.instruction_following == 0.0
    assert result.completeness == 0.0
    assert result.response_quality == 0.0
    assert result.overall_score == 0.0
    assert result.passed is False


def test_invalid_threshold_raises_error():
    with pytest.raises(ValueError):
        evaluate_response("Valid response.", pass_threshold=101)


def test_non_string_response_raises_error():
    with pytest.raises(TypeError):
        evaluate_response(None)  # type: ignore[arg-type]


def test_report_aggregates_results():
    first = evaluate_response(
        "Data validation is important for accurate and complete data.",
        sample_id="response-001",
    )
    second = evaluate_response(
        "Automated testing provides repeatable verification.",
        sample_id="response-002",
    )

    report = build_report([first, second])

    assert report["count"] == 2
    assert 0 <= report["average_overall_score"] <= 100
    assert 0 <= report["pass_rate"] <= 100
    assert len(report["evaluations"]) == 2


def test_empty_report_is_valid():
    report = build_report([])

    assert report["count"] == 0
    assert report["average_overall_score"] == 0.0
    assert report["pass_rate"] == 0.0
    assert report["evaluations"] == []


def test_markdown_report_contains_summary_and_samples():
    result = evaluate_response("A complete response.", sample_id="response-001")

    markdown = build_markdown_report([result])

    assert "# AI Response Evaluation Report" in markdown
    assert "response-001" in markdown
    assert "Overall" in markdown


def test_report_files_are_written(tmp_path: Path):
    result = evaluate_response("A complete response.", sample_id="response-001")

    json_path = save_report([result], tmp_path / "report.json")
    markdown_path = save_markdown_report([result], tmp_path / "report.md")

    assert json_path.exists()
    assert markdown_path.exists()
    assert "response-001" in json_path.read_text(encoding="utf-8")
    assert "response-001" in markdown_path.read_text(encoding="utf-8")
