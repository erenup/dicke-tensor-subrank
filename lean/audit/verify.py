#!/usr/bin/env python3
"""Audit fixed TR-28 sources and rebuild every target into a fresh isolated library.

The no-argument entry point expects the official pinned Mathlib cache to have
been installed with `lake exe cache get`. It never cleans or builds a dependency.
"""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'audit/input-hashes.json'
MANIFEST_SHA = 'f76c88f8439e52c5820227bcd51176cb1d89c8ba94d311e1ec86f17a690da1b9'
TOOLCHAIN = 'leanprover/lean4:v4.34.0-rc2'
LEAN_COMMIT = '6a10ac8c22beadecabdbb0919c2b50214762f91d'
FIXED = {'TR28/Definitions.lean': 'ba51baff6753f6c143b900f5289baf7fc59968aa68579a3a4d8e3fc8bba3d0eb',
         'TR28/Statement.lean': 'bd5dd1252e0a3fcae5e5858816f6dc404eef1ac8d5db74bcd4da83bd8fe9cbb6'}
BUDGET = 5400
MODULES = ['TR28.Definitions', 'TR28.Statement', 'TR28.Counting', 'TR28.LinearCount',
           'TR28.Isolation', 'TR28.Density', 'TR28.Proofs', 'TR28']
CONTROLS = ['Positive', 'WrongFullPartnerCount', 'WrongKernelCount',
            'CandidateOnlyIsolation', 'ZeroModeExtraction']
TARGETS = dict(zip(
    ['PartnerPositionCount', 'PartnerHistogramCount', 'BalancedPartnerCount',
     'ExactSpanPartnerSubset', 'ExactSpanPartnerBound', 'FiniteFieldKernelCount',
     'IsolationCountTheorem', 'ExactCoordinateExtraction', 'UniformIsolationExtraction',
     'InvariantSupermodularDensity', 'CoreTheorems'],
    ['partner_position_count', 'partner_histogram_count', 'balanced_partner_count',
     'exact_span_partner_subset', 'exact_span_partner_bound', 'finite_field_kernel_count',
     'isolation_count', 'exact_coordinate_extraction', 'uniform_isolation_extraction',
     'invariant_supermodular_density', 'core_theorems']))
AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
REVS = {'mathlib': '85e3a25e006c35636f0e53b0e9296caca2685bc0',
        'plausible': 'd9598f07b1bc701f1e3aae163d2681c1fd978793',
        'LeanSearchClient': 'ba67e212be1197b84c1f1f6299488a10a3002713',
        'importGraph': 'd8823026ac7ef130c253089d95685f9877b95323',
        'proofwidgets': 'a8acbfd87375ff4abe14ce09db5b7664d383bc7f',
        'aesop': '18889deb9e83ea7420ef51c160d6f88552e744e3',
        'Qq': '507746ab8f4b643ccdacb2ec4cdb5853fa9f8ab3',
        'batteries': 'd54dddc581e08be364c278052863524bff7a99a9',
        'Cli': 'ab3a82db9fea14cf0fd7f5a2de650f4b534640af'}
FORBIDDEN = re.compile(r'\b(sorry|admit|axiom|sorryAx|unsafe|implemented_by|extern|native_decide|'
    r'set_option|ofReduceBool|skipKernelTC|macro|elab|syntax|run_tac|run_elab|initialize|'
    r'builtin_initialize|opaque|partial)\b')

