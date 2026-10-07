"""CodaBench adapter for the source Streaming VQA evaluator's OSL JSON schema."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from eval_predictions import calculate_scores, load_json


def score(reference, submission, average_by="subcategory"):
    result = calculate_scores(reference, submission, average_by)
    scores = {
        f"{group.replace(' ', '_')}_accuracy": 100.0 * result["correct"][group] / result["totals"][group]
        for group in result["groups"]
        if result["totals"][group]
    }
    scores["score"] = 100.0 * result["average"]
    scores["unanswered"] = result["unanswered"]
    return scores


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("/app/input"))
    parser.add_argument("--output", type=Path, default=Path("/app/output"))
    parser.add_argument("--average-by", choices=("subcategory", "category"), default="subcategory")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    output = args.output / "scores.json"
    output.unlink(missing_ok=True)
    try:
        result = score(
            load_json(args.input / "ref" / "benchmark.json"),
            load_json(args.input / "res" / "predictions.json"),
            args.average_by,
        )
        output.write_text(json.dumps(result, allow_nan=False), encoding="utf-8")
        print("Scoring completed successfully.")
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError):
        print("Scoring failed: check OSL JSON structure, IDs, and predictions.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
