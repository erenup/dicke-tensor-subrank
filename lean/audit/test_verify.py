#!/usr/bin/env python3
"""Pre-build, fail-closed controls for source integrity and build evidence.

These tests compile no Lean and use explicitly synthetic receipt fixtures. The
fresh mathematical build and its actual rejection controls run in verify.py.
"""
from contextlib import contextmanager
import copy
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
import verify as audit

COUNT = 0


def passed(name):
    global COUNT
    COUNT += 1
    print('PASS', name)


def reject(name, operation, expected):
    try:
        operation()
    except SystemExit as error:
        audit.need(str(error) == 'FAIL: ' + expected,
                   'unexpected rejection for ' + name + ': ' + str(error))
        passed(name)
    else:
        raise SystemExit('FAIL: corruption accepted: ' + name)


@contextmanager
def fixture():
    parent = audit.ROOT / '.lake'
    parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='audit-control-', dir=parent) as directory:
        root = Path(directory)
        for name in audit.check_inputs():
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(audit.read(audit.ROOT, name))
        audit.check_inputs(root)
        yield root


def valid_axioms(wrapped=False, values='propext, Classical.choice, Quot.sound'):
    separator = '\n  ' if wrapped else ''
    return ''.join("'TR28." + name + "' depends on axioms: [" + separator + values + ']\n'
                   for name in audit.TARGETS.values())


def source_controls():
    audit.need(len(audit.check_inputs()) == 22, 'complete input count differs')
    passed('current-inputs-and-22-literal-alias-probes')
    for name in sorted(audit.bound_names()):
        with fixture() as root:
            path = root / name
            path.write_bytes(path.read_bytes() + b'\n-- modified\n')
            reject('modified-' + name, lambda: audit.check_inputs(root), 'bound input drift: ' + name)
    with fixture() as root:
        (root / 'TR28/Definitions.lean').unlink()
        reject('missing-definition', lambda: audit.check_inputs(root),
               'missing/linked input: TR28/Definitions.lean')
    for name in ['TR28/Nested/Extra.lean', 'audit/extra.py']:
        with fixture() as root:
            path = root / name; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('extra\n')
            reject('unbound-' + name, lambda: audit.check_inputs(root), 'project input inventory differs')
    with fixture() as root:
        path = root / 'TR28/Statement.lean'; path.unlink()
        path.symlink_to(audit.ROOT / 'TR28/Statement.lean')
        reject('linked-statement', lambda: audit.check_inputs(root),
               'missing/linked input: TR28/Statement.lean')
    with fixture() as root:
        (root / 'injected').symlink_to(audit.ROOT / 'TR28', target_is_directory=True)
        reject('linked-directory', lambda: audit.check_inputs(root), 'linked project member')
    with fixture() as root:
        path = root / audit.MANIFEST
        path.write_bytes(path.read_bytes() + b'\n')
        reject('changed-manifest', lambda: audit.check_inputs(root), 'input manifest drift')
    for schema in [True, 0, '1']:
        with fixture() as root:
            path = root / audit.MANIFEST; data = audit.load(path); data['schema'] = schema
            audit.save(path, data)
            old = audit.MANIFEST_SHA
            try:
                audit.MANIFEST_SHA = audit.sha(path.read_bytes())
                reject('invalid-manifest-schema-' + str(schema), lambda: audit.check_inputs(root),
                       'input manifest schema differs')
            finally:
                audit.MANIFEST_SHA = old
    with fixture() as root:
        # Even a rewritten inventory cannot redefine the fixed statement.
        path = root / 'TR28/Statement.lean'; path.write_bytes(path.read_bytes() + b'\n')
        manifest = root / audit.MANIFEST; data = audit.load(manifest)
        data['files']['TR28/Statement.lean'] = audit.sha(path.read_bytes()); audit.save(manifest, data)
        old = audit.MANIFEST_SHA
        try:
            audit.MANIFEST_SHA = audit.sha(manifest.read_bytes())
            reject('retargeted-fixed-statement', lambda: audit.check_inputs(root),
                   'fixed statement drift: TR28/Statement.lean')
        finally:
            audit.MANIFEST_SHA = old
    for token in ['axiom bad : False', 'example : False := by sorry', 'unsafe def bad := 0',
                  'macro "bad" : term => `(True)', 'elab "bad" : term => return Lean.mkConst ``True',
                  'set_option debug.skipKernelTC true', 'example : True := by native_decide']:
        with fixture() as root:
            path = root / 'TR28/Proofs.lean'; path.write_text(path.read_text() + '\n' + token + '\n')
            reject('forbidden-' + token.split()[0], lambda: audit.check_lean(root),
                   'forbidden Lean source command: TR28/Proofs.lean')
    with fixture() as root:
        path = root / 'audit/FinalProbe.lean'
        path.write_text(path.read_text().replace('example : PartnerPositionCount',
                                                'example : PartnerHistogramCount', 1))
        reject('changed-alias-probe', lambda: audit.check_lean(root), '22 exact-type examples differ')
    with fixture() as root:
        path = root / 'audit/FinalProbe.lean'
        path.write_text(path.read_text().replace('0 < k → A ⊆ E →', 'A ⊆ E →', 1))
        reject('weakened-literal-probe', lambda: audit.check_lean(root), '22 exact-type examples differ')


