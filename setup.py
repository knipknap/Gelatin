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
pkg = 'Gelatin'

# Import the file that contains the version number.
gelatin_dir = os.path.join(os.path.dirname(__file__), 'src', pkg)
sys.path.insert(0, gelatin_dir)
from version import __version__

# Import the project description from the README.
readme = open('README').read()
start  = readme.index('\n\n')
end    = readme.index('\n\n=')
descr  = readme[start:end].strip()

# Run the setup.
setup(name             = pkg,
      version          = __version__,
      description      = 'Transform text files to XML, JSON, or YAML',
      long_description = descr,
      author           = 'Samuel Abels',
      author_email     = 'knipknap@gmail.com',
      license          = 'GPLv2',
      package_dir      = {pkg: os.path.join('src', pkg)},
      package_data     = {pkg: [os.path.join('parser', 'syntax.ebnf')]},
      packages         = find_packages('src'),
      scripts          = ['gel'],
      install_requires = [],
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
      url              = 'http://github.com/knipknap/Gelatin',
      classifiers      = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: XML'
      ])
