# Data

The 2027 dataset source is [SoccerNet/SN-VQA-2027](https://huggingface.co/datasets/SoccerNet/SN-VQA-2027). Questions and predictions follow [OpenSportsLib OSL JSON](https://opensportslab.github.io/opensportslib/data/osl-json-format/): top-level `data` contains match halves, each with `id`, `inputs`, and `streaming_vqa` questions. Each question has an `id`, `position_ms`, text, options, and metadata.

## Available files

| Split | File | Contents |
| --- | --- | --- |
| Test | [test_GT.json](../data/test/test_GT.json) | Public test questions and correct options: 4 halves, 700 questions |
| Test | [test_submission.json](../data/test/test_submission.json) | Baseline predictions in submission shape |
| Challenge | [challenge_public.json](../data/challenge/challenge_public.json) | Public challenge questions without correct options: 10 halves, 1,158 questions |
| Challenge | [challenge_submission.json](../data/challenge/challenge_submission.json) | Baseline predictions in submission shape, without correct options |
| Challenge | Organizer-only `challenge_GT.json` | **Private; do not commit or distribute** |

Train and validation splits are not yet identified. Their directories are placeholders and should not be treated as released sets. See [split layout](../data/README.md). Freeze source versions and ID coverage before opening submissions. The public challenge file and baseline predictions must not contain `correct_option_id`; the repository checks this before release.
