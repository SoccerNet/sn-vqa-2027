# Streaming VQA evaluation

[eval_predictions.py](eval_predictions.py) comes from the [task lead's reference evaluator](https://github.com/jyrao/soccernet-streaming-vqa-challenge/tree/6e71e319e1f0c74bd5d5a096d986b4c3dbb9388c/codes). [scoring.py](scoring.py) applies the same ID matching, option handling, and dimension aggregation to the scoring-package layout.

## Local scoring

Python 3.9+ is sufficient; no third-party packages are required. From the repository root:

```bash
python3 evaluation/eval_predictions.py data/test_submission.json data/test_GT.json
```

The test answers and baseline predictions are in [data](../data/README.md). Challenge questions and baseline predictions are also there, while challenge answers are withheld.

## Prediction format and score

Predictions use the OSL `data[].streaming_vqa[]` JSON structure. Each answer is matched by `(sample ID, question ID)` because question IDs can repeat across halves. Put an option ID such as `"o2"` in `prediction`, or JSON `null` if unanswered. A missing, duplicate, or extra question ID fails validation; an invalid or empty option counts as incorrect.

The ranking score is the unweighted mean of the D1–D4 dimension accuracies, reported as a percentage. The evaluator also reports per-dimension scores and unanswered count. Its optional `--average-by subcategory` report does not change the ranking score.

## Scoring-package layout

The adapter reads `/app/input/ref/benchmark.json` and `/app/input/res/predictions.json`, then writes `/app/output/scores.json`. Use `data/test_GT.json` as a local test reference. The answer-file scorer measures prediction accuracy; compliance with the [streaming and input rules](../RULES.md) is established through method documentation and review.
