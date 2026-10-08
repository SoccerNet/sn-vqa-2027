# Streaming VQA evaluation

The single [scoring script](scoring.py) evaluates OSL prediction and ground-truth JSON files locally and is also the [CodaBench evaluation program](https://www.codabench.org/competitions/18329/). The server scores the 2027 challenge split; public test files are for local verification.

## Local scoring

Python 3.9+ is sufficient; no third-party packages are required. From the repository root:

```bash
python3 evaluation/scoring.py data/test_submission.json data/test_GT.json
```

The test answers and baseline predictions are in [data](../data/README.md). Challenge questions and baseline predictions are also there, while challenge answers are withheld.

## Prediction format and score

Predictions use the OSL `data[].streaming_vqa[]` JSON structure. Each answer is matched by `(sample ID, question ID)` because question IDs can repeat across halves. Put an option ID such as `"o2"` in `prediction`, or JSON `null` if unanswered. A missing, duplicate, or extra question ID fails validation; an invalid or empty option counts as incorrect.

The ranking score is the unweighted mean of the six subcategory accuracies, reported as a percentage. This is the default for both local and CodaBench execution and is equivalent to `--average-by subcategory`. The six groups are counting, recall event time, recall event player, event team, event player, and causal reasoning. Each unanswered or invalid option counts as incorrect. The test baseline scores **41.76%** with this metric.

For each subcategory, pool all its questions across match halves before calculating accuracy. Then compute:

```text
accuracy[k] = correct answers in subcategory k / all questions in subcategory k
score = 100 × (accuracy[1] + ... + accuracy[6]) / 6
```

All six subcategories must be present in the reference; otherwise scoring fails instead of silently averaging fewer groups. Use full test or challenge references. This differs from overall accuracy (274/700 = 39.14% for the included test predictions) and from averaging match-level scores. Calculations use full precision; the local report rounds percentages to two decimal places.

Taxonomy comes exclusively from the reference question's metadata. `category` identifies `dim1`–`dim4`; `subcategory` is one of `counting`, `recall_event_time`, `recall_event_player`, `event_team`, `event_player`, or `causal reasoning`. Preserve these fields in generated submissions, using `category` rather than the legacy `dimension` name. Submission metadata never determines the scoring group, and missing or invalid reference taxonomy causes an error.

For an analytical view that weights the four D1–D4 categories equally, run:

```bash
python3 evaluation/scoring.py data/test_submission.json data/test_GT.json --average-by category
```

This gives **41.80%** on the test baseline. It is an optional local analysis score. Keep the CodaBench scoring command at its default subcategory setting for the official leaderboard.

## Scoring-package layout

In CodaBench, the script reads `/app/input/ref/benchmark.json` and `/app/input/res/predictions.json`, then writes `/app/output/scores.json`. Use `data/test_GT.json` as a local test reference. The answer-file scorer measures prediction accuracy; compliance with the [streaming and input rules](../RULES.md) is established through method documentation and review.
