# AI Response Evaluation Platform

A reproducible Python framework for evaluating AI-generated responses against explicit, transparent criteria.

![CI](https://github.com/AriPutraP2996/ai-response-evaluation-platform/actions/workflows/ci.yml/badge.svg)

---

## Overview

AI-generated responses can appear fluent and useful while still failing important requirements such as instruction following, completeness, or response quality.

This project demonstrates a small, transparent evaluation framework that converts qualitative response requirements into structured and reproducible evaluation scores.

The system is intentionally deterministic and dependency-light so that the evaluation process can be inspected, tested, and reproduced.

---

## What This Project Demonstrates

- AI response evaluation
- Rubric-based scoring
- Instruction-following evaluation
- Completeness evaluation
- Deterministic quality checks
- Structured JSON reporting
- Python development
- Automated testing
- GitHub Actions CI
- Reproducible workflows
- Technical documentation

---

## Evaluation Framework

Each response is evaluated across three dimensions:

| Dimension | Description |
|---|---|
| Instruction Following | Checks whether explicitly required phrases are present |
| Completeness | Checks whether required content markers or sections are present |
| Response Quality | Applies deterministic checks for response structure and basic quality |

The three criterion scores are combined into an overall score.

```text
Instruction Following
        │
        ▼
Completeness
        │
        ▼
Response Quality
        │
        ▼
Overall Score
        │
        ▼
Pass / Fail
