# Split layout

The task lead's [Streaming VQA reference repository](https://github.com/jyrao/soccernet-streaming-vqa-challenge) supplies the public test questions and labels, public challenge questions without labels, and baseline prediction files mirrored here.

| Split | Status | Ground truth here? |
| --- | --- | --- |
| train | Not yet identified | No |
| valid | Not yet identified | No |
| test | [test_GT.json](test_GT.json): 4 halves and 700 questions; [test_submission.json](test_submission.json): baseline predictions | Yes, test only |
| challenge | [challenge_public.json](challenge_public.json): 10 halves and 1,158 questions; [challenge_submission.json](challenge_submission.json): baseline predictions | **No** |

The challenge GT exists in the organizer's private source directory. It must stay outside this repository and the participant package. Frozen source commit: `6e71e319e1f0c74bd5d5a096d986b4c3dbb9388c` for the copied public files. See [data guide](../README.md#data).
