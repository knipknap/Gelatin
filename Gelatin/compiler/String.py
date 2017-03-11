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
import re
from Gelatin import INDENT
from .Token import Token

_string_re = re.compile(r'(\\?)\$(\d*)')

class String(Token):
    def __init__(self, context, data):
        self.context = context
        self.data    = data

    def _expand_string(self, match):
        field    = match.group(0)
        escape   = match.group(1)
        fieldnum = match.group(2)

        # Check the variable name syntax.
        if escape:
            return '$' + fieldnum
        elif fieldnum == '':
            return '$'

        # Check the variable value.
        cmatch = self.context.re_stack[-1]
        try:
            return cmatch.group(int(fieldnum) + 1)
        except IndexError as e:
            raise Exception('invalid field number %s in %s' % (fieldnum, self.data))

    def value(self):
        return _string_re.sub(self._expand_string, self.data)

    def re_value(self):
        return re.escape(self.data)

    def dump(self, indent = 0):
        return INDENT * indent + '\'' + self.data + '\''
