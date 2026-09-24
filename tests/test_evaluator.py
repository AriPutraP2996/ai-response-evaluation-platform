from src.evaluator import score_response


def test_overall_score_is_average():
    result = score_response(
        prompt="Explain data validation.",
        response="Data validation checks missing and invalid values before training.",
        expected_topics=["missing", "invalid", "training"],
        instruction="Answer concisely.",
    )

    expected = round(
        (
            result.relevance
            + result.completeness
            + result.clarity
            + result.instruction_following
        )
        / 4,
        2,
    )

    assert result.overall == expected


def test_missing_response_scores_low_for_relevance():
    result = score_response(
        prompt="Explain data validation.",
        response="",
        expected_topics=["validation"],
        instruction="Answer concisely.",
    )

    assert result.relevance == 1.0
