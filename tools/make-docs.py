import os
import glob
import sys

import pydoc

out = 'docs/api'

sys.path.append('./src/')

for src in glob.glob('src/**/*.py', recursive = True):
	sys.argv = [ 'pydoc', '-w', src ]
	pydoc.cli()

if not os.path.isdir(out):
	os.mkdir(out)

for html in glob.glob('*.html'):
	os.rename(html, f"{out}/{html}")
