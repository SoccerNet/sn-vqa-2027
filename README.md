# SoccerNet Challenge 2027 — Streaming Visual Question Answering

📢 **Streaming Visual Question Answering Challenge!** 🚀

Can AI answer questions about a match as it unfolds? This challenge brings together football video understanding and language, asking models to answer questions using information available in an incoming video stream. The focus is on understanding what has been observed so far, without relying on future footage.

⏳ **Status:** In preparation — submissions are not open.  
📅 **Submission deadline:** April 25, 2027; cutoff time and timezone to be announced.  
👥 **Task lead(s):** KAUST, Jiayuan Rao and Ahmad Sait  
🤝 **Sponsor:** To be announced

🏠 [Challenge website](https://www.soccer-net.org/challenges/2027) / 🗂️ [Data](https://huggingface.co/datasets/SoccerNet/SN-VQA-2027) / 💻 [Baseline predictions](baselines/README.md) / 📚 [Rules](docs/rules.md) / 📊 [Evaluation](evaluation/README.md)

## Task

[Task specification and open decisions](docs/task.md) describes the current scope. This repository will hold the versioned evaluation code and submission instructions for the 2027 challenge. Baselines may live here or in an external repository linked below.

## Data

Access the dataset on [Hugging Face](https://huggingface.co/datasets/SoccerNet/SN-VQA-2027). Follow its access conditions and download instructions.

This repository includes [public test questions and labels](data/test/test_GT.json), [public challenge questions without labels](data/challenge/challenge_public.json), and baseline predictions for both splits. See [the data guide](docs/data.md) for the complete inventory. **Challenge ground truth remains private.**

## Baseline

The task lead's [GPT-5.5 test predictions](data/test/test_submission.json) and [challenge predictions](data/challenge/challenge_submission.json) are included. The [source repository](https://github.com/jyrao/soccernet-streaming-vqa-challenge) also has a text-only API baseline and links to a streaming video baseline. These are reference starting points, not final published 2027 rankings.

See [baseline instructions](baselines/README.md). Existing research baselines must be checked against the final challenge format before their scores are advertised as 2027 reference results.

## Evaluation

The scorer now follows the task lead's OSL JSON format and D1–D4 dimension-average metric. It is locally tested on the public test set; the CodaBench challenge server and final rules remain to be launched.

See [evaluation instructions](evaluation/README.md) for the OSL JSON format, local command, scoring rule, and CodaBench package contract. CodaBench test and challenge links will be added after the servers have been validated.

## Release readiness

| Item | Current state |
| --- | --- |
| Task definition | Streaming OSL multiple-choice task and draft rules documented |
| Data and splits | Public test GT and challenge questions present; challenge GT private; train/valid TBD |
| Baseline | Test and challenge baseline predictions present |
| Evaluation | Source evaluator adapted and tested on public test |
| Benchmark | CodaBench server pending |
| Sponsor | Not confirmed |

Each task launches independently after its rules, data, baseline, evaluator and benchmark are verified. See the [task specification](docs/task.md) for remaining technical decisions.

## Getting started

1. Read the [task specification](docs/task.md) and [draft rules](docs/rules.md).
2. Follow the [data access guide](docs/data.md).
3. Consult the [baseline instructions](baselines/README.md).
4. Check the [evaluation status](evaluation/README.md) before generating submissions.

## Updates and support

Each task launches independently once ready. Follow the [challenge website](https://www.soccer-net.org/challenges/2027) and [SoccerNet Discord](https://discord.gg/cPbqf2mAwF). Use repository issues for reproducible code problems; do not post access tokens, restricted data or private labels.

## Citation and licensing

The Streaming VQA paper is forthcoming. [CITATION.bib](CITATION.bib) will be updated with its verified conference citation after publication. The 2027 challenge citation and repository code license will be confirmed before release.
