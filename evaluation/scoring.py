"""Dependency-free scoring core. Proposed contracts; real manifest adapters pending."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key')
        result[key] = value
    return result


def load_json(path):
    if path.stat().st_size > 50_000_000:
        raise ValueError('JSON file exceeds 50 MB')
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Nonfinite JSON value')))


def indexed(rows, value_key):
    if not isinstance(rows, list) or not rows:
        raise ValueError('Expected a nonempty list of records')
    result = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {'id', value_key}:
            raise ValueError('Each record must contain exactly id and ' + value_key)
        key = row['id']
        value = row[value_key]
        if not isinstance(key, str) or not key or key in result:
            raise ValueError('IDs must be nonempty unique strings')
        if not isinstance(value, str) or not value:
            raise ValueError('Predictions and labels must be nonempty strings')
        result[key] = value
    return result


def score(reference, predictions):
    task = reference.get('task')
    if task != 'vqa':
        raise ValueError('Unsupported reference task')
    field = 'label' if task == 'gar' else 'answer'
    truth = indexed(reference['records'], field)
    pred = indexed(predictions, field)
    if set(pred) != set(truth):
        raise ValueError('Submission must cover every expected ID exactly once, with no extra IDs')
    if task == 'gar':
        classes = reference.get('classes')
        if (not isinstance(classes, list) or not classes or
                any(not isinstance(c, str) or not c for c in classes) or len(set(classes)) != len(classes)):
            raise ValueError('Reference requires unique class names')
        if set(truth.values()) != set(classes):
            raise ValueError('Reference must contain every configured class; revise the split or protocol')
        if not set(pred.values()) <= set(classes):
            raise ValueError('Unknown predicted class')
    else:
        # Exact option IDs only. No inferred free-text normalization or model judging.
        options = reference.get('options')
        if not isinstance(options, dict) or set(options) != set(truth):
            raise ValueError('VQA reference must specify allowed options for every question')
        for key in truth:
            choices = options[key]
            if (not isinstance(choices, list) or not choices or
                    any(not isinstance(c, str) or not c for c in choices) or
                    len(set(choices)) != len(choices) or truth[key] not in choices):
                raise ValueError('Invalid VQA reference options')
            if pred[key] not in choices:
                raise ValueError('Unknown predicted answer option')
    correct = sum(pred[key] == value for key, value in truth.items())
    result = {'accuracy': 100.0 * correct / len(truth)}
    if task == 'gar':
        actual = Counter(truth.values())
        predicted = Counter(pred.values())
        tp = Counter(value for key, value in truth.items() if pred[key] == value)
        result['balanced_accuracy'] = 100.0 * sum(tp[c] / actual[c] for c in classes) / len(classes)
        result['macro_f1'] = 100.0 * sum(2 * tp[c] / (actual[c] + predicted[c]) for c in classes) / len(classes)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, default=Path('/app/input'))
    parser.add_argument('--output', type=Path, default=Path('/app/output'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    output = args.output / 'scores.json'
    output.unlink(missing_ok=True)
    try:
        reference = load_json(args.input / 'ref' / 'reference.json')
        predictions = load_json(args.input / 'res' / 'predictions.json')
        scores = score(reference, predictions)
        output.write_text(json.dumps(scores, allow_nan=False), encoding='utf-8')
        print('Scoring completed successfully.')
    except (ValueError, KeyError, TypeError, OSError):
        # Do not print private labels, paths, per-example results or participant strings.
        print('Scoring failed: check predictions.json format, ID coverage and allowed values.', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
