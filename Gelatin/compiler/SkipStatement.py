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
from __future__ import print_function
import re
from Gelatin import INDENT, SEARCH_WINDOW
from .Token import Token


class SkipStatement(Token):

    def __init__(self):
        self.match = None
        self.regex = None

    def parse(self, context, debug=0):
        if not self.regex:
            self.regex = re.compile(self.match.re_value())

        end = context.start+SEARCH_WINDOW
        match = self.regex.match(context.input[context.start:end])
        if match is not None:
            start, end = match.span(0)
            context.start += end - start
            return 1
        return 0

    def dump(self, indent=0):
        res = INDENT * indent + 'match:\n'
        return res + self.matchlist.dump(indent + 1)
