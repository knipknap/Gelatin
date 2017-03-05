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
import sys, os
from setuptools import setup, find_packages
from Gelatin.version import __version__
pkg = 'Gelatin'
descr = '''
Gelatin is a parser generator for converting text to a structured
format such as XML, JSON or YAML.
'''.strip()

# Run the setup.
setup(name             = pkg,
      version          = __version__,
      description      = 'Transform text files to XML, JSON, or YAML',
      long_description = descr,
      author           = 'Samuel Abels',
      author_email     = 'knipknap@gmail.com',
      license          = 'GPLv2',
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
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: XML'
      ])
