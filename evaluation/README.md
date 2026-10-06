# Evaluation — prototype

**Not an official challenge release.** Real manifest adapters, held-out reference data and the final scoring protocol are pending.

## Metrics

Exact option-ID accuracy, reported as a percentage. This is a plumbing prototype, not the official 2027 metric. It applies only to multiple-choice answers. It does not implement free-text evaluation, measure latency or enforce no access to future frames.

## Local example

Python 3.9 or newer; no third-party dependencies. From the repository root:

```bash
python3 evaluation/scoring.py --input examples --output outputs/example
python3 -m unittest discover -s tests -v
```

The included data is synthetic. The sample predictions are perfect and should yield 100 for every reported metric. Generated aggregate scores are written to `outputs/example/scores.json`.

## Proposed submission format

A ZIP with `predictions.json` at its root. The JSON is a list of records, each with exactly `id` and `answer`. IDs and values are nonempty strings; every expected ID must appear exactly once. Missing IDs, extra IDs, duplicate keys and unknown values are rejected. Order is irrelevant.

See [the synthetic submission](../examples/res/predictions.json) and [synthetic reference](../examples/ref/reference.json). The reference schema contains `task`, `records` and `options` for every question. It is an internal prototype format, not an assertion about the native dataset format.

## CodaBench integration

The scoring directory contains `metadata.yaml` and `scoring.py`. At runtime it reads `/app/input/ref/reference.json` and `/app/input/res/predictions.json`, then writes `/app/output/scores.json`. Store real private references only in the organizer reference-data package, never in this repository or a public starting kit.

Test and challenge servers: **coming soon**. Test against the real baseline and malformed submissions on CodaBench before launch. This repository alone does not create a competition or enforce input-modality restrictions.

## Protocol decisions

See [the task specification](../docs/task.md) and [draft rules](../docs/rules.md).
