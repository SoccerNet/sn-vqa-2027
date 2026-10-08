# Streaming Visual Question Answering Challenge Rules

📅 **Submission deadline:** April 25, 2027, 23:59 Anywhere on Earth (AoE; UTC−12).

## Permitted inputs and temporal cutoff

At a question timestamp `t`, a method may use only the match video observed up to and including `t`, the current question and answer options, the question timestamp, and permitted match metadata. Permitted metadata is limited to team names, kit colors, rosters and jersey numbers, initial lineups and positions, and playing directions once they have been established from the broadcast.

The same cutoff applies to model inputs, memory, cached features, retrieved frames, tool calls, and state or model updates. Do not use future frames, future match information, post-match reports, reference annotations, or ground-truth answers to produce predictions.

## Visual-only methods

Challenge video is provided with broadcast audio muted. Do not use broadcast audio, speech recognition, commentary transcripts, subtitles derived from audio, or any other audio source. Text-only methods that use the question and options without viewing video are eligible on the same leaderboard.

## Models, APIs, and external information

Local models and remote LLM, VLM, or agent APIs are allowed. Disable web browsing, web search, search grounding, and external information retrieval in every model and tool. Do not query live-score services, match databases, social media, news, post-match reports, or other external sources for match facts. Predictions must use only the permitted inputs listed above.

## Submission and technical report

Submit one OpenSportsLib (OSL) JSON prediction for every challenge question. Match questions by `(sample ID, question ID)` because question IDs may repeat across match halves. Each prediction must be an option ID from that question, or JSON `null` if unanswered. Missing, duplicate, or unknown question IDs fail validation. An unanswered, empty, or invalid option is scored as incorrect.

Each team must provide a technical report with its entry. Document the models or APIs used, data sources, prompts and settings, and how the method enforces the audio, temporal-cutoff, permitted-metadata, and no-web-retrieval rules. Include enough implementation detail to reproduce the method and review its compliance. The scoring script checks prediction format and accuracy; rule compliance is assessed from the report and method review.

## Ranking

The official challenge ranking uses multiple-choice accuracy averaged equally over the six subcategories present in the challenge split. This is the default `subcategory` evaluation. The four-category average is available for analysis with `--average-by category` and does not replace the leaderboard score. See the [evaluation guide](evaluation/README.md) for the metric definition and commands.

The public test set is for development and local scoring. The hidden challenge answers determine the official ranking and must not be used as model inputs.
