# Streaming VQA rules — draft

📅 **Deadline:** April 25, 2027; cutoff time and timezone to be announced. Final rules take effect only when the task launches.

- **Visual-only:** use muted video; no broadcast audio, speech recognition, commentary transcript, or alternate audio source.
- **Streaming-only:** a question at time `t` may use frames and memory available by `t`, never future footage or post-match information.
- **Model APIs:** local or remote models are allowed, but disable browsing, web search, search grounding, and retrieval of external match facts. Do not query score services, match databases, social media, or reports.
- **Inputs:** use only the video history, current question/options, timestamp, and the permitted pre-match metadata defined in the final release.
- **Technical report:** each submission must document models/APIs, data sources, prompts/settings, and how audio, future frames, and web retrieval were excluded. Final report form and verification procedure are pending.
- **Submission:** provide one OSL JSON prediction for every question. Missing or extra IDs fail validation. An unanswered or invalid option counts as incorrect.

The [evaluation guide](../evaluation/README.md) describes the current metric. Team eligibility, limits, tie policy, external training data, verification, and appeals still need organizer approval. The public test set is for development; the hidden challenge set determines the final ranking.