def output_controls():
    for output in [valid_axioms(), valid_axioms(True), valid_axioms(values=''),
                   valid_axioms(values='Quot.sound, propext')]:
        audit.check_outcome('FinalProbe', True, 0, output)
    passed('valid-wrapped-and-subset-axiom-output')
    for name, output, reason in [
        ('omitted-axiom', valid_axioms().split('\n', 1)[1], 'missing/extra axiom target'),
        ('extra-axiom-target', valid_axioms() + valid_axioms(), 'missing/extra axiom target'),
        ('axiom-residue', valid_axioms() + 'unrelated\n', 'unexpected probe output'),
        ('unexpected-axiom', valid_axioms(values='sorryAx'), 'unexpected axiom: TR28.partner_position_count'),
        ('duplicate-axiom', valid_axioms(values='propext, propext'), 'unexpected axiom: TR28.partner_position_count'),
    ]:
        reject(name, lambda output=output: audit.check_outcome('FinalProbe', True, 0, output), reason)
    negative = 'file.lean:1:1: error: unsolved goals\n⊢ False\n'
    audit.check_outcome('WrongKernelCount', False, 1, negative)
    passed('mathematical-negative-output')
    for name, code, output, reason in [
        ('accepted-negative', 0, negative, 'negative control did not fail mathematically: WrongKernelCount'),
        ('infrastructure-negative', 1, negative + 'unknown module\n', 'infrastructure failure in negative control: WrongKernelCount'),
        ('two-negative-errors', 1, negative + negative, 'negative control did not fail mathematically: WrongKernelCount'),
        ('positive-returncode', 1, '', 'positive compile failed: WrongKernelCount'),
    ]:
        reject(name, lambda code=code, output=output, name=name: audit.check_outcome(
            'WrongKernelCount', name == 'positive-returncode', code, output), reason)
    reject('over-memory-budget', lambda: audit.check_usage(
        'Maximum resident set size (kbytes): 7340033\nExit status: 0\n', 0), 'resource bound exceeded/missing')
    reject('resource-exit-mismatch', lambda: audit.check_usage(
        'Maximum resident set size (kbytes): 1024\nExit status: 1\n', 0), 'resource exit status differs')


