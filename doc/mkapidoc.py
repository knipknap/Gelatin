#!/usr/bin/env python
# Copyright (C) 2010 Samuel Abels.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""
Generates the *public* API documentation.
Remember to hide your private parts, people!
"""
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
