#!/usr/bin/env python3
"""Create the analysis environment (.venv) and install requirements.txt.

Run it directly, or let run.py call it: run.py bootstraps through this
script the first time it finds the environment missing.

  python3 setup_env.py            build the env if it is not ready
  python3 setup_env.py --check    exit 0 if ready, 1 if not (builds nothing)
  python3 setup_env.py --force    rebuild from scratch

Tries uv, then the standard venv module, then venv without pip plus a
get-pip bootstrap — whichever the machine supports. Prints what it used.
"""
import argparse, os, shutil, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REQS = os.path.join(HERE, 'requirements.txt')
PKGS = ('numpy', 'pandas', 'sklearn')


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
    code = 'import ' + ', '.join(PKGS)
    return subprocess.run([py, '-c', code], capture_output=True).returncode == 0


def run(cmd, **kw):
    print('  $ ' + ' '.join(cmd), flush=True)
    return subprocess.run(cmd, **kw).returncode == 0


def build_with_uv():
    uv = shutil.which('uv')
    if not uv:
        return False
    print('· using uv')
    return run([uv, 'venv', ENV]) and run([uv, 'pip', 'install', '--python', env_python() or '', '-r', REQS])


def build_with_venv():
    print('· using the venv module')
    if not run([sys.executable, '-m', 'venv', ENV]):
        return False
    py = env_python()
    return bool(py) and run([py, '-m', 'pip', 'install', '--quiet', '--upgrade', 'pip']) \
        and run([py, '-m', 'pip', 'install', '--quiet', '-r', REQS])


def build_without_ensurepip():
    """Debian/Ubuntu without python3-venv: no ensurepip, so fetch get-pip."""
    print('· using venv --without-pip + get-pip.py (no ensurepip on this machine)')
    if not run([sys.executable, '-m', 'venv', '--without-pip', ENV]):
        return False
    py = env_python()
    if not py:
        return False
    getpip = os.path.join(ENV, 'get-pip.py')
    try:
        print('  downloading get-pip.py', flush=True)
        urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', getpip)
    except Exception as e:
        print('  could not download get-pip.py: %s' % e)
        return False
    ok = run([py, getpip, '--quiet']) and run([py, '-m', 'pip', 'install', '--quiet', '-r', REQS])
    if os.path.exists(getpip):
        os.remove(getpip)
    return ok


def build():
    for attempt in (build_with_uv, build_with_venv, build_without_ensurepip):
        if os.path.isdir(ENV) and not ready():
            shutil.rmtree(ENV, ignore_errors=True)
        try:
            if attempt() and ready():
                return True
        except Exception as e:
            print('  failed: %s' % e)
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--check', action='store_true', help='report readiness only')
    ap.add_argument('--force', action='store_true', help='rebuild from scratch')
    a = ap.parse_args()

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
    if build():
        print('environment ready: %s' % ENV)
        print('run the chain with:  %s %s --mode honest' % (env_python(), os.path.join(HERE, 'run.py')))
        return 0

    print('\ncould not build the environment automatically.')
    print('The chain still runs on the frozen results in cache.json, so the')
    print('activity is not blocked. To fix the environment, install one of:')
    print('  - uv          curl -LsSf https://astral.sh/uv/install.sh | sh')
    print('  - python venv sudo apt install python3-venv   (Debian/Ubuntu)')
    print('then run this script again.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
