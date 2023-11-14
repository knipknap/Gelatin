"""TODO: Create docstring."""
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

from Gelatin import INDENT, SEARCH_WINDOW

from .Token import Token


class MatchFieldList(Token):
    """TODO: Create docstring."""

    def __init__(self, modifiers=None):
        """TODO: Create docstring."""
        self.expressions = []
        self.regex = None
        self.modifiers = modifiers

    def when(self, context):
        """TODO: Create docstring."""
        if not self.regex:
            regex = ")(".join(e.re_value() for e in self.expressions)
            self.regex = re.compile(f"({regex})", self.modifiers)

        end = context.start + SEARCH_WINDOW
        return self.regex.match(context.input[context.start : end])

    def match(self, context):
        """TODO: Create docstring."""
        match = self.when(context)
        if not match:
            return None
        start, end = match.span(0)
        context.start += end - start
        return match

    def dump(self, indent=0):
        """TODO: Create docstring."""
        res = INDENT * indent
        for expr in self.expressions:
            res += f"{expr.dump()} "
        return res.rstrip()
