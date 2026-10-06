# Data

Dataset: [https://huggingface.co/datasets/SoccerNet/SN-VQA-2027](https://huggingface.co/datasets/SoccerNet/SN-VQA-2027).

Request access and follow the dataset card’s conditions. This repository does not redistribute the dataset.

The dataset card documents `test` and `challenge` splits. Each manifest contains a `data` list with video `inputs` and `streaming_vqa` questions. The scorer adapter cannot be finalized until the actual question/answer schema and private labels are supplied. Do not apply the 2026 multiple-choice schema automatically.

## Release requirements

Before opening submissions, freeze the release version, stable sample IDs, split boundaries and public versus private fields. Verify that final-ranking labels have not already been released. Keep ground truth outside public Git history.
