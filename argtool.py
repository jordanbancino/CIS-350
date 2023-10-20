import glob
import os
import subprocess
import sys

# Update Python path so we can find all modules.
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

# Create the environment map to pass along to subprocesses.
env = {
    **os.environ,
    'PYTHONPATH': ';'.join(sys.path)
}

# Collect all source files.
srcs = glob.glob('src/**/*.py', recursive=True)


def cmd_exec(cmd: list):
    """
    Execute a command with the same environment as the current environment.
    """
    return subprocess.run(cmd, env=env)


print("Making sure all dependencies are satisfied...")
cmd_exec(['pip', 'install', '-r', 'requirements.txt'])

print("Generating UML class diagram...")
cmd_exec(['pyreverse', *srcs, '--output', 'puml'])

print("Executing style checks...")
cmd_exec(['pep8', '--statistics', *srcs])

print("Performing static analysis...")
cmd_exec(['pylint', '--errors-only', '--generated-members', 'pygame.*', *srcs])

print("Generating API documentation...")
cmd_exec(['pdoc', '-o', 'docs/api', *srcs])

print("Done.")
