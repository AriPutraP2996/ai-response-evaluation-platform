"""Core rubric-based evaluation logic.

The evaluator is intentionally deterministic and dependency-light.
It evaluates an AI-generated response against explicit criteria:

- instruction following
- completeness
- response quality

The scoring approach is designed to be transparent and reproducible.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class EvaluationResult:
    """Structured result returned by the evaluator."""

    instruction_following: float
    completeness: float
    response_quality: float
    overall_score: float
    passed: bool
    sample_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return the evaluation result as a dictionary."""
        return asdict(self)


def _clamp_score(value: float) -> float:
    """Keep a score inside the supported 0-100 range."""
    return max(0.0, min(100.0, float(value)))


def _clean_requirements(items: list[str] | None) -> list[str]:
    """Remove blank requirements so they cannot count as accidental matches."""
    if not items:
        return []
    return [item.strip() for item in items if isinstance(item, str) and item.strip()]


def _score_instruction_following(
    response: str,
    required_phrases: list[str] | None = None,
) -> float:
    """Score whether the response contains explicit required phrases."""
    if not response.strip():
        return 0.0

    phrases = _clean_requirements(required_phrases)
    if not phrases:
        return 100.0

    normalized_response = response.casefold()
    matches = sum(
        1 for phrase in phrases if phrase.casefold() in normalized_response
    )

    return _clamp_score((matches / len(phrases)) * 100)


def _score_completeness(
    response: str,
    required_sections: list[str] | None = None,
) -> float:
    """Score whether required content markers are present."""
    if not response.strip():
        return 0.0

    sections = _clean_requirements(required_sections)
    if not sections:
        return 100.0

    normalized_response = response.casefold()
    matches = sum(
        1 for section in sections if section.casefold() in normalized_response
    )

    return _clamp_score((matches / len(sections)) * 100)


def _score_response_quality(response: str) -> float:
    """Apply simple deterministic checks to observable response properties.

    This is not an LLM-based quality judgment and does not establish factual
    correctness. It checks basic structure, length, punctuation, and spacing.
    """
    text = response.strip()

    if not text:
        return 0.0

    score = 60.0

    if len(text) >= 40:
        score += 10.0

    if len(text) >= 100:
        score += 10.0

    if any(character in text for character in ".!?"):
        score += 10.0

    if "\n\n" in text:
        score += 5.0

    if "  " not in text:
        score += 5.0

    return _clamp_score(score)


def evaluate_response(
    response: str,
    *,
    required_phrases: list[str] | None = None,
    required_sections: list[str] | None = None,
    pass_threshold: float = 70.0,
    sample_id: str | None = None,
) -> EvaluationResult:
    """Evaluate an AI-generated response.

    Args:
        response: Response text to evaluate.
        required_phrases: Phrases that should appear in the response.
        required_sections: Content markers that should appear in the response.
        pass_threshold: Minimum overall score required to pass.
        sample_id: Optional identifier carried into the structured report.

    Raises:
        TypeError: If response is not a string.
        ValueError: If pass_threshold is outside the 0-100 range.
    """
    if not isinstance(response, str):
        raise TypeError("response must be a string")

    if not 0 <= pass_threshold <= 100:
        raise ValueError("pass_threshold must be between 0 and 100")

    instruction_score = _score_instruction_following(response, required_phrases)
    completeness_score = _score_completeness(response, required_sections)
    quality_score = _score_response_quality(response)

    overall_score = round(
        (instruction_score + completeness_score + quality_score) / 3,
        2,
    )

    return EvaluationResult(
        instruction_following=round(instruction_score, 2),
        completeness=round(completeness_score, 2),
        response_quality=round(quality_score, 2),
        overall_score=overall_score,
        passed=overall_score >= pass_threshold,
        sample_id=sample_id,
    )
