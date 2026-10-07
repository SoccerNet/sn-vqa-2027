#!/usr/bin/env python3
"""Score OSL Streaming VQA submissions locally or in CodaBench."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
import sys
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
            answers[key] = {
                "answer": None if answer == "" else answer,
                "metadata": question.get("metadata", {}),
            }
    return answers


def metadata_value(question: dict[str, Any], prediction: dict[str, Any], field: str) -> Any:
    """Read taxonomy metadata from the GT question, then the prediction question."""
    for record in (question, prediction):
        metadata = record.get("metadata")
        if isinstance(metadata, dict):
            value = metadata.get(field)
            if value is not None:
                return value
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


def score(
    reference: dict[str, Any], submission: dict[str, Any], average_by: str = "subcategory"
) -> dict[str, float | int]:
    result = calculate_scores(reference, submission, average_by)
    scores: dict[str, float | int] = {
        f"{group.replace(' ', '_')}_accuracy":
            100.0 * result["correct"][group] / result["totals"][group]
        for group in result["groups"]
        if result["totals"][group]
    }
    scores["score"] = 100.0 * result["average"]
    scores["unanswered"] = result["unanswered"]
    return scores


def print_report(result: dict[str, Any], average_by: str) -> None:
    print("Streaming VQA evaluation")
    print("=" * 42)
    for group in result["groups"]:
        if not result["totals"][group]:
            print(f"{group:<28} N/A (0 questions)")
            continue
        label = group.upper() if average_by == "category" else group
        correct, total = result["correct"][group], result["totals"][group]
        print(f"{label:<28} {correct:>3}/{total:<3}  {correct / total:.2%}")
    print("-" * 42)
    average_label = (
        "Average across 4 categories"
        if average_by == "category"
        else "Average across 6 subcategories"
    )
    print(f"{average_label}: {result['average']:.2%}")
    print(f"Unanswered: {result['unanswered']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare an OSL Streaming VQA submission with a labeled benchmark JSON."
    )
    parser.add_argument("predictions", nargs="?", type=Path, help="OSL prediction JSON")
    parser.add_argument("benchmark", nargs="?", type=Path, help="OSL ground-truth JSON")
    parser.add_argument("--input", type=Path, default=Path("/app/input"))
    parser.add_argument("--output", type=Path, default=Path("/app/output"))
    parser.add_argument(
        "--average-by",
        choices=("subcategory", "category"),
        default="subcategory",
        help="Use the unweighted average by subcategory (default) or by category",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if (args.predictions is None) != (args.benchmark is None):
        raise SystemExit("Provide both prediction and ground-truth paths, or neither.")

    try:
        if args.predictions is not None:
            result = calculate_scores(
                load_json(args.benchmark), load_json(args.predictions), args.average_by
            )
            print_report(result, args.average_by)
            return 0

        args.output.mkdir(parents=True, exist_ok=True)
        output = args.output / "scores.json"
        output.unlink(missing_ok=True)
        result = score(
            load_json(args.input / "ref" / "benchmark.json"),
            load_json(args.input / "res" / "predictions.json"),
            args.average_by,
        )
        output.write_text(json.dumps(result, allow_nan=False), encoding="utf-8")
        print("Scoring completed successfully.")
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as error:
        if args.predictions is not None:
            raise SystemExit(f"Evaluation error: {error}") from error
        print("Scoring failed: check OSL JSON structure, IDs, and predictions.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
