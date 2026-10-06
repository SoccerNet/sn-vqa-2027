# SoccerNet Challenge 2027 — Streaming Visual Question Answering

📢 **Streaming Visual Question Answering Challenge!** 🚀

Can AI answer questions about a match as it unfolds? This challenge brings together football video understanding and language, asking models to answer questions using information available in an incoming video stream. The focus is on understanding what has been observed so far, without relying on future footage.

⏳ **Status:** In preparation — submissions are not open.  
📅 **Submission deadline:** April 25, 2027; cutoff time and timezone to be announced.  
👥 **Task lead(s):** KAUST, Jiayuan Rao and Ahmad Sait  
🤝 **Sponsor:** To be announced

🏠 [Challenge website](https://www.soccer-net.org/challenges/2027) / 🗂️ [Data](https://huggingface.co/datasets/SoccerNet/SN-VQA-2027) / 💻 **Baseline:** Coming soon / 📚 [Rules](docs/rules.md) / 📊 [Evaluation](evaluation/README.md)

## Task

[Task specification and open decisions](docs/task.md) describes the current scope. This repository will hold the versioned evaluation code and submission instructions for the 2027 challenge. Baselines may live here or in an external repository linked below.

## Data

Access the dataset on [Hugging Face](https://huggingface.co/datasets/SoccerNet/SN-VQA-2027). Follow its access conditions and download instructions.

See [the data guide](docs/data.md) for release status and split details. Dataset availability does not mean that the challenge is open. Private evaluation labels are not included in this repository.

## Baseline

The 2027 streaming baseline has not been announced. The previous SoccerAgent repository (https://github.com/jyrao/SoccerAgent) is background only and is not presented as a compatible streaming baseline.

See [baseline instructions](baselines/README.md). Existing research baselines must be checked against the final challenge format before their scores are advertised as 2027 reference results.

## Evaluation

A locally tested prototype scorer is included; the official 2027 evaluation protocol is not frozen.

See [evaluation instructions](evaluation/README.md) for current code, submission formats and remaining decisions. CodaBench test and challenge links will be added after the servers have been validated.

## Getting started

1. Read the [task specification](docs/task.md) and [draft rules](docs/rules.md).
2. Follow the [data access guide](docs/data.md).
3. Consult the [baseline instructions](baselines/README.md).
4. Check the [evaluation status](evaluation/README.md) before generating submissions.

## Updates and support

Each task launches independently once ready. Follow the [challenge website](https://www.soccer-net.org/challenges/2027) and [SoccerNet Discord](https://discord.gg/cPbqf2mAwF). Use repository issues for reproducible code problems; do not post access tokens, restricted data or private labels.

## Citation and licensing

The 2027 citation and repository code license will be confirmed before release. Dataset access terms and external baseline licenses apply independently; linking them does not relicense their contents.
