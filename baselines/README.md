# Streaming VQA baseline

## Text-only API baseline

[baseline_osl.py](baseline_osl.py) sends only each question and its answer options to a configurable, OpenAI-compatible Chat Completions endpoint. It does not inspect video or send ground-truth answers, timestamps, or match metadata to the model. This is a starting point for measuring what question text alone can answer.

Run these commands from the repository root with Python 3.9+:

```bash
python3 -m pip install -r baselines/requirements.txt
export OPENAI_API_KEY="your_api_key"
python3 baselines/baseline_osl.py \
  --input data/test_GT.json \
  --output outputs/test_predictions.json \
  --model YOUR_MODEL_ID
python3 baselines/baseline_osl.py \
  --input data/challenge_public.json \
  --output outputs/challenge_predictions.json \
  --model YOUR_MODEL_ID
```

Generation makes paid API requests according to your provider's pricing. Select an available model with `--model` or `OPENAI_MODEL`; the inherited script default is `gpt-4o`. Use `--api-url` or `OPENAI_API_URL` for an alternative compatible endpoint. The default endpoint is `https://api.openai.com/v1/chat/completions`. Keep browsing, web search, search grounding, and external retrieval disabled, including any provider-side defaults. The script sends no tool definitions.

`--workers N` controls parallel requests (default: 1). `--resume` reuses valid saved predictions and retries unanswered questions. Use the same input, model, and settings when resuming. Predictions are saved as questions complete; failed or unparseable responses produce JSON `null`.

### Output fields

Each output question retains its ID, timestamp, question, options, and public metadata. The script uses `metadata.category` for `dim1`–`dim4`, preserves `metadata.subcategory`, and converts the legacy `dimension` key to `category`. Conflicting values are rejected. It omits `correct_option_id` and the metadata `reason` annotation and adds an option ID or `null` as `prediction`.

Questions are matched by `(sample ID, question ID)`. Ground-truth answers in the public test file are used only for local progress diagnostics; they are excluded from model prompts and submissions. The progress display's micro accuracy is not the leaderboard metric. Score a generated file with:

```bash
python3 evaluation/scoring.py outputs/test_predictions.json data/test_GT.json
```

## Included reference predictions

The repository includes [test predictions](../data/test_submission.json) and [challenge predictions](../data/challenge_submission.json) from the text-only reference baseline. The [test answers](../data/test_GT.json) are public, so the test score can be reproduced from this repository root:

```bash
python evaluation/scoring.py data/test_submission.json data/test_GT.json
```

This reports **41.76%**, the equally weighted mean of the six test-subcategory accuracies. Use `--average-by category` for the four-category analysis score (**41.80%**).

The text-only reference baseline uses question text and options without inspecting video; **text-only methods are leaderboard-eligible**. The included JSON files can be scored directly. Their reported score describes these saved predictions; running the script with a different model, provider, or configuration is not expected to reproduce identical predictions. Existing reference submissions use the legacy `dimension` metadata key; new script outputs use `category`. Scoring reads taxonomy from the reference file, so this naming difference in submissions does not change the score.

## MatchLive: streaming-video baseline

[MatchLive](https://github.com/Becomebright/MatchLive) is the separate video-based starting point. It combines streaming visual perception with revisable match memory, updating events and player identities as new observations arrive. This supports questions about current actions and earlier events in the same match.

The linked repository contains the corresponding baseline implementation and setup instructions. Follow it for the video pipeline, model requirements, and run configuration. When adapting it to this challenge, restrict observations and memory updates to the current question time, use no broadcast audio or external match-information retrieval, and export predictions in the same OSL submission format.

See the [challenge rules](../RULES.md) for permitted inputs and the [evaluation guide](../evaluation/README.md) for scoring.
