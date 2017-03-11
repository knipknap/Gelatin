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
import os
import codecs
from simpleparse import parser
from .Newline     import Newline
from .Indent      import Indent
from .Dedent      import Dedent
from .util        import error

_ebnf_file = os.path.join(os.path.dirname(__file__), 'syntax.ebnf')
with open(_ebnf_file) as _thefile:
    _ebnf = _thefile.read()

class Parser(parser.Parser):
    def __init__(self):
        self.indent = 0
        offside     = (
            ("NEWLINE", Newline(self).table()),
            ("INDENT",  Indent(self).table()),
            ("DEDENT",  Dedent(self).table()),
        )
        parser.Parser.__init__(self, _ebnf, 'root', prebuilts = offside)

    def parse_string(self, input, compiler):
        compiler.reset()
        start, _, end = parser.Parser.parse(self, input, processor = compiler)
        if end < len(input):
            error(input, end)
        if 'input' not in compiler.context.grammars:
            error(input, end, 'Required grammar "input" not found.')
        return compiler.context

    def parse(self, filename, compiler):
        with codecs.open(filename, 'r') as input_file:
            string = input_file.read()
            return self.parse_string(string, compiler)