def need(ok, message):
    if not ok:
        raise SystemExit('FAIL: ' + message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read(root, name):
    rel = Path(name)
    need(not rel.is_absolute() and '..' not in rel.parts, 'unsafe relative path')
    path = root / rel
    need(path.is_file() and not any(root.joinpath(*rel.parts[:i]).is_symlink()
                                   for i in range(len(rel.parts) + 1)),
         'missing/linked input: ' + name)
    return path.read_bytes()

def load(path):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            need(key not in out, 'duplicate JSON key')
            out[key] = value
        return out
    return json.loads(path.read_bytes(), object_pairs_hook=unique)

def inventory(root):
    need(root.is_dir() and not root.is_symlink(), 'invalid inventory directory')
    result = {}
    def unreadable(error):
        raise error
    for directory, dirs, files in os.walk(root, onerror=unreadable):
        for name in sorted(dirs + files):
            path = Path(directory) / name
            need(not path.is_symlink(), 'linked inventory member')
            if path.is_file():
                result[path.relative_to(root).as_posix()] = sha(path.read_bytes())
            else:
                need(path.is_dir(), 'special inventory member')
    return result

def source_name(module):
    return module.replace('.', '/') + '.lean'

def bound_names():
    return set(map(source_name, MODULES)) | {
        'lean-toolchain', 'lakefile.toml', 'lake-manifest.json', 'verify',
        'audit/TARGETS.json', 'audit/FinalProbe.lean',
    } | {'audit/controls/' + n + '.lean' for n in CONTROLS}


def project_inventory(root):
    """All project files except build state and the two prose documents."""
    need(root.is_dir() and not root.is_symlink(), 'invalid project directory')
    files = {}
    def unreadable(error):
        raise error
    for directory, dirs, names in os.walk(root, onerror=unreadable):
        directory = Path(directory)
        if directory == root:
            dirs[:] = [n for n in dirs if n not in {'.lake', '.git'}]
            names = [n for n in names if n != '.git']
        for name in dirs + names:
            need(not (directory / name).is_symlink(), 'linked project member')
        for name in names:
            path = directory / name
            need(path.is_file(), 'special project member')
            relative = path.relative_to(root).as_posix()
            if relative not in {'README.md', 'SCOPE.md'}:
                files[relative] = sha(path.read_bytes())
    return files


def check_inputs(root=ROOT):
    root = Path(root)
    raw = read(root, MANIFEST)
    need(sha(raw) == MANIFEST_SHA, 'input manifest drift')
    manifest = load(root / MANIFEST)
    need(set(manifest) == {'schema', 'files'} and type(manifest['schema']) is int
         and manifest['schema'] == 1, 'input manifest schema differs')
    bindings = manifest['files']
    need(type(bindings) is dict and set(bindings) == bound_names(), 'bound input inventory differs')
    for name, digest in bindings.items():
        need(type(digest) is str and re.fullmatch('[0-9a-f]{64}', digest) is not None,
             'malformed input digest')
        need(sha(read(root, name)) == digest, 'bound input drift: ' + name)
    for name, digest in FIXED.items():
        need(bindings[name] == digest, 'fixed statement drift: ' + name)
    actual = project_inventory(root)
    need(set(actual) == bound_names() | {MANIFEST, 'audit/verify.py', 'audit/test_verify.py'},
         'project input inventory differs')
    need(read(root, 'lean-toolchain').decode().strip() == TOOLCHAIN, 'toolchain drift')
    packages = load(root / 'lake-manifest.json')['packages']
    need(len(packages) == len(REVS) and {p['name']: p['rev'] for p in packages} == REVS,
         'dependency manifest drift')
    need(load(root / 'audit/TARGETS.json') == {'TR28.' + a: 'TR28.' + b for a, b in TARGETS.items()},
         'target registry differs')
    check_lean(root)
    return actual


def lean_code(text):
    out = []; index = 0; depth = 0
    while index < len(text):
        if text.startswith('/-', index): depth += 1; index += 2
        elif depth and text.startswith('-/', index): depth -= 1; index += 2
        elif depth: index += 1
        elif text.startswith('--', index):
            end = text.find('\n', index)
            index = len(text) if end < 0 else end
        else: out.append(text[index]); index += 1
    need(depth == 0, 'unclosed Lean comment')
    return ''.join(out)

def check_lean(root):
    imports = {}
    lean_files = list(map(source_name, MODULES)) + ['audit/FinalProbe.lean'] + [
        'audit/controls/' + n + '.lean' for n in CONTROLS]
    for name in lean_files:
        code = lean_code(read(root, name).decode())
        # The probe's observational commands do not declare axioms.
        scanned = re.sub(r'^#print axioms TR28\.[a-z_]+\s*$', '', code, flags=re.M)
        need(not FORBIDDEN.search(scanned), 'forbidden Lean source command: ' + name)
        need(not re.search(r'^\s*#', scanned, re.M), 'unregistered Lean command: ' + name)
        deps = []
        for line in code.splitlines():
            if re.search(r'\bimport\b', line):
                match = re.fullmatch(r'import ([A-Za-z0-9_.]+)', line)
                need(match is not None, 'nonliteral import: ' + name)
                dep = match[1]
                need(dep.startswith('Mathlib.') or dep in MODULES, 'unregistered import: ' + dep)
                if name in set(map(source_name, MODULES)) and dep in MODULES:
                    need(MODULES.index(dep) < MODULES.index(name[:-5].replace('/', '.')), 'non-topological own import')
                deps.append(dep)
        imports[name] = deps
    probe = lean_code(read(root, 'audit/FinalProbe.lean').decode())
    examples = re.findall(r'example\s*:\s*(.*?)\s*:=\s*([a-z_]+)', probe, re.S)
    statement = lean_code(read(root, 'TR28/Statement.lean').decode())
    bodies = dict(re.findall(r'def (\w+) : Prop :=\s*(.*?)(?=\n\s*def |\nend TR28)', statement, re.S))
    norm = lambda text: ' '.join(text.split())
    expected = [(name, theorem) for name, theorem in TARGETS.items()] + [
        (norm(bodies[name]), theorem) for name, theorem in TARGETS.items()]
    need([(norm(body), theorem) for body, theorem in examples] == expected, '22 exact-type examples differ')
    need(re.findall(r'^#print axioms (TR28\.[a-z_]+)$', probe, re.M) == [
        'TR28.' + n for n in TARGETS.values()], 'axiom probe inventory differs')
    return imports

def clean_environment():
    env = os.environ.copy()
    for key in list(env):
        if key.startswith(('LEAN_', 'LAKE_')) or key in {'LD_PRELOAD', 'LD_LIBRARY_PATH'}:
            env.pop(key)
    env.update(LC_ALL='C', GIT_OPTIONAL_LOCKS='0', LAKE_ARTIFACT_CACHE='false',
               LAKE_RESTORE_ARTIFACTS='false', OMP_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2',
               MKL_NUM_THREADS='2', NUMEXPR_NUM_THREADS='2')
    return env


def capture(args, root, env):
    result = subprocess.run(args, cwd=root, env=env, capture_output=True, text=True,
                            encoding='utf-8', timeout=60, check=False)
    need(result.returncode == 0 and not result.stderr, 'environment command failed: ' + args[0])
    return result.stdout.strip()


def dependency_state(root, env):
    packages = {}
    libraries = []
    for name, revision in REVS.items():
        package = root / '.lake/packages' / name
        need(package.is_dir(), 'missing pinned package: ' + name)
        actual = capture(['git', 'rev-parse', 'HEAD'], package, env)
        diff = capture(['git', 'diff', '--no-ext-diff', 'HEAD', '--'], package, env)
        need(actual == revision and not diff, 'dependency source drift: ' + name)
        library = package / '.lake/build/lib/lean'
        if library.is_dir():
            need(not (library / 'TR28').exists() and not (library / 'TR28.olean').exists(),
                 'dependency library contains project objects')
            libraries.append(str(library.resolve()))
        else:
            need(name == 'Cli', 'missing official dependency library: ' + name)
        packages[name] = {'rev': actual, 'tracked_diff_empty': True}
    need(len(libraries) == len(set(libraries)), 'duplicate dependency library')
    return {'packages': packages, 'libraries': libraries}


def environment(root):
    env = clean_environment()
    # Lake selects the pinned toolchain. Its project-object search path is discarded.
    expression = 'import shutil; print(shutil.which("lean") or "")'
    binary = Path(capture(['lake', 'env', sys.executable, '-B', '-c', expression], root, env))
    need(binary.is_absolute() and binary.is_file(), 'missing pinned compiler')
    version = capture([str(binary), '--version'], root, env)
    need(version.startswith('Lean (version 4.34.0-rc2, ') and
         'commit ' + LEAN_COMMIT + ', Release)' in version, 'compiler version differs')
    library = Path(capture([str(binary), '--print-libdir'], root, env))
    need(library.is_dir() and not (library / 'TR28').exists() and not (library / 'TR28.olean').exists(),
         'compiler library contains project objects')
    return {'lean': str(binary.resolve()), 'lean_sha256': sha(binary.read_bytes()),
            'lean_version': version, **dependency_state(root, env)}


def clean_project(root):
    # A named package cleans only that package's build directory, never dependencies.
    command = ['lake', 'clean', 'tr28']
    capture(command, root, clean_environment())
    return {'argv': command, 'cwd': str(root), 'returncode': 0}


def expected_jobs():
    return [(m, 'module', source_name(m), True) for m in MODULES] + [
        ('FinalProbe', 'probe', 'audit/FinalProbe.lean', True)] + [
        (n, 'control', 'audit/controls/' + n + '.lean', n == 'Positive') for n in CONTROLS]


def argv_for(binary, name, kind, source):
    args = ['/usr/bin/time', '-v', '-o', 'logs/' + name.replace('.', '_') + '.time',
            binary, '-j2', '-M6000', '-R', 'inputs']
    if kind == 'module':
        args += ['-o', 'projectownlib/' + name.replace('.', '/') + '.olean']
    return args + ['inputs/' + source]


def check_outcome(name, accepted, returncode, output):
    errors = re.findall(r'\berror(?:\([^\n)]*\))?:', output, re.I)
    need('warning:' not in output.lower(), 'compiler warning: ' + name)
    if accepted:
        need(returncode == 0 and not errors, 'positive compile failed: ' + name)
    else:
        need(returncode == 1 and len(errors) == 1 and
             len(re.findall(r'error(?:\([^\n)]*\))?: unsolved goals', output)) == 1 and
             re.search(r'^⊢ False\s*$', output, re.M) is not None,
             'negative control did not fail mathematically: ' + name)
        need(not re.search(r'unknown|missing|does not exist|failed to synthesize|unexpected token|'
                           r'heartbeat|recursion|allocation|out of memory|timeout|killed|interrupted', output, re.I),
             'infrastructure failure in negative control: ' + name)
    if name == 'FinalProbe':
        entries = re.compile(r"^'([^'\n]+)' depends on axioms:\s*\[([^]]*)\]", re.M)
        pairs = entries.findall(output)
        need([n for n, _ in pairs] == ['TR28.' + n for n in TARGETS.values()], 'missing/extra axiom target')
        need(not entries.sub('', output).strip(), 'unexpected probe output')
        for target, values in pairs:
            items = [] if not values.strip() else [s.strip() for s in values.split(',')]
            need(len(items) == len(set(items)) and set(items) <= AXIOMS, 'unexpected axiom: ' + target)

def check_usage(raw, returncode):
    rss = re.findall(r'Maximum resident set size \(kbytes\): (\d+)', raw)
    exit_status = re.findall(r'Exit status: (\d+)', raw)
    need(len(rss) == 1 and 0 < int(rss[0]) <= 7 * 1024 * 1024,
         'resource bound exceeded/missing')
    need(type(returncode) is int and exit_status == [str(returncode)], 'resource exit status differs')


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def check_receipt(path, root=ROOT, live=False):
    path = Path(path).resolve(); run = path.parent; root = Path(root).resolve()
    record = load(path)
    need(type(record['schema']) is int and record['schema'] == 1 and record['status'] == 'PASS',
         'incomplete build receipt')
    need(record['project_root'] == str(root), 'project root differs')
    need(record['run_dir'] == str(run), 'receipt run directory differs')
    need(record['cleanup'] == {'argv': ['lake', 'clean', 'tr28'], 'cwd': str(root), 'returncode': 0}
         and type(record['cleanup']['returncode']) is int, 'project cleanup differs')
    inputs = check_inputs(root)
    need(record['inputs'] == inputs, 'receipt input bindings differ')
    need(inventory(run / 'inputs') == inputs, 'copied input drift/inventory')
    need(check_inputs(run / 'inputs') == inputs, 'copied source checks differ')
    before = record['environment_before']
    need(before == record['environment_after'], 'environment changed during build')
    need(before['packages'] == {n: {'rev': r, 'tracked_diff_empty': True} for n, r in REVS.items()},
         'dependency receipt differs')
    libraries = [str((root / '.lake/packages' / n / '.lake/build/lib/lean').resolve())
                 for n in REVS if n != 'Cli']
    cli = str((root / '.lake/packages/Cli/.lake/build/lib/lean').resolve())
    need(before['libraries'] in [libraries, libraries + [cli]], 'dependency library bindings differ')
    need(Path(before['lean']).is_absolute() and
         re.fullmatch('[0-9a-f]{64}', before['lean_sha256']) is not None, 'compiler receipt differs')
    need(before['lean_version'].startswith('Lean (version 4.34.0-rc2, ') and
         'commit ' + LEAN_COMMIT + ', Release)' in before['lean_version'], 'compiler version differs')
    if live:
        need(environment(root) == before, 'live environment differs')
    need(record['initial_objects'] == [], 'build was not fresh')
    need(record['lean_path'] == [str(run / 'projectownlib')] + before['libraries'],
         'Lean search path differs')
    jobs = expected_jobs(); results = record['results']
    need(len(results) == len(jobs), 'omitted/extra build target')
    objects = {}; logs = set()
    for row, (name, kind, source, accepted) in zip(results, jobs):
        need((row['name'], row['kind'], row['source'], row['expected_accept']) ==
             (name, kind, source, accepted), 'build target order differs')
        need(row['argv'] == argv_for(before['lean'], name, kind, source) and row['cwd'] == '.',
             'build command differs')
        need(row['source_sha256'] == inputs[source], 'compiled source differs')
        need(row['timed_out'] is False and type(row['seconds']) in {int, float}
             and 0 < row['seconds'] <= BUDGET, 'timeout/invalid elapsed time')
        stem = name.replace('.', '_')
        log = read(run, 'logs/' + stem + '.log'); usage = read(run, 'logs/' + stem + '.time')
        logs |= {stem + '.log', stem + '.time'}
        need(sha(log) == row['log_sha256'] and sha(usage) == row['resource_sha256'], 'log/resource drift')
        check_usage(usage.decode(), row['returncode'])
        check_outcome(name, accepted, row['returncode'], log.decode())
        if kind == 'module':
            obj = name.replace('.', '/') + '.olean'
            artifacts = row['artifacts']
            need(obj in artifacts and set(artifacts) <= {
                obj, obj + '.private', obj + '.server', name.replace('.', '/') + '.ilean'},
                 'module artifact inventory differs')
            for relative, info in artifacts.items():
                data = read(run, 'projectownlib/' + relative)
                need(type(info['bytes']) is int and len(data) > 0 and len(data) == info['bytes']
                     and sha(data) == info['sha256'], 'compiled object drift')
                need(relative not in objects, 'duplicate compiled artifact')
                objects[relative] = info['sha256']
        else:
            need('artifacts' not in row, 'unexpected probe object')
    need(inventory(run / 'projectownlib') == objects, 'fresh object inventory differs')
    need(set(inventory(run / 'logs')) == logs, 'log inventory differs')
    need(type(record['total_seconds']) in {int, float} and 0 < record['total_seconds'] <= BUDGET,
         '90-minute allowance exceeded')
    return record


def verify(root=ROOT):
    root = Path(root).resolve()
    started = time.monotonic()
    inputs = check_inputs(root)
    cleanup = clean_project(root)
    before = environment(root)
    run = root / '.lake' / ('audit-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    run.mkdir(parents=True, exist_ok=False)
    for directory in ['inputs', 'projectownlib', 'logs']:
        (run / directory).mkdir()
    for name in inputs:
        target = run / 'inputs' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(read(root, name))
    need(not inventory(run / 'projectownlib'), 'own library not initially empty')
    lean_path = [str(run / 'projectownlib')] + before['libraries']
    env = clean_environment(); env['LEAN_PATH'] = os.pathsep.join(lean_path)
    record = {'schema': 1, 'status': 'RUNNING', 'project_root': str(root), 'run_dir': str(run),
        'inputs': inputs, 'cleanup': cleanup, 'environment_before': before, 'lean_path': lean_path,
        'initial_objects': [], 'results': []}
    receipt = run / 'RECEIPT.json'; save(receipt, record)
    try:
        objects = {}
        for name, kind, source, accepted in expected_jobs():
            stem = name.replace('.', '_'); args = argv_for(before['lean'], name, kind, source)
            if kind == 'module':
                (run / 'projectownlib' / name.replace('.', '/')).parent.mkdir(parents=True, exist_ok=True)
            elapsed = time.monotonic() - started
            need(elapsed < BUDGET, '90-minute allowance exceeded')
            launched = time.monotonic(); timed_out = False
            with (run / 'logs' / (stem + '.log')).open('wb') as log_file:
                process = subprocess.Popen(args, cwd=run, env=env, stdin=subprocess.DEVNULL,
                    stdout=log_file, stderr=subprocess.STDOUT, start_new_session=True)
                try:
                    code = process.wait(timeout=BUDGET - elapsed)
                except subprocess.TimeoutExpired:
                    timed_out = True
                    os.killpg(process.pid, signal.SIGKILL)
                    code = process.wait()
            log = read(run, 'logs/' + stem + '.log'); usage = read(run, 'logs/' + stem + '.time')
            row = {'name': name, 'kind': kind, 'source': source, 'source_sha256': inputs[source],
                'argv': args, 'cwd': '.', 'expected_accept': accepted, 'returncode': code,
                'timed_out': timed_out, 'seconds': time.monotonic() - launched,
                'log_sha256': sha(log), 'resource_sha256': sha(usage)}
            current = inventory(run / 'projectownlib')
            need(all(current.get(n) == h for n, h in objects.items()), 'earlier compiled object changed')
            added = {n: h for n, h in current.items() if n not in objects}
            if kind == 'module':
                obj = name.replace('.', '/') + '.olean'
                need(obj in added and set(added) <= {obj, obj + '.private', obj + '.server',
                    name.replace('.', '/') + '.ilean'}, 'module did not produce exact fresh artifacts')
                row['artifacts'] = {n: {'sha256': h, 'bytes': len(read(run / 'projectownlib', n))}
                                    for n, h in added.items()}
            else:
                need(not added, 'probe unexpectedly wrote own objects')
            objects = current
            record['results'].append(row); save(receipt, record)
            need(not timed_out, 'Lean invocation timed out')
            check_usage(usage.decode(), code)
            check_outcome(name, accepted, code, log.decode())
            print('CHECKED', name, flush=True)
        record['environment_after'] = environment(root)
        need(check_inputs(root) == inputs, 'inputs changed during build')
        record.update(status='PASS', total_seconds=time.monotonic() - started)
        save(receipt, record)
        check_receipt(receipt, root)
    except BaseException:
        record.update(status='FAIL', total_seconds=time.monotonic() - started)
        save(receipt, record)
        raise
    print('PASS: 8 fresh modules; 22 exact-type examples; 11 axiom targets; 1 positive and 4 negative controls.')
    print('RECEIPT', receipt)
    return receipt


if __name__ == '__main__':
    try:
        need(len(sys.argv) == 1, 'usage: python audit/verify.py')
        verify()
    except (OSError, ValueError, KeyError, TypeError, UnicodeError, subprocess.SubprocessError) as error:
        raise SystemExit('FAIL: malformed evidence or execution error: ' + type(error).__name__)
