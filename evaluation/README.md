# Evaluation — OSL Streaming VQA

The local evaluator [eval_predictions.py](eval_predictions.py) is copied from the [task lead's reference repository](https://github.com/jyrao/soccernet-streaming-vqa-challenge/tree/6e71e319e1f0c74bd5d5a096d986b4c3dbb9388c/codes), commit `6e71e319e1f0c74bd5d5a096d986b4c3dbb9388c`. [scoring.py](scoring.py) adapts the same ID matching, option handling, and dimension aggregation for CodaBench. Recheck both against the final reference before launch.

## Run locally

Python 3.9+; no third-party packages. From the repository root:

```bash
python3 evaluation/eval_predictions.py data/test/test_submission.json data/test/test_GT.json
python3 -m unittest discover -s tests -v
```

The public test ground truth and baseline predictions are in [data/test](../data/test). The challenge questions and baseline predictions are in [data/challenge](../data/challenge); **challenge ground truth is not in this repository**. Only organizers can score that split locally.

## Contract and metric

Predictions use the OSL `data[].streaming_vqa[]` JSON structure. Match each answer by `(sample ID, question ID)`, since question IDs repeat across halves. Put an option ID (for example `"o2"`) in `prediction`, or JSON `null` if unanswered. A missing, duplicate, or extra question ID is rejected. An empty or invalid option counts as incorrect. The primary candidate score is the unweighted mean of the four dimension accuracies, D1–D4, reported as a percentage; per-dimension scores and unanswered count are also recorded. The reference evaluator optionally reports an unweighted subcategory average with `--average-by subcategory`; that is not the default ranking score.

## CodaBench package

The scorer reads `/app/input/ref/benchmark.json` from the organizer-only reference package and `/app/input/res/predictions.json` from the submission ZIP, then writes `/app/output/scores.json`. Use `data/test/test_GT.json` for test phase validation. Keep the challenge reference outside Git, in a private organizer package. The task is not live on CodaBench yet. This answer-file scorer cannot enforce visual-only, temporal, or no-web-search rules; those require submission rules and finalist verification.
