from __future__ import annotations

import json
from pathlib import Path

from src.evaluator import score_response


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample_responses.json"


def main() -> None:
    records = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    print("AI Response Evaluation Report")
    print("=" * 32)

    for record in records:
        result = score_response(
            prompt=record["prompt"],
            response=record["response"],
            expected_topics=record["expected_topics"],
            instruction=record.get("instruction", ""),
        )
        print(f"{record['id']}: overall={result.overall}/5")
        print(
            "  "
            f"relevance={result.relevance}, "
            f"completeness={result.completeness}, "
            f"clarity={result.clarity}, "
            f"instruction_following={result.instruction_following}"
        )


if __name__ == "__main__":
    main()