def synthetic_receipt(root):
    """A parser fixture, never evidence that Lean accepted any source."""
    run = root / '.lake/synthetic'; run.mkdir(parents=True)
    for directory in ['inputs', 'projectownlib', 'logs']:
        (run / directory).mkdir()
    inputs = audit.check_inputs(root)
    for name in inputs:
        target = run / 'inputs' / name; target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(audit.read(root, name))
    environment = {'lean': str(root / '.lake/synthetic-lean'), 'lean_sha256': '0' * 64,
        'lean_version': 'Lean (version 4.34.0-rc2, synthetic, commit ' + audit.LEAN_COMMIT + ', Release)',
        'packages': {n: {'rev': r, 'tracked_diff_empty': True} for n, r in audit.REVS.items()},
        'libraries': [str((root / '.lake/packages' / n / '.lake/build/lib/lean').resolve())
                      for n in audit.REVS if n != 'Cli']}
    record = {'schema': 1, 'status': 'PASS', 'project_root': str(root), 'run_dir': str(run),
        'inputs': inputs, 'cleanup': {'argv': ['lake', 'clean', 'tr28'], 'cwd': str(root), 'returncode': 0},
        'environment_before': environment, 'environment_after': copy.deepcopy(environment),
        'lean_path': [str(run / 'projectownlib')] + environment['libraries'],
        'initial_objects': [], 'results': [], 'total_seconds': 1.0}
    for name, kind, source, accepted in audit.expected_jobs():
        stem = name.replace('.', '_')
        log = valid_axioms() if kind == 'probe' else ('' if accepted else
            'file.lean:1:1: error: unsolved goals\n⊢ False\n')
        code = 0 if accepted else 1
        usage = 'Maximum resident set size (kbytes): 1024\nExit status: ' + str(code) + '\n'
        (run / 'logs' / (stem + '.log')).write_text(log)
        (run / 'logs' / (stem + '.time')).write_text(usage)
        row = {'name': name, 'kind': kind, 'source': source, 'source_sha256': inputs[source],
            'argv': audit.argv_for(environment['lean'], name, kind, source), 'cwd': '.',
            'expected_accept': accepted, 'returncode': code, 'timed_out': False, 'seconds': 0.01,
            'log_sha256': audit.sha(log.encode()), 'resource_sha256': audit.sha(usage.encode())}
        if kind == 'module':
            row['artifacts'] = {}
            for suffix in ['.olean', '.olean.private', '.olean.server']:
                relative = name.replace('.', '/') + suffix
                data = ('SYNTHETIC ONLY ' + relative).encode()
                path = run / 'projectownlib' / relative; path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
                row['artifacts'][relative] = {'bytes': len(data), 'sha256': audit.sha(data)}
        record['results'].append(row)
    path = run / 'RECEIPT.json'; audit.save(path, record)
    audit.check_receipt(path, root)
    return path, record


def receipt_controls():
    cases = {
        'incomplete': 'incomplete build receipt',
        'omitted-module': 'omitted/extra build target',
        'changed-input': 'copied input drift/inventory',
        'changed-object': 'compiled object drift',
        'changed-sidecar': 'compiled object drift',
        'changed-log': 'log/resource drift',
        'changed-command': 'build command differs',
        'extra-cached-object': 'fresh object inventory differs',
        'changed-dependency': 'environment changed during build',
        'injected-library': 'dependency library bindings differ',
        'run-directory': 'receipt run directory differs',
        'wrong-search-path': 'Lean search path differs',
        'not-fresh': 'build was not fresh',
        'cleanup-dependencies': 'project cleanup differs',
        'over-time': '90-minute allowance exceeded',
    }
    for case, expected in cases.items():
        with fixture() as root:
            receipt, record = synthetic_receipt(root)
            run = receipt.parent
            def append(relative):
                path = run / relative; path.write_bytes(path.read_bytes() + b'corruption')
            if case == 'incomplete': record['status'] = 'RUNNING'
            elif case == 'omitted-module': record['results'].pop(2)
            elif case == 'changed-input': append('inputs/TR28/Statement.lean')
            elif case == 'changed-object': append('projectownlib/TR28/Counting.olean')
            elif case == 'changed-sidecar': append('projectownlib/TR28/Counting.olean.private')
            elif case == 'changed-log': append('logs/TR28_Counting.log')
            elif case == 'changed-command': record['results'][0]['argv'].append('--trust=999')
            elif case == 'extra-cached-object': (run / 'projectownlib/Injected.olean').write_bytes(b'injected')
            elif case == 'changed-dependency': record['environment_after']['packages']['mathlib']['rev'] = '0' * 40
            elif case == 'injected-library':
                for key in ['environment_before', 'environment_after']:
                    record[key]['libraries'].append(str(run / 'injected-library'))
                record['lean_path'].append(str(run / 'injected-library'))
            elif case == 'run-directory': record['run_dir'] = str(run / 'other')
            elif case == 'wrong-search-path': record['lean_path'][0] = str(root / '.lake/build/lib/lean')
            elif case == 'not-fresh': record['initial_objects'] = ['TR28.olean']
            elif case == 'cleanup-dependencies': record['cleanup']['argv'] = ['lake', 'clean']
            elif case == 'over-time': record['total_seconds'] = 5401
            audit.save(receipt, record)
            reject('receipt-' + case, lambda: audit.check_receipt(receipt, root), expected)


def main():
    audit.need(len(sys.argv) == 1, 'usage: python audit/test_verify.py')
    source_controls()
    output_controls()
    receipt_controls()
    print('PASS', COUNT, 'pre-build integrity controls; no Lean build performed')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, UnicodeError) as error:
        raise SystemExit('FAIL: test fixture: ' + type(error).__name__)
