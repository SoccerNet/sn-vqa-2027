# Streaming VQA baseline

The repository includes [test predictions](../data/test_submission.json) and [challenge predictions](../data/challenge_submission.json) from the [task lead's reference repository](https://github.com/jyrao/soccernet-streaming-vqa-challenge). The [test answers](../data/test_GT.json) are public, so the test score can be reproduced from this repository root:

```bash
python evaluation/eval_predictions.py data/test_submission.json data/test_GT.json
```

This reports **41.76%**, the equally weighted mean of the six test-subcategory accuracies. Use `--average-by category` for the four-category analysis score (**41.80%**).

The reference repository also provides a [text-only API baseline script](https://github.com/jyrao/soccernet-streaming-vqa-challenge/blob/6e71e319e1f0c74bd5d5a096d986b4c3dbb9388c/baseline/baseline_osl.py). It generates OSL-format predictions from question text and options without inspecting video; **text-only methods are leaderboard-eligible**. From that repository root, configure its API key and run `python baseline/baseline_osl.py --input /path/to/challenge_public.json --output /path/to/predictions.json`. [MatchLive](https://github.com/Becomebright/MatchLive) is a separate streaming-video approach. See the [challenge rules](../RULES.md) for permitted inputs and the [evaluation guide](../evaluation/README.md) for scoring.
