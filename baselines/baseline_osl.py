#!/usr/bin/env python3
"""
Text-only baseline for the Soccer Streaming VQA Challenge (OpenSportsLib format).

================================================================================
  THIS IS A BASELINE.
  It does NOT watch the video. It reads ONLY the question text + the answer
  options (plus general football knowledge) and answers directly.
================================================================================

It calls the **official OpenAI API** (https://api.openai.com/v1/chat/completions)
with your official OpenAI API key and asks the model to pick the most plausible
multiple-choice option.

Output: an OpenSportsLib-style submission file, i.e. the INPUT question file with
a `prediction` field added to every question (and the ground-truth-only fields
removed). This is the exact shape of `test_submission_osl.json`:

    {
      "version": "2.0", "date": "...", "task": "streaming_vqa",
      "dataset_name": "Test" | "Challenge", "modalities": ["video"],
      "metadata": {...},
      "data": [
        {
          "id": "match_001_half_1",
          "inputs": [...],
          "metadata": {...},
          "streaming_vqa": [
            {
              "id": "dim4_q1", "position_ms": 712000, "question": "...",
              "options": [...],
              "metadata": {"category": "dim4", "question_type": "multiple-choice"},
              "prediction": "o2"
            }
          ]
        }
      ]
    }

--------------------------------------------------------------------------------
  Everything below is SWAPPABLE. You can replace the model / API key / endpoint
  to use any other OpenAI-compatible service, or any other LLM provider.
--------------------------------------------------------------------------------
  - Model   : --model / OPENAI_MODEL        (default: gpt-4o)
  - API key : --api-key / OPENAI_API_KEY    (default: your official OpenAI key)
  - Endpoint: --api-url / OPENAI_API_URL    (default: official OpenAI endpoint)

Usage:
    # test split      -> test_submission_osl.json
    python3 baseline_osl.py --input test.json --output test_submission_osl.json

    # challenge split -> challenge_submission_osl.json
    python3 baseline_osl.py --input challenge.json --output challenge_submission_osl.json
"""

import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

import requests

# ---------------------------------------------------------------------------
# Defaults (all swappable via flags / environment variables)
# ---------------------------------------------------------------------------
DEFAULT_API_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-4o"          # change to gpt-4o-mini / gpt-4.1 / o1 / ... as you like


SYSTEM_PROMPT = (
    "You are answering multiple-choice questions about football (soccer) "
    "match videos. You do NOT have access to the video, so answer based only "
    "on the text of the question and its options, plus general football "
    "knowledge. Choose the single most reasonable option. "
    "Reply with ONLY the option id (e.g. o1, o2, o3, o4). Do not add any "
    "explanation or other text."
)

# ANSI colours for the live tally (auto-disabled when not a TTY).
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def option_map(q: dict) -> dict:
    """Return {option_id: option_text} for one question."""
    return {o["id"]: o["text"] for o in q.get("options", [])}


def build_question_metadata(q: dict) -> dict:
    """Preserve public metadata and normalize legacy dimension to category."""
    meta = dict(q.get("metadata", {}))
    meta.pop("reason", None)
    if "dimension" in meta:
        legacy = meta.pop("dimension")
        if "category" in meta and meta["category"] != legacy:
            raise ValueError("Conflicting category and dimension metadata")
        meta.setdefault("category", legacy)
    return meta


def build_user_prompt(q: dict) -> str:
    """Question text + options only. Never any ground-truth answer."""
    lines = [
        f"Question: {q['question']}",
        "",
        "Options:",
    ]
    for o in q.get("options", []):
        lines.append(f"{o['id']}: {o['text']}")
    lines.append("")
    lines.append("Answer with the option id only.")
    return "\n".join(lines)


def parse_response(raw: str, q: dict):
    """Extract the chosen option id from the model output.

    Returns (predicted_id, predicted_text, status).
    """
    opt_map = option_map(q)
    if not raw:
        return None, None, "empty"
    raw = raw.strip()

    # 1) explicit option id o1..oN
    m = re.search(r"\b(o\d+)\b", raw)
    if m and m.group(1) in opt_map:
        oid = m.group(1)
        return oid, opt_map[oid], "answered"

    # 2) single letter A/B/C/D -> first/second/... option
    m = re.search(r"\b([A-Da-d])\b", raw)
    if m:
        idx = ord(m.group(1).upper()) - ord("A")
        options = q.get("options", [])
        if 0 <= idx < len(options):
            oid = options[idx]["id"]
            return oid, opt_map[oid], "answered"

    # 3) fuzzy: the raw text contains one of the option texts
    for oid, text in opt_map.items():
        if text.strip() and text.strip().lower() in raw.lower():
            return oid, text, "answered"

    return None, raw[:120], "unparsed"


