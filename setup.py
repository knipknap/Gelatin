# Copyright (c) 2010-2017 Samuel Abels
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys, os
from setuptools import setup, find_packages
from Gelatin.version import __version__
pkg = 'Gelatin'
descr = '''
Gelatin converts text to a structured format, such as XML, JSON or YAML.
'''.strip()

# Run the setup.
setup(name             = pkg,
      version          = __version__,
      description      = 'Transform text files to XML, JSON, or YAML',
      long_description = descr,
      author           = 'Samuel Abels',
      author_email     = 'knipknap@gmail.com',
      license          = 'MIT',
      package_dir      = {pkg: pkg},
      package_data     = {pkg: [os.path.join('parser', 'syntax.ebnf')]},
      packages         = find_packages('.'),
      scripts          = ['gel'],
      install_requires = ['lxml',
                          'pyyaml',
                          'SimpleParse'],
      keywords         = ' '.join(['gelatin',
                                   'gel',
                                   'parser',
                                   'lexer',
                                   'xml',
                                   'json',
                                   'yaml',
                                   'generator',
                                   'syntax',
                                   'text',
                                   'transform']),
      url              = 'https://github.com/knipknap/Gelatin',
      classifiers      = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: XML'
      ])
