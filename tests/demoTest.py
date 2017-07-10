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
from __future__ import unicode_literals, print_function
import sys
import unittest
import re
import os
import codecs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from Gelatin.util import compile, generate

dirname = os.path.dirname(__file__)
demo_dir = os.path.join(os.path.dirname(dirname), 'demo')

def convert(filename, format):
    syntax_file = os.path.join(demo_dir, filename, 'syntax.gel')
    input_file = os.path.join(demo_dir, filename, 'input1.txt')
    syntax = compile(syntax_file)
    return generate(syntax, input_file, format)


class DemoTest(unittest.TestCase):

    def setUp(self):
        self.demos = os.listdir(demo_dir)
        self.maxDiff = None

    def testDemos(self):
        for filename in self.demos:
            for format in ('xml', 'yaml', 'json'):
                output = convert(filename, format)
                # In Python 3.3, json.dumps() would output trailing whitespace
                # in the generated JSON. As a workaround, we remove this here...
                output = output.replace(' \n', '\n')
                output_name = 'output1.' + format
                output_file = os.path.join(demo_dir, filename, output_name)
                #with codecs.open(output_file, 'w', encoding='utf-8') as fp:
                #    fp.write(output)
                with codecs.open(output_file, encoding='utf-8') as fp:
                    expected = fp.read()
                    # print(output_file, repr(output))
                    # print(output_file, repr(expected))
                    self.assertEqual(output, expected)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(DemoTest)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