def call_api(prompt: str, api_url: str, api_key: str, model: str,
             timeout: int = 120, retries: int = 3):
    """Call the official OpenAI chat/completions endpoint (OpenAI-compatible)."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.0,
        "stream": False,
    }
    last_err = None
    for attempt in range(retries):
        try:
            resp = requests.post(api_url, headers=headers, json=payload, timeout=timeout)
            resp.raise_for_status()
            return (resp.json()["choices"][0]["message"].get("content") or "").strip()
        except Exception as e:  # noqa: BLE001 - retry on transient failures
            last_err = e
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"API call failed after {retries} attempts: {last_err}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Answer streaming VQA questions with the official OpenAI API "
                    "(text-only baseline, no video)."
    )
    parser.add_argument("--input", "-i", required=True,
                        help="Path to the input questions JSON (test.json / challenge.json).")
    parser.add_argument("--output", "-o", required=True,
                        help="Path to write the submission JSON (e.g. test_submission_osl.json).")
    parser.add_argument("--model", default=os.environ.get("OPENAI_MODEL", DEFAULT_MODEL),
                        help=f"Model name (default: {DEFAULT_MODEL}).")
    parser.add_argument("--api-url", default=os.environ.get("OPENAI_API_URL", DEFAULT_API_URL),
                        help="OpenAI-compatible chat/completions endpoint.")
    parser.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY", ""),
                        help="OpenAI API key (default: OPENAI_API_KEY env var).")
    parser.add_argument("--workers", type=int, default=1,
                        help="Number of parallel API workers (default: 1 = sequential).")
    parser.add_argument("--resume", action="store_true",
                        help="Skip questions already answered in an existing output file.")
    args = parser.parse_args()

    if not args.api_key:
        sys.exit(
            "ERROR: no OpenAI API key. Set the OPENAI_API_KEY environment variable "
            "or pass --api-key <your-key>."
        )

    in_path = Path(args.input)
    out_path = Path(args.output)
    if not in_path.exists():
        sys.exit(f"ERROR: input file not found: {in_path}")

    data = json.loads(in_path.read_text())

    # ------------------------------------------------------------------
    # Build the output skeleton in input order. This is the OpenSportsLib
    # submission format: the full input, minus ground-truth-only fields,
    # with a `prediction` slot on every question.
    # ------------------------------------------------------------------
    items = []          # ordered list of output data items
    lookup = {}         # (item_id, question_id) -> (item, question)
    tasks = []          # (item_id, question_id) flat list, in order
    for item in data.get("data", []):
        out_item = {
            "id": item["id"],
            "inputs": item.get("inputs", []),
            "metadata": item.get("metadata", {}),
            "streaming_vqa": [],
        }
        items.append(out_item)
        for q in item.get("streaming_vqa", []):
            out_q = {
                "id": q["id"],
                "position_ms": q.get("position_ms"),
                "question": q["question"],
                "options": q.get("options", []),
                "metadata": build_question_metadata(q),
                "prediction": None,
            }
            out_item["streaming_vqa"].append(out_q)
            key = (item["id"], q["id"])
            if key in lookup:
                sys.exit(f"ERROR: duplicate sample/question ID: {key}")
            lookup[key] = (out_q, q)
            tasks.append(key)

    total = len(tasks)
    if total == 0:
        sys.exit("ERROR: no streaming_vqa questions found in the input file.")
    print(f"Loaded {total} questions from {in_path}")
    print(f"Model: {args.model} | Endpoint: {args.api_url}")

    # Ground truth is present in test.json but absent in challenge.json.
    has_labels = all("correct_option_id" in q for _, q in lookup.values())

    # Resume: mark already-answered questions from an existing output file.
    done_set = set()
    if args.resume and out_path.exists():
        try:
            prev = json.loads(out_path.read_text())
            for m in prev.get("data", []):
                for q in m.get("streaming_vqa", []):
                    key = (m["id"], q["id"])
                    if key in lookup:
                        out_q, original = lookup[key]
                        if (q.get("question") != original.get("question")
                                or q.get("options") != original.get("options")):
                            raise ValueError("Resume file questions/options differ from input")
                        if q.get("prediction") in option_map(original):
                            out_q["prediction"] = q["prediction"]
                            done_set.add(key)
            if done_set:
                print(f"Resuming: {len(done_set)} question(s) already answered -> will skip.")
        except (json.JSONDecodeError, KeyError):
            print("Warning: existing output unreadable; starting fresh.")

    todo = [k for k in tasks if k not in done_set]

    lock = Lock()
    stats = {"answered": len(done_set), "correct": 0, "wrong": 0,
             "unparsed": 0, "error": 0}
    if has_labels:
        stats["correct"] = sum(
            lookup[k][0]["prediction"] == lookup[k][1]["correct_option_id"]
            for k in done_set
        )
        stats["wrong"] = len(done_set) - stats["correct"]
    use_color = sys.stdout.isatty()

    def save():
        out = {
            "version": data.get("version"),
            "date": data.get("date"),
            "task": data.get("task"),
            "dataset_name": data.get("dataset_name"),
            "modalities": data.get("modalities"),
            "metadata": data.get("metadata"),
            "data": items,
        }
        out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    save()

    def process(key):
        out_q, q = lookup[key]
        pred_id = None
        status = "error"
        try:
            prompt = build_user_prompt(q)
            raw = call_api(prompt, args.api_url, args.api_key, args.model)
            pred_id, _, status = parse_response(raw, q)
        except Exception:  # noqa: BLE001 - API/network failure -> mark error, allow resume
            pred_id = None
            status = "error"
        out_q["prediction"] = pred_id
        return key, pred_id, status, q

    def on_done(key, pred_id, status, q):
        with lock:
            stats["answered"] += 1
            if status == "unparsed":
                stats["unparsed"] += 1
            elif status == "error":
                stats["error"] += 1
            elif has_labels:
                if pred_id == q.get("correct_option_id"):
                    stats["correct"] += 1
                else:
                    stats["wrong"] += 1

            item_id, qid = key
            q_text = q["question"][:55] + ("..." if len(q["question"]) > 55 else "")
            if has_labels:
                correct = q.get("correct_option_id")
                if status in ("unparsed", "error"):
                    mark = f"{YELLOW}??{RESET}" if use_color else "?? "
                    verdict = f"[{status}]"
                elif pred_id == correct:
                    mark = f"{GREEN}OK{RESET}" if use_color else "OK "
                    verdict = f"-> {pred_id}"
                else:
                    mark = f"{RED}XX{RESET}" if use_color else "XX "
                    verdict = f"-> {pred_id} (correct: {correct})"
                acc = stats["correct"] / stats["answered"] * 100 if stats["answered"] else 0.0
                print(f"[{stats['answered']:>4}/{total}] {mark} "
                      f"micro_acc={acc:5.1f}%  {item_id}/{qid}  \"{q_text}\" {verdict}",
                      flush=True)
            else:
                mark = f"{YELLOW}??{RESET}" if status in ("unparsed", "error") else \
                       (f"{GREEN}OK{RESET}" if use_color else "OK ")
                print(f"[{stats['answered']:>4}/{total}] {mark} "
                      f"{item_id}/{qid}  \"{q_text}\" -> {pred_id or status}",
                      flush=True)
            save()

    if args.workers <= 1:
        for key in todo:
            k, pred_id, status, q = process(key)
            on_done(k, pred_id, status, q)
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futures = {ex.submit(process, key): key for key in todo}
            for fut in as_completed(futures):
                k, pred_id, status, q = fut.result()
                on_done(k, pred_id, status, q)

    # Final summary
    print("\n" + "=" * 60)
    print("DONE")
    print(f"  Total     : {total}")
    print(f"  Answered  : {stats['answered']}")
    if has_labels:
        print(f"  Correct   : {stats['correct']}")
        print(f"  Wrong     : {stats['wrong']}")
        print(f"  Unparsed  : {stats['unparsed']}")
        print(f"  Errors    : {stats['error']}")
        print(f"  Micro accuracy (diagnostic only): {stats['correct']/total*100:.2f}%")
        print("  Official score: run evaluation/scoring.py for the six-subcategory mean.")
    else:
        print(f"  Unparsed  : {stats['unparsed']}")
        print(f"  Errors    : {stats['error']}")
    print(f"  Saved to  : {out_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
