#!/usr/bin/env python3
"""Create the analysis environment (.venv) and install requirements.txt.

Run it directly, or let run.py call it: run.py bootstraps through this
script the first time it finds the environment missing.

  python3 setup_env.py            build the env if it is not ready
  python3 setup_env.py --check    exit 0 if ready, 1 if not (builds nothing)
  python3 setup_env.py --force    rebuild from scratch
  python3 setup_env.py --verbose  show the output of every command

Tries uv, then the standard venv module, then venv without pip plus a
get-pip bootstrap — whichever the machine supports. Each attempt is quiet;
if they all fail, the captured output is printed so you can see why.
"""
import argparse, os, shutil, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REQS = os.path.join(HERE, 'requirements.txt')
PKGS = ('numpy', 'pandas', 'sklearn')
LOG = []
VERBOSE = False


def project_root():
    """Nearest enclosing project dir, so the env is shared, not per-skill."""
    d = HERE
    for _ in range(4):
        d = os.path.dirname(d)
        if not d or d == os.path.dirname(d):
            break
        if os.path.isdir(os.path.join(d, '.git')) or os.path.exists(os.path.join(d, 'index.html')):
            return d
    return HERE


ENV = os.path.join(project_root(), '.venv')


def env_python(env=ENV):
    p = os.path.join(env, 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join(env, 'bin', 'python')
    return p if os.path.exists(p) else None


def ready(env=ENV):
    """True when the env exists and can import everything the chain needs."""
    py = env_python(env)
    if not py:
        return False
    return subprocess.run([py, '-c', 'import ' + ', '.join(PKGS)],
                          capture_output=True).returncode == 0


def run(cmd):
    """Run quietly, keeping the output in case every attempt fails."""
    if VERBOSE:
        print('  $ ' + ' '.join(cmd), flush=True)
        return subprocess.run(cmd).returncode == 0
    p = subprocess.run(cmd, capture_output=True, text=True)
    LOG.append('$ %s\n%s%s' % (' '.join(cmd), p.stdout or '', p.stderr or ''))
    return p.returncode == 0


def build_with_uv():
    uv = shutil.which('uv')
    if not uv:
        return False
    return run([uv, 'venv', ENV]) and run([uv, 'pip', 'install', '--python', env_python() or '', '-r', REQS])


def build_with_venv():
    if not run([sys.executable, '-m', 'venv', ENV]):
        return False
    py = env_python()
    return bool(py) and run([py, '-m', 'pip', 'install', '--quiet', '--upgrade', 'pip']) \
        and run([py, '-m', 'pip', 'install', '--quiet', '-r', REQS])


def build_without_ensurepip():
    """Debian/Ubuntu without python3-venv: no ensurepip, so fetch get-pip."""
    if not run([sys.executable, '-m', 'venv', '--without-pip', ENV]):
        return False
    py = env_python()
    if not py:
        return False
    getpip = os.path.join(ENV, 'get-pip.py')
    try:
        urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', getpip)
    except Exception as e:
        LOG.append('get-pip.py download failed: %s' % e)
        return False
    ok = run([py, getpip, '--quiet']) and run([py, '-m', 'pip', 'install', '--quiet', '-r', REQS])
    if os.path.exists(getpip):
        os.remove(getpip)
    return ok


ATTEMPTS = ((build_with_uv, 'uv'),
            (build_with_venv, 'venv module'),
            (build_without_ensurepip, 'venv without pip, plus get-pip'))


def build():
    for i, (attempt, label) in enumerate(ATTEMPTS):
        if os.path.isdir(ENV) and not ready():
            shutil.rmtree(ENV, ignore_errors=True)
        print('· %s' % label, end='', flush=True)
        try:
            ok = attempt() and ready()
        except Exception as e:
            LOG.append('%s raised %s' % (attempt.__name__, e))
            ok = False
        if ok:
            print(' — done')
            return True
        print(' — not available here, trying another way'
              if i < len(ATTEMPTS) - 1 else ' — failed')
    return False


def main():
    global VERBOSE
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--check', action='store_true', help='report readiness only')
    ap.add_argument('--force', action='store_true', help='rebuild from scratch')
    ap.add_argument('--verbose', action='store_true', help='show every command and its output')
    a = ap.parse_args()
    VERBOSE = a.verbose

    if a.check:
        ok = ready()
        print('environment %s: %s' % ('READY' if ok else 'not built', ENV))
        return 0 if ok else 1

    if a.force:
        shutil.rmtree(ENV, ignore_errors=True)
    elif ready():
        print('environment already ready: %s' % ENV)
        return 0

    print('building the analysis environment in %s' % ENV)
    print('installing numpy, pandas and scikit-learn — this takes a moment.')
    if build():
        print('environment ready: %s' % ENV)
        try:
            cmd = os.path.relpath(os.path.join(HERE, 'run.py'))
        except ValueError:
            cmd = os.path.join(HERE, 'run.py')
        print('run the chain with:  python3 %s --mode honest' % cmd)
        return 0

    print('\ncould not build the environment automatically.')
    print('The chain still runs on the frozen results in cache.json, so the')
    print('activity is not blocked. To fix the environment, install one of:')
    print('  - uv          curl -LsSf https://astral.sh/uv/install.sh | sh')
    print('  - python venv sudo apt install python3-venv   (Debian/Ubuntu)')
    print('then run this script again.')
    if LOG and not VERBOSE:
        print('\n--- what was tried ---')
        for entry in LOG:
            print(entry.strip()[:1200])
    return 1


if __name__ == '__main__':
    sys.exit(main())
