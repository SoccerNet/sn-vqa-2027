#!/usr/bin/env python3
"""Evaluate an OSL Streaming VQA submission against a labeled benchmark."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


CATEGORIES = ("dim1", "dim2", "dim3", "dim4")
SUBCATEGORIES = (
    "counting",
    "recall_event_time",
    "recall_event_player",
    "event_team",
    "event_player",
    "causal reasoning",
)


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return payload


def benchmark_questions(payload: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    questions: dict[tuple[str, str], dict[str, Any]] = {}
    for sample in payload.get("data", []):
        sample_id = sample.get("id")
        if not sample_id:
            raise ValueError("Benchmark contains a sample without an id")
        for question in sample.get("streaming_vqa", []):
            question_id = question.get("id")
            key = (sample_id, question_id)
            if not question_id:
                raise ValueError(f"{sample_id}: question without an id")
            if key in questions:
                raise ValueError(f"Duplicate benchmark question: {sample_id}/{question_id}")
            if question.get("correct_option_id") is None:
                raise ValueError(f"Missing ground-truth answer: {sample_id}/{question_id}")
            questions[key] = question
    if not questions:
        raise ValueError("Benchmark contains no questions")
    return questions


def submitted_answers(payload: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    answers: dict[tuple[str, str], dict[str, Any]] = {}
    for sample in payload.get("data", []):
        sample_id = sample.get("id")
        if not sample_id:
            raise ValueError("Submission contains a sample without an id")
        questions = sample.get("streaming_vqa")
        if not isinstance(questions, list):
            raise ValueError(f"{sample_id}: submission must use OSL streaming_vqa questions")
        for question in questions:
            question_id = question.get("id")
            key = (sample_id, question_id)
            if not question_id:
                raise ValueError(f"{sample_id}: submitted question without an id")
            if key in answers:
                raise ValueError(f"Duplicate submitted question: {sample_id}/{question_id}")
            if "prediction" not in question:
                raise ValueError(f"Missing prediction: {sample_id}/{question_id}")
            answer = question["prediction"]
            # Treat an empty string as unanswered, equivalent to JSON null.
            answers[key] = {
                "answer": None if answer == "" else answer,
                "metadata": question.get("metadata", {}),
            }
    return answers


def format_score(correct: int, total: int) -> str:
    accuracy = correct / total if total else 0.0
    return f"{correct:>3}/{total:<3}  {accuracy:.2%}"


def metadata_value(question: dict[str, Any], prediction: dict[str, Any], field: str) -> Any:
    """Read taxonomy metadata from the GT question, then the prediction question."""
    for record in (question, prediction):
        metadata = record.get("metadata")
        if isinstance(metadata, dict):
            value = metadata.get(field)
            if value is not None:
                return value
            # Older test files stored category labels as metadata.dimension.
            if field == "category":
                value = metadata.get("dimension")
                if value is not None:
                    return value
    return None


def calculate_scores(
    reference: dict[str, Any], submission: dict[str, Any], average_by: str = "subcategory"
) -> dict[str, Any]:
    if average_by not in ("subcategory", "category"):
        raise ValueError(f"Unknown averaging mode: {average_by}")
    benchmark = benchmark_questions(reference)
    predictions = submitted_answers(submission)

    expected_keys = set(benchmark)
    submitted_keys = set(predictions)
    missing = sorted(expected_keys - submitted_keys)
    extra = sorted(submitted_keys - expected_keys)
    if missing:
        formatted = ", ".join(f"{sample}/{question}" for sample, question in missing)
        raise ValueError(f"Missing {len(missing)} required prediction(s): {formatted}")
    if extra:
        formatted = ", ".join(f"{sample}/{question}" for sample, question in extra)
        raise ValueError(f"Found {len(extra)} unknown prediction(s): {formatted}")

    totals: dict[str, int] = defaultdict(int)
    correct: dict[str, int] = defaultdict(int)
    unanswered = 0

    groups = SUBCATEGORIES if average_by == "subcategory" else CATEGORIES
    for key, question in benchmark.items():
        group = metadata_value(question, predictions[key], average_by)
        if group not in groups:
            raise ValueError(f"Invalid {average_by} for {key[0]}/{key[1]}: {group!r}")

        answer = predictions[key]["answer"]
        valid_options = {option.get("id") for option in question.get("options", [])}
        if answer is not None and answer not in valid_options:
            answer = None

        totals[group] += 1
        if answer is None:
            unanswered += 1
        elif answer == question["correct_option_id"]:
            correct[group] += 1

    present = [group for group in groups if totals[group]]
    if not present:
        raise ValueError("No valid questions")
    return {
        "groups": groups,
        "totals": totals,
        "correct": correct,
        "average": sum(correct[group] / totals[group] for group in present) / len(present),
        "unanswered": unanswered,
    }


def evaluate(predictions_path: Path, benchmark_path: Path, average_by: str = "subcategory") -> int:
    result = calculate_scores(load_json(benchmark_path), load_json(predictions_path), average_by)
    print("Streaming VQA evaluation")
    print("=" * 42)
    for group in result["groups"]:
        if not result["totals"][group]:
            print(f"{group:<28} N/A (0 questions)")
            continue
        label = group.upper() if average_by == "category" else group
        print(f"{label:<28} {format_score(result['correct'][group], result['totals'][group])}")
    print("-" * 42)
    average_label = "Average across 4 categories" if average_by == "category" else "Average across 6 subcategories"
    print(f"{average_label}: {result['average']:.2%}")
    print(f"Unanswered: {result['unanswered']}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare an OSL Streaming VQA submission with a labeled benchmark JSON."
    )
    parser.add_argument(
        "predictions",
        type=Path,
        help="Path to the OSL submission JSON containing per-question prediction fields",
    )
    parser.add_argument("benchmark", type=Path, help="Path to the benchmark JSON with answers")
    parser.add_argument(
        "--average-by",
        choices=("subcategory", "category"),
        default="subcategory",
        help="Report the unweighted average by subcategory (default) or by category",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        return evaluate(args.predictions, args.benchmark, args.average_by)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise SystemExit(f"Evaluation error: {error}") from error


if __name__ == "__main__":
    raise SystemExit(main())
