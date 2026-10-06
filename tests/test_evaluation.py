import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('scoring', ROOT / 'evaluation/scoring.py')
scoring = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scoring)

class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.ref = json.loads((ROOT / 'examples/ref/reference.json').read_text())
        self.pred = json.loads((ROOT / 'examples/res/predictions.json').read_text())
    def test_perfect_and_shuffled(self):
        self.assertTrue(all(v == 100 for v in scoring.score(self.ref, self.pred[::-1]).values()))
    def test_missing_extra_duplicate(self):
        for pred in [self.pred[:-1], self.pred + [self.pred[0]], self.pred + [{'id':'extra','answer':self.pred[0]['answer']}]]:
            with self.assertRaises(ValueError): scoring.score(self.ref, pred)
    def test_invalid_value(self):
        self.pred[0]['answer'] = 'INVALID'
        with self.assertRaises(ValueError): scoring.score(self.ref, self.pred)
    def test_other_task_rejected(self):
        self.ref['task'] = 'other'
        with self.assertRaises(ValueError): scoring.score(self.ref, self.pred)
    def test_wrong_valid_prediction(self):
        self.pred[0]['answer'] = self.pred[1]['answer']
        result = scoring.score(self.ref, self.pred)
        self.assertAlmostEqual(result['accuracy'], 100 * (len(self.pred)-1) / len(self.pred))
