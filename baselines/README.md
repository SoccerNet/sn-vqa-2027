# Streaming VQA baseline

The repository includes [test predictions](../data/test_submission.json) and [challenge predictions](../data/challenge_submission.json) from the text-only reference baseline. The [test answers](../data/test_GT.json) are public, so the test score can be reproduced from this repository root:

```bash
python evaluation/scoring.py data/test_submission.json data/test_GT.json
```

This reports **41.76%**, the equally weighted mean of the six test-subcategory accuracies. Use `--average-by category` for the four-category analysis score (**41.80%**).

The text-only reference baseline uses question text and options without inspecting video; **text-only methods are leaderboard-eligible**. The included JSON files are OSL predictions that can be scored directly. [MatchLive](https://github.com/Becomebright/MatchLive) is a separate streaming-video approach. See the [challenge rules](../RULES.md) for permitted inputs and the [evaluation guide](../evaluation/README.md) for scoring.
