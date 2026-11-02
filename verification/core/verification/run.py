#!/usr/bin/env python3
"""Authenticate the TR-28 proof bindings and run exact supporting checks."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
MODES = [('normal', [], '1'), ('optimized', ['-O'], '1'), ('hash-seed', [], '8675309')]
CHECKERS = {
    'check_entropy.py': (
        'd960b32bb7668c28557351aea90d9d378d0f8f406a0f7fdb44c3ba5bb502417d',
        '8a5475b6c07384f9f287395a0acf9506aeea91b8c21ec41800f0f475e8ac1fc2'),
    'check_hashing.py': (
        'f11773baa27df67c0aeb83675fe5e487759d9e4ad6e8c01140a4ad47f2ad154c',
        'f9abf354872f883b09f496b6131969a353be4e3890a9ae0e13c3d9c59466cb25'),
}
SOURCE_PROOFS = {
    'PROOF.md': 'de6b1e56044a2810b640fa1ad22efc25be23e10be87032e813b58cd2066a4457',
    'STATEMENT.md': 'b3fcc672ce9dd5701ea2a213eb95e7ffee36446f74598df64d00d48095094150',
    'SOURCES.md': '214f20bebf1733235fad830bea31ddacfd72c6d51575a865e7eea690769d11a0',
}
CURATED_PROOFS = {
    'PROOF.md': 'de6b1e56044a2810b640fa1ad22efc25be23e10be87032e813b58cd2066a4457',
    'STATEMENT.md': 'f686f95d1405506121596c61c72b11ee0214fa9c3be7fe31899413d0bb809ba5',
    'SOURCES.md': '61f98d583c4b12f30292651b1eb151daf4e4be5c7a989d4adf7604f70193fcf9',
}
FILES = {'README.md', 'run.py', 'CHECKERS.txt', 'SOURCE_BINDINGS.txt', 'SHA256SUMS'} | set(CHECKERS)


def need(condition, message):
    if not condition:
        raise SystemExit('FAIL: ' + message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique_pairs(pairs):
    result = {}
    for name, value in pairs:
        need(name not in result, 'duplicate JSON key')
        result[name] = value
    return result


def reject_number(value):
    raise SystemExit('FAIL: non-integer JSON number')


def read_json(data):
    return json.loads(data, object_pairs_hook=unique_pairs,
                      parse_float=reject_number, parse_constant=reject_number)


def inventory(directory):
    need(directory.is_dir() and not directory.is_symlink(), 'invalid directory')
    files = {}
    for path in directory.iterdir():
        need(path.is_file() and not path.is_symlink(), 'unexpected directory or linked file')
        need(path.stat().st_size <= 4500000, 'file too large')
        files[path.name] = path.read_bytes()
    return files


def proof_hashes():
    files = inventory(HERE.parent / 'proofs')
    need(set(files) == set(SOURCE_PROOFS), 'proof inventory')
    return {name: digest(data) for name, data in files.items()}


def validate(files, proofs):
    need(set(files) == FILES, 'verification inventory')
    entries = {}
    for line in files['SHA256SUMS'].decode().splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  ([A-Za-z0-9_.]+)', line)
        need(match is not None, 'manifest syntax')
        value, name = match.groups()
        need(name not in entries, 'duplicate manifest entry')
        entries[name] = value
    need(set(entries) == FILES - {'SHA256SUMS'}, 'manifest coverage')
    for name, value in entries.items():
        need(digest(files[name]) == value, 'manifest mismatch: ' + name)
    for name, (source, output) in CHECKERS.items():
        need(digest(files[name]) == source, 'checker source changed: ' + name)
    registry = ''.join(name + ' ' + output + '\n'
                       for name, (source, output) in sorted(CHECKERS.items()))
    need(files['CHECKERS.txt'] == registry.encode(), 'registered output differs')
    binding = {}
    for line in files['SOURCE_BINDINGS.txt'].decode().splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  ([0-9a-f]{64})  ([A-Za-z_.]+)', line)
        need(match is not None, 'proof binding syntax')
        source, curated, name = match.groups()
        need(name in SOURCE_PROOFS and source == SOURCE_PROOFS[name], 'source proof binding')
        need(name not in binding, 'duplicate proof binding')
        binding[name] = curated
    need(binding == proofs == CURATED_PROOFS, 'proof binding mismatch')
    for name in sorted(set(CHECKERS) | {'run.py'}):
        tree = ast.parse(files[name].decode(), filename=name)
        for node in ast.walk(tree):
            need(not isinstance(node, ast.Assert), 'optimization-sensitive assertion')
            need(not (isinstance(node, ast.Constant) and
                      type(node.value).__name__ in {'float', 'complex'}), 'inexact arithmetic literal')
            if name in CHECKERS and isinstance(node, (ast.Import, ast.ImportFrom)):
                roots = [n.name.split('.')[0] for n in node.names] if isinstance(node, ast.Import) else [node.module]
                need(all(n in {'collections', 'itertools', 'fractions', 'math', 'json'} for n in roots),
                     'unexpected checker import')
    return True


def reseal(files):
    files['SHA256SUMS'] = ''.join(digest(data) + '  ' + name + '\n'
        for name, data in sorted(files.items()) if name != 'SHA256SUMS').encode()
    return files


def integrity_controls(files, proofs):
    cases = []
    for name in CHECKERS:
        bad = dict(files); bad[name] += b'\n'
        cases.append((bad, proofs, 'manifest mismatch: ' + name))
        cases.append((reseal(dict(bad)), proofs, 'checker source changed: ' + name))
    bad = dict(files); del bad['check_entropy.py']
    cases.append((bad, proofs, 'verification inventory'))
    bad = dict(files); bad['extra.txt'] = b'extra'
    cases.append((bad, proofs, 'verification inventory'))
    bad = dict(files); bad['SHA256SUMS'] += files['SHA256SUMS'].splitlines(keepends=True)[0]
    cases.append((bad, proofs, 'duplicate manifest entry'))
    bad = dict(files); bad['SHA256SUMS'] = b'not a manifest\n'
    cases.append((bad, proofs, 'manifest syntax'))
    bad = dict(files); bad['SHA256SUMS'] = b''
    cases.append((bad, proofs, 'manifest coverage'))
    bad = dict(files); bad['CHECKERS.txt'] = b'check_entropy.py ' + b'0'*64 + b'\n'
    cases.append((reseal(bad), proofs, 'registered output differs'))
    bad = dict(files); bad['SOURCE_BINDINGS.txt'] = files['SOURCE_BINDINGS.txt'].replace(
        SOURCE_PROOFS['PROOF.md'].encode(), b'0'*64, 1)
    cases.append((reseal(bad), proofs, 'source proof binding'))
    bad = dict(files); bad['SOURCE_BINDINGS.txt'] += files['SOURCE_BINDINGS.txt'].splitlines(keepends=True)[0]
    cases.append((reseal(bad), proofs, 'duplicate proof binding'))
    bad = dict(files); bad['SOURCE_BINDINGS.txt'] = b''
    cases.append((reseal(bad), proofs, 'proof binding mismatch'))
    for name in CURATED_PROOFS:
        changed = dict(proofs); changed[name] = '0'*64
        cases.append((files, changed, 'proof binding mismatch'))
    for bad, changed, expected in cases:
        try:
            validate(bad, changed)
        except SystemExit as error:
            need(str(error) == 'FAIL: ' + expected, 'wrong integrity-control rejection')
        else:
            raise SystemExit('FAIL: integrity control accepted')
    return len(cases)


def main():
    files = inventory(HERE); proofs = proof_hashes()
    validate(files, proofs)
    count = integrity_controls(files, proofs)
    for name, (source, output) in sorted(CHECKERS.items()):
        previous = None
        for mode, flags, seed in MODES:
            command = [sys.executable, '-S', '-s', '-B', *flags, str(HERE / name)]
            env = {'PATH': os.defpath, 'LC_ALL': 'C.UTF-8', 'PYTHONHASHSEED': seed}
            result = subprocess.run(command, cwd=HERE, env=env, stdin=subprocess.DEVNULL,
                                    capture_output=True, timeout=600)
            need(result.returncode == 0 and not result.stderr, 'checker failed: ' + name + ' ' + mode)
            need(digest(result.stdout) == output, 'checker output: ' + name + ' ' + mode)
            need(previous is None or previous == result.stdout, 'checker mode mismatch: ' + name)
            previous = result.stdout
            parsed = read_json(result.stdout)
            need(isinstance(parsed, dict) and 'scope' in parsed, 'missing checker scope')
        print('PASS: ' + name + ' (normal, optimized, hash-seed; registered output)')
    need(inventory(HERE) == files and proof_hashes() == proofs, 'inputs changed during execution')
    print('PASS: ' + str(count) + ' integrity controls; 3 proof bindings')
    print('RESULT: PASS TR-28 finite supporting checks')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, SyntaxError, UnicodeError, subprocess.TimeoutExpired) as error:
        raise SystemExit('FAIL: verification input: ' + type(error).__name__)
