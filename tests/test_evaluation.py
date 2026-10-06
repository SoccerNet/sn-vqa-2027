import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'evaluation'))
spec = importlib.util.spec_from_file_location('scoring', ROOT / 'evaluation/scoring.py')
scoring = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scoring)


class EvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ref = json.loads((ROOT / 'data/test/test_GT.json').read_text())
        cls.baseline = json.loads((ROOT / 'data/test/test_submission.json').read_text())

    def test_public_baseline_score_matches_dimension_average(self):
        result = scoring.score(self.ref, self.baseline)
        self.assertEqual(set(result), {'score', 'unanswered', 'dim1_accuracy', 'dim2_accuracy', 'dim3_accuracy', 'dim4_accuracy'})
        self.assertAlmostEqual(result['score'], sum(result[f'dim{i}_accuracy'] for i in range(1, 5)) / 4)
        self.assertGreater(result['score'], 0)
        self.assertLess(result['score'], 100)

    def test_missing_and_extra_question_rejected(self):
        missing = copy.deepcopy(self.baseline)
        missing['data'][0]['streaming_vqa'].pop()
        with self.assertRaises(ValueError):
            scoring.score(self.ref, missing)
        extra = copy.deepcopy(self.baseline)
        extra['data'][0]['streaming_vqa'].append(copy.deepcopy(extra['data'][0]['streaming_vqa'][0]))
        with self.assertRaises(ValueError):
            scoring.score(self.ref, extra)

    def test_invalid_option_counts_as_incorrect(self):
        changed = copy.deepcopy(self.baseline)
        changed['data'][0]['streaming_vqa'][0]['prediction'] = 'not_an_option'
        result = scoring.score(self.ref, changed)
        self.assertGreaterEqual(result['unanswered'], 1)

    def test_challenge_public_files_have_no_ground_truth(self):
        for name in ('challenge_public.json', 'challenge_submission.json'):
            payload = json.loads((ROOT / 'data/challenge' / name).read_text())
            self.assertFalse(any('correct_option_id' in q for sample in payload['data'] for q in sample['streaming_vqa']))
            self.assertEqual(sum(len(sample['streaming_vqa']) for sample in payload['data']), 1158)
