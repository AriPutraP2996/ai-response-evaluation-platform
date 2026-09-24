from src.evaluator import EvaluationResult, evaluate_response
from src.report import build_report


def test_evaluate_response_returns_structured_result():
    result = evaluate_response(
        "Data validation is important because accurate and complete "
        "data supports reliable analysis.",
        required_phrases=[
            "data validation",
            "accurate",
            "complete",
        ],
        required_sections=[
            "important",
            "data",
        ],
    )

    assert isinstance(result, EvaluationResult)
    assert result.instruction_following == 100.0
    assert result.completeness == 100.0
    assert result.overall_score > 0
    assert result.passed is True


def test_missing_required_phrase_reduces_instruction_score():
    result = evaluate_response(
        "This response explains data quality.",
        required_phrases=[
            "data validation",
            "accurate",
            "complete",
        ],
    )

    assert result.instruction_following < 100.0


def test_missing_required_section_reduces_completeness():
    result = evaluate_response(
        "The workflow validates incoming data.",
        required_sections=[
            "workflow",
            "quality",
            "report",
        ],
    )

    assert result.completeness < 100.0


def test_empty_response_scores_zero():
    result = evaluate_response("")

    assert result.instruction_following == 0.0
    assert result.completeness == 0.0
    assert result.response_quality == 0.0
    assert result.overall_score == 0.0
    assert result.passed is False


def test_invalid_threshold_raises_error():
    try:
        evaluate_response("Valid response.", pass_threshold=101)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")


def test_report_aggregates_results():
    first = evaluate_response(
        "Data validation is important for accurate and complete data."
    )

    second = evaluate_response(
        "Automated testing provides repeatable verification."
    )

    report = build_report([first, second])

    assert report["count"] == 2
    assert 0 <= report["average_overall_score"] <= 100
    assert 0 <= report["pass_rate"] <= 100
    assert len(report["evaluations"]) == 2
