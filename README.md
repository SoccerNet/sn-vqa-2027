# SoccerNet Challenge 2027 — Streaming Visual Question Answering (VQA)

📢 **Streaming Visual Question Answering (VQA) Challenge!** 🚀

⏳ **Status:** In preparation — submissions are not open.\
📅 **Submission deadline:** April 25, 2027, 23:59 Anywhere on Earth (AoE; UTC−12).\
👥 **Task leads:** Jiayuan Rao and Ahmad Sait\
🤝 **Sponsor:** To be announced

🏠 [Challenge website](https://www.soccer-net.org/challenges/2027) · 🗂️ [Data on Hugging Face](https://huggingface.co/datasets/SoccerNet/SN-VQA-2027) · 💻 [Baseline](baselines/README.md) · 📚 [Rules](RULES.md) · 📊 [Evaluation](evaluation/README.md) · 🏆 [Evaluation server](https://www.codabench.org/) (task URL TBD)

## Task

Answer multiple-choice questions while a soccer match unfolds. At question time `t`, a system may use only video observed up to `t`, the question and options, and permitted pre-match metadata. The task tests immediate visual understanding and memory over long streams without access to future frames.

## Data

The [SN-VQA-2027 dataset](https://huggingface.co/datasets/SoccerNet/SN-VQA-2027) uses OpenSportsLib OSL JSON. This repository includes [public test questions and labels](data/test_GT.json) for 4 halves/700 questions, [public challenge questions without labels](data/challenge_public.json) for 10 halves/1,158 questions, and the baseline predictions for both. The **challenge ground truth is private** and not committed. Train and validation sets have not yet been identified; see the [split inventory](data/README.md).

## Baseline

The [baseline folder](baselines/README.md) points to the included GPT-5.5 prediction files, the task lead's [text-only API baseline](https://github.com/jyrao/soccernet-streaming-vqa-challenge), and [MatchLive](https://github.com/Becomebright/MatchLive). It explains how to download the dataset and run or evaluate each available baseline. The 2027 reference paper is forthcoming.

## Evaluation

The [evaluation folder](evaluation/README.md) contains the task lead's OSL multiple-choice evaluator and a CodaBench adapter. The default score is the unweighted mean of D1–D4 accuracies. This task-specific evaluator remains authoritative: OpenSportsLib's generic VQA metrics score free-text answers and do not implement this streaming option-ID/dimension protocol. The server URL is TBD.

## Citation

The 2027 Streaming VQA reference paper is forthcoming. Its verified conference BibTeX will be added here after publication.

## Updates and support

Each task launches independently when ready. Follow the [challenge website](https://www.soccer-net.org/challenges/2027) and [SoccerNet Discord](https://discord.gg/cPbqf2mAwF) for announcements. Use repository issues for reproducible code problems; do not post access tokens or restricted data.

## Release readiness

| Item | Current state |
| --- | --- |
| Task definition | Streaming multiple-choice protocol and draft rules documented |
| Data | Public test GT and challenge questions present; challenge GT private; train/valid TBD |
| Baseline | Test and challenge predictions present |
| Evaluation | Task-lead evaluator and adapter tested against public test and private challenge reference |
| Benchmark | CodaBench server TBD |
| Sponsor | TBD |

This section is for preparation and will be removed when this task is ready for release.
