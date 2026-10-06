# Streaming Visual Question Answering task specification

Status: draft; technical choices below are not final rules.

Can AI answer questions about a match as it unfolds? This challenge brings together football video understanding and language, asking models to answer questions using information available in an incoming video stream. The focus is on understanding what has been observed so far, without relying on future footage.

## Decisions before launch

- [ ] Inspect and freeze the native streaming question IDs, timestamps and answer types.
- [ ] Choose uploaded answers versus execution of submitted models on a controlled stream.
- [ ] Define allowed context, memory, response deadlines, model/API access and compute.
- [ ] Select scoring for each question type and aggregation; the included option-ID scorer is only a prototype.
- [ ] Define enforcement or finalist audits for the no-future-frames rule.
