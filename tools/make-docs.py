import glob
import os
import subprocess
import sys

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))


out = 'docs/api'

srcs = glob.glob('src/**/*.py', recursive=True)
subprocess.run(['pdoc', '-o', out, *srcs],
                   env={**os.environ, 'PYTHONPATH': ';'.join(sys.path)})
