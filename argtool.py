import glob
import os
import subprocess
import sys

# Remove the script name from the arguments; we won't be using it.
sys.argv.pop(0)

# Update Python path so we can find all modules properly.
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

# Collect all source files.
srcs = glob.glob('src/**/*.py', recursive=True)


def cmd_exec(cmd: list):
    """
    Execute a command with the same environment as the current environment.
    """
    return subprocess.run(cmd, env={
        **os.environ,
        'PYTHONPATH': ';'.join(sys.path)
    })


def recipe_deps():
    print("Making sure all dependencies are satisfied...")
    cmd_exec(['pip', 'install', '-r', 'requirements.txt'])


def recipe_uml():
    print("Generating UML class diagram...")
    cmd_exec(['pyreverse', *srcs, '--output', 'puml'])


def recipe_style():
    print("Executing style checks...")
    cmd_exec(['pycodestyle', '--statistics', *srcs])


def recipe_lint():
    print("Performing static analysis...")
    cmd_exec(
        ['pylint', '--errors-only', '--generated-members', 'pygame.*', *srcs])


def recipe_docs():
    print("Generating API documentation...")
    cmd_exec(['pdoc', '-o', 'docs/api', *srcs])


def recipe_coverase():
    print("Removing existing coverage data...")
    cmd_exec(['coverage', 'erase'])


def recipe_covhtml():
    print("Generating coverage report...")
    cmd_exec(['coverage', 'html', '--directory', 'docs/coverage'])


def recipe_coverage():
    print("Executing code with coverage...")
    cmd_exec(['coverage', 'run', '--append', 'src/arg.py'])
    recipe_covhtml()

def recipe_test():
    print("Executing automated tests...")
    cmd_exec(['pytest', '--cov', 'tests'])
    recipe_covhtml()

if not len(sys.argv):
    exclude = ['recipe_test', 'recipe_coverage', 'recipe_coverase']
    sys.argv = list(
        filter(
            lambda x: x.startswith('recipe_') and x not in exclude, globals()))
else:
    sys.argv = list(map(lambda x: f"recipe_{x}", sys.argv))

for recipe in sys.argv:
    if recipe in globals():
        globals()[recipe]()
    else:
        print(f"Warning: Unknown recipe: {recipe}")
