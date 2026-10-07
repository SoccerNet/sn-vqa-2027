# Streaming VQA evaluation

[eval_predictions.py](eval_predictions.py) adapts the [task lead's reference evaluator](https://github.com/jyrao/soccernet-streaming-vqa-challenge/tree/94f45fd/codes). [scoring.py](scoring.py) uses the same ID matching, option handling, and aggregation for the scoring-package layout.

## Local scoring

Python 3.9+ is sufficient; no third-party packages are required. From the repository root:

```bash
python3 evaluation/eval_predictions.py data/test_submission.json data/test_GT.json
```

The test answers and baseline predictions are in [data](../data/README.md). Challenge questions and baseline predictions are also there, while challenge answers are withheld.

## Prediction format and score

Predictions use the OSL `data[].streaming_vqa[]` JSON structure. Each answer is matched by `(sample ID, question ID)` because question IDs can repeat across halves. Put an option ID such as `"o2"` in `prediction`, or JSON `null` if unanswered. A missing, duplicate, or extra question ID fails validation; an invalid or empty option counts as incorrect.

The ranking score is the unweighted mean of the six subcategory accuracies, reported as a percentage. This is the default in both scripts and is equivalent to `--average-by subcategory`. The six groups are counting, recall event time, recall event player, event team, event player, and causal reasoning. Each unanswered or invalid option counts as incorrect. The test baseline scores **41.76%** with this metric.

For an analytical view that weights the four D1–D4 categories equally, run:

```bash
python3 evaluation/eval_predictions.py data/test_submission.json data/test_GT.json --average-by category
```

This gives **41.80%** on the test baseline. It does not set the ranking score. The CodaBench adapter defaults to subcategory mode and accepts the same `--average-by category` option for local evaluation.

## Scoring-package layout

The adapter reads `/app/input/ref/benchmark.json` and `/app/input/res/predictions.json`, then writes `/app/output/scores.json`. Use `data/test_GT.json` as a local test reference. The answer-file scorer measures prediction accuracy; compliance with the [streaming and input rules](../RULES.md) is established through method documentation and review.
