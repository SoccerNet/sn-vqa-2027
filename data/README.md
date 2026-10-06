# Data

[SoccerNet/SN-VQA-2027](https://huggingface.co/datasets/SoccerNet/SN-VQA-2027) uses OpenSportsLib OSL JSON. The files mirrored in this repository are:

The task provides **test and challenge sets only**; there is no separate training or validation set.

| File | Contents |
| --- | --- |
| [test_GT.json](test_GT.json) | Questions and answers from 4 match halves (700 questions) |
| [test_submission.json](test_submission.json) | Baseline predictions for the test set |
| [challenge_public.json](challenge_public.json) | Questions without answers from 10 match halves (1,158 questions) |
| [challenge_submission.json](challenge_submission.json) | Baseline predictions for the challenge questions |

The challenge answers are withheld for evaluation. The mirrored files come from the [task lead's reference repository](https://github.com/jyrao/soccernet-streaming-vqa-challenge) at commit `6e71e319e1f0c74bd5d5a096d986b4c3dbb9388c`.
