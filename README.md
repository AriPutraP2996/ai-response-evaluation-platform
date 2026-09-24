# AI Response Evaluation Platform

A reproducible Python framework for evaluating AI-generated responses against explicit, transparent criteria.

![CI](https://github.com/AriPutraP2996/ai-response-evaluation-platform/actions/workflows/ci.yml/badge.svg)

## Overview

AI-generated responses can be fluent and useful while still failing explicit requirements. This project demonstrates a small, deterministic evaluation pipeline that converts response requirements into structured scores and machine-readable reports.

The design intentionally favors:

- transparent scoring rules
- deterministic behavior
- dependency-light Python
- automated tests
- reproducible execution
- CI verification

## What This Project Demonstrates

- Rubric-based AI response evaluation
- Instruction-following checks
- Completeness checks
- Deterministic response-quality checks
- Structured JSON reporting
- Human-readable Markdown reporting
- Python automation
- Automated testing with pytest
- GitHub Actions CI
- Reproducible evaluation workflows

## Evaluation Dimensions

| Dimension | What is checked |
|---|---|
| Instruction Following | Presence of explicitly required phrases |
| Completeness | Presence of required content markers |
| Response Quality | Observable properties such as length, punctuation, and whitespace |
| Overall Score | Mean of the three dimension scores |
| Pass / Fail | Overall score compared with a configurable threshold |

Scores are normalized to a 0-100 scale.

> The response-quality checks are intentionally deterministic. They do not establish factual correctness or replace human/LLM-based evaluation.

## Architecture

```text
data/sample_responses.json
          |
          v
   run_evaluation.py
          |
          v
    src/evaluator.py
          |
          v
 EvaluationResult
          |
          v
      src/report.py
       /        \
      v          v
 JSON report   Markdown report
          |
          v
   GitHub Actions CI
```

## Quick Start

Requirements:

- Python 3.11+
- pip

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the test suite:

```bash
python -m pytest -q
```

Run the evaluation pipeline:

```bash
python run_evaluation.py
```

The pipeline reads:

```text
data/sample_responses.json
```

and generates:

```text
reports/evaluation_report.json
reports/evaluation_report.md
```

Generated reports are intentionally ignored by Git because they are reproducible build artifacts.

## CLI Options

The pipeline supports configurable input, output, and pass threshold:

```bash
python run_evaluation.py \
  --input data/sample_responses.json \
  --output reports/evaluation_report.json \
  --markdown-output reports/evaluation_report.md \
  --threshold 70
```

## Example Output

```text
response-001: score=96.67, passed=True
response-002: score=96.67, passed=True
response-003: score=96.67, passed=True

JSON report: .../reports/evaluation_report.json
Markdown report: .../reports/evaluation_report.md
```

The exact score depends on the dataset and rubric configuration.

## Dataset Schema

Each evaluation sample follows this structure:

```json
{
  "id": "response-001",
  "prompt": "Explain why data validation is important.",
  "response": "Generated response text...",
  "required_phrases": [
    "data validation",
    "accurate"
  ],
  "required_sections": [
    "important",
    "data"
  ]
}
```

This makes the evaluation inputs explicit and easy to extend.

## Testing

The test suite covers:

- structured evaluation results
- instruction-following failures
- completeness failures
- empty responses
- invalid thresholds
- invalid response types
- blank requirement handling
- report aggregation
- Markdown report generation
- report file creation

Run:

```bash
python -m pytest -q
```

## Continuous Integration

Every push to `main` and every pull request targeting `main` runs:

1. dependency installation
2. automated tests
3. the executable evaluation pipeline
4. evaluation report artifact generation

This ensures that both the evaluator and the end-to-end pipeline remain executable.

## Project Structure

```text
ai-response-evaluation-platform/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   └── sample_responses.json
├── src/
│   ├── __init__.py
│   ├── evaluator.py
│   └── report.py
├── tests/
│   └── test_evaluator.py
├── .gitignore
├── README.md
├── requirements.txt
└── run_evaluation.py
```

## Design Principles

### 1. Transparency

Each score comes from visible deterministic rules rather than an opaque model judgment.

### 2. Reproducibility

The same response and rubric inputs produce the same result.

### 3. Testability

Core evaluation and reporting behavior is covered by automated tests.

### 4. Separation of Concerns

Evaluation logic, reporting, test data, and CI configuration are kept separate.

### 5. Honest Scope

This project does not claim to solve factuality, semantic correctness, safety, or production-scale evaluation. Those require additional evidence, reference data, or model-assisted/human review.

## Limitations

The current evaluator is intentionally small. Phrase matching does not understand synonyms or semantic equivalence, and deterministic quality checks cannot judge whether a response is factually correct.

A stronger production-oriented system could add:

- weighted rubrics
- semantic similarity checks
- reference-answer comparison
- factual-evidence verification
- larger benchmark datasets
- experiment tracking
- model-assisted judging with calibration
- richer analytics

Those capabilities are future extensions rather than claims about the current implementation.

## Why This Project Exists

The project demonstrates practical skills in turning qualitative AI-response requirements into an inspectable software workflow:

```text
Requirement
    ↓
Evaluation rubric
    ↓
Deterministic scoring
    ↓
Structured result
    ↓
Automated report
    ↓
CI verification
```

## Author

**Ari Putra**

Focus areas:

- AI Evaluation
- Data Quality
- Python Automation
- Data Research
