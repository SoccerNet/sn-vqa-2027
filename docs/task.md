# Streaming Visual Question Answering task specification

At each question timestamp, a system selects one of the provided options using only the broadcast frames observed up to that time, the current question and options, and permitted pre-match metadata. This task tests memory and reasoning over a long match stream. The 2027 paper is forthcoming.

## Current question format

The available OSL records identify questions by `(half ID, question ID)` and give `position_ms`, question text, and option IDs. The test set covers four dimensions, D1–D4; the challenge set may use different metadata field names, which the [evaluator](../evaluation/README.md) handles. The public challenge file has no correct options.

## Decisions before launch

- [ ] Confirm that the public challenge question set and private ground truth are frozen, disjoint from public test, and versioned.
- [ ] Decide whether participants submit answers only or run models on a controlled stream; answer files alone do not prove causal operation.
- [ ] Finalize permitted pre-match metadata, API use, time limits, team rules and technical-report requirements.
- [ ] Confirm the dimension-average score, tie handling, and submission limits in CodaBench.
- [ ] Add the paper's verified conference citation when available.
