from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


@dataclass(frozen=True)
class Evaluation:
    relevance: float
    completeness: float
    clarity: float
    instruction_following: float

    @property
    def overall(self) -> float:
        return round(
            (
                self.relevance
                + self.completeness
                + self.clarity
                + self.instruction_following
            )
            / 4,
            2,
        )


def _clamp(score: float) -> float:
    return max(1.0, min(5.0, round(score, 2)))


def score_response(
    prompt: str,
    response: str,
    expected_topics: Iterable[str],
    instruction: str = "",
) -> Evaluation:
    """Apply a small deterministic demonstration rubric.

    This is intentionally simple and transparent. It is not a replacement
    for expert human evaluation.
    """
    response_lower = response.lower()
    topics = [topic.lower() for topic in expected_topics if topic.strip()]
    matched = sum(1 for topic in topics if topic in response_lower)

    relevance = 5.0 if prompt.strip() and response.strip() else 1.0
    completeness = _clamp(1.0 + 4.0 * (matched / len(topics))) if topics else 3.0

    sentences = [s for s in re.split(r"[.!?]+", response) if s.strip()]
    avg_sentence_length = (
        sum(len(s.split()) for s in sentences) / len(sentences)
        if sentences
        else 0
    )
    clarity = 5.0 if 8 <= avg_sentence_length <= 28 else 3.5
    if len(response.split()) < 8:
        clarity = 2.5

    instruction_lower = instruction.lower()
    concise_requested = "concis" in instruction_lower
    word_count = len(response.split())
    instruction_following = 5.0 if not concise_requested or word_count <= 80 else 3.0

    return Evaluation(
        relevance=relevance,
        completeness=completeness,
        clarity=clarity,
        instruction_following=instruction_following,
    )
