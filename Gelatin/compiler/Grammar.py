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
from __future__ import print_function

from Gelatin import INDENT

from .Token import Token


class Grammar(Token):
    """TODO: Create docstring."""

    def __init__(self):
        """TODO: Create docstring."""
        self.name = None
        self.inherit = None
        self.statements = None
        self.on_leave = []

    def get_statements(self, context):
        """TODO: Create docstring."""
        if not self.inherit:
            return self.statements
        inherited = context.grammars[self.inherit].get_statements(context)
        return inherited + self.statements

    def _enter(self, context, debug):
        """TODO: Create docstring."""
        context.stack.append(self)
        if debug > 1:
            print(f"ENTER{self.__class__.__name__}{self.name}")

    def _leave(self, context, debug):
        """TODO: Create docstring."""
        for func, args in self.on_leave:
            func(*args)
        self.on_leave = []
        context.stack.pop()
        if debug > 1:
            print(f"LEAVE{self.__class__.__name__}{self.name}")

    def parse(self, context, debug=0):
        """TODO: Create docstring."""
        self._enter(context, debug)
        statements = self.get_statements(context)
        matched = True
        while matched:
            if context._eof():
                self._leave(context, debug)
                return
            matched = False
            # context._msg(self.name)
            for statement in statements:
                result = statement.parse(context, debug)
                if result == 1:
                    matched = True
                    break
                elif result < 0:
                    self._leave(context, debug)
                    return result + 1
        context._error(f"no match found, context was {self.name}")

    def dump(self, indent=0):
        """TODO: Create docstring."""
        res = f"{INDENT * indent}grammar{self.name}"
        if self.inherit:
            res += f"({self.inherit})"
        res += ":\n"
        for statement in self.statements:
            res += statement.dump(indent + 1)
        return res
