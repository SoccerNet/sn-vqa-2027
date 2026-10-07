# Data

[SoccerNet/SN-VQA-2027](https://huggingface.co/datasets/SoccerNet/SN-VQA-2027) uses OpenSportsLib OSL JSON. The files mirrored in this repository are:

The task provides **test and challenge sets only**; there is no separate training or validation set.

| File | Contents |
| --- | --- |
| [test_GT.json](test_GT.json) | Questions and answers from 4 match halves (700 questions; six subcategories) |
| [test_submission.json](test_submission.json) | Baseline predictions for the same 700 test questions |
| [challenge_public.json](challenge_public.json) | Questions without answers from 10 match halves (1,158 questions) |
| [challenge_submission.json](challenge_submission.json) | Baseline predictions for the challenge questions |

The challenge answers are withheld for evaluation. All files use the OpenSportsLib OSL JSON format described in the repository's [evaluation guide](../evaluation/README.md).
