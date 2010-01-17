#!/usr/bin/env python
# Generates the *public* API documentation.
# Remember to hide your private parts, people!
import os, re, sys

project  = 'Gelatin'
base_dir = os.path.join('..', 'src')
doc_dir  = 'api'

# Create the documentation directory.
if not os.path.exists(doc_dir):
    os.makedirs(doc_dir)

# Generate the API documentation.
cmd = 'epydoc ' + ' '.join(['--name', project,
                            r'--exclude ^Gelatin\.parser\.Newline$',
                            r'--exclude ^Gelatin\.parser\.Indent$',
                            r'--exclude ^Gelatin\.parser\.Dedent$',
                            r'--exclude ^Gelatin\.parser\.Token$',
                            r'--exclude ^Gelatin\.parser\.util$',
                            r'--exclude ^Gelatin\.compiler\.Function$',
                            r'--exclude ^Gelatin\.compiler\.Grammar$',
                            r'--exclude ^Gelatin\.compiler\.Match',
                            r'--exclude ^Gelatin\.compiler\.Number$',
                            r'--exclude ^Gelatin\.compiler\.Regex$',
                            r'--exclude ^Gelatin\.compiler\.String$',
                            r'--exclude ^Gelatin\.compiler\.Token$',
                            '--html',
                            '--no-private',
                            '--introspect-only',
                            '--no-source',
                            '--no-frames',
                            '--inheritance=included',
                            '-v',
                            '-o %s' % doc_dir,
                            os.path.join(base_dir, project)])
print cmd
os.system(cmd)
