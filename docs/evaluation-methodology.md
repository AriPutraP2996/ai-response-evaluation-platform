# Evaluation Methodology

## Purpose

This project demonstrates how explicit response requirements can be converted into deterministic, inspectable evaluation signals.

The methodology is intentionally small so that every score can be traced to a visible rule.

## Dimensions

### Instruction Following

The evaluator checks whether required phrases appear in the response.

```text
matched required phrases / total required phrases × 100
```

### Completeness

The evaluator checks whether required content markers appear in the response.

```text
matched required markers / total required markers × 100
```

### Response Quality

The evaluator checks observable text properties:

- non-empty response
- minimum response length
- longer-form response length
- sentence punctuation
- paragraph separation
- absence of repeated spaces

These checks are deliberately simple and deterministic.

### Overall Score

The current implementation uses an equal-weight mean:

```text
(instruction + completeness + quality) / 3
```

The result is rounded to two decimal places.

### Pass Threshold

A response passes when its overall score is greater than or equal to the configured threshold.

The default threshold is 70.

## What This Method Does Not Claim

This evaluator does not determine:

- factual correctness
- semantic equivalence
- truthfulness
- safety
- reasoning quality
- real-world usefulness
- production readiness

Those properties require additional evidence, reference data, model-assisted evaluation, human review, or a combination of methods.

## Why Keep It Deterministic?

A transparent baseline provides a useful foundation for later experiments. More sophisticated evaluators can be compared against the same dataset and baseline rules rather than replacing the baseline with an opaque score.

## Extension Path

Future versions can introduce:

1. weighted criteria
2. reference-answer comparison
3. semantic similarity
4. evidence-aware factuality checks
5. model-assisted judging
6. calibration against human labels
7. benchmark datasets and experiment tracking

Each extension should preserve reproducibility and document its assumptions.
