# Streaming Visual Question Answering challenge rules

📅 **Submission deadline:** April 25, 2027, 23:59 Anywhere on Earth (AoE; UTC−12).

- **Visual-only:** use muted video; do not use broadcast audio, speech recognition, commentary transcripts, or another audio source.
- **Streaming-only:** a question at time `t` may use frames and memory available by `t`, never future footage or post-match information.
- **Model APIs:** local or remote models are allowed, but disable browsing, web search, search grounding, and retrieval of external match facts. Do not query score services, match databases, social media, or reports.
- **Inputs:** use only the video history, current question and options, timestamp, and permitted pre-match metadata.
- **Technical report:** document models or APIs, data sources, prompts and settings, and how audio, future frames, and web retrieval were excluded.
- **Submission:** provide one OSL JSON prediction for every question. Missing or extra IDs fail validation. An unanswered or invalid option counts as incorrect.

The [evaluation guide](evaluation/README.md) describes the D1–D4 dimension-average metric. The test set supports development; the withheld challenge answers determine the final ranking.
