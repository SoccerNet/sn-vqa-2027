# SoccerNet Challenge 2027 — Streaming Visual Question Answering (VQA)

📢 **Streaming Visual Question Answering (VQA) Challenge!** 🚀

📅 **Submission deadline:** April 25, 2027, 23:59 Anywhere on Earth (AoE; UTC−12).\
👥 **Task leads:** Jiayuan Rao and Ahmad Sait

🏠 [Challenge website](https://www.soccer-net.org/challenges/2027) · 🗂️ [Data on Hugging Face](https://huggingface.co/datasets/SoccerNet/SN-VQA-2027) · 💻 [Baseline](baselines/README.md) · 📚 [Rules](RULES.md) · 📊 [Evaluation](evaluation/README.md)

## Task

Answer multiple-choice questions as a soccer match unfolds. At question time `t`, use only the video observed up to `t`, the question and options, and permitted pre-match metadata. The task measures immediate visual understanding and memory over long streams without future frames.

## Data

The [SN-VQA-2027 dataset](https://huggingface.co/datasets/SoccerNet/SN-VQA-2027) uses OpenSportsLib OSL JSON. This repository includes [test questions and labels](data/test_GT.json) for 4 halves and 700 questions, [challenge questions without labels](data/challenge_public.json) for 10 halves and 1,158 questions, and [baseline predictions](data/README.md) for both. Challenge answers are withheld for evaluation.

## Baseline

The [baseline guide](baselines/README.md) links the included prediction files, the task lead's text-only API reference, and MatchLive. It explains how to score the included test predictions and generate submissions in the OSL JSON format.

## Evaluation

The [evaluation guide](evaluation/README.md) contains the task lead's multiple-choice evaluator and a CodaBench scoring adapter. The ranking score is the unweighted mean of the four dimension accuracies, D1–D4.

## Community

Follow the [SoccerNet challenge website](https://www.soccer-net.org/challenges/2027) and [Discord](https://discord.gg/cPbqf2mAwF) for challenge announcements and discussion.
