"""CodaBench adapter for the source Streaming VQA evaluator's OSL JSON schema."""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

from eval_predictions import DIMENSIONS, benchmark_questions, load_json, metadata_value, submitted_answers


def score(reference, submission):
    benchmark = benchmark_questions(reference)
    predictions = submitted_answers(submission)
    if set(predictions) != set(benchmark):
        raise ValueError("Submission question IDs do not match the benchmark")

    totals = defaultdict(int)
    correct = defaultdict(int)
    unanswered = 0
    for key, question in benchmark.items():
        group = metadata_value(question, predictions[key], "dimension")
        if group not in DIMENSIONS:
            raise ValueError("A benchmark question has an invalid dimension")
        answer = predictions[key]["answer"]
        valid_options = {option.get("id") for option in question.get("options", [])}
        if answer is not None and answer not in valid_options:
            answer = None
        totals[group] += 1
        if answer is None:
            unanswered += 1
        elif answer == question["correct_option_id"]:
            correct[group] += 1

    present = [dimension for dimension in DIMENSIONS if totals[dimension]]
    if not present:
        raise ValueError("No valid questions")
    scores = {f"{dimension}_accuracy": 100.0 * correct[dimension] / totals[dimension] for dimension in present}
    scores["score"] = sum(scores[f"{dimension}_accuracy"] for dimension in present) / len(present)
    scores["unanswered"] = unanswered
    return scores


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("/app/input"))
    parser.add_argument("--output", type=Path, default=Path("/app/output"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    output = args.output / "scores.json"
    output.unlink(missing_ok=True)
    try:
        result = score(
            load_json(args.input / "ref" / "benchmark.json"),
            load_json(args.input / "res" / "predictions.json"),
        )
        output.write_text(json.dumps(result, allow_nan=False), encoding="utf-8")
        print("Scoring completed successfully.")
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError):
        print("Scoring failed: check OSL JSON structure, IDs, and predictions.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
