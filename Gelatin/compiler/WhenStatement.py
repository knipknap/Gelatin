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


class WhenStatement(Token):
    """TODO: Create docstring."""

    def __init__(self):
        """TODO: Create docstring."""
        self.matchlist = None
        self.statements = None
        self.on_leave = []

    def _enter(self, context, debug):
        """TODO: Create docstring."""
        context.stack.append(self)
        if debug > 2:
            print(f"ENTER{self.__class__.__name__}{self.matchlist.dump()}", end="")

    def _leave(self, context, debug):
        """TODO: Create docstring."""
        for func, args in self.on_leave:
            func(*args)
        self.on_leave = []
        context.stack.pop()
        if debug > 2:
            print(f"LEAVE{self.__class__.__name__}{self.matchlist.dump()}", end="")

    def _handle_match(self, context, match, debug):
        """TODO: Create docstring."""
        if not match:
            return 0
        self._enter(context, debug)
        context._match_before_notify(match)
        for statement in self.statements:
            result = statement.parse(context, debug)
            if result == 1:
                break
            elif result < 0:
                context._match_after_notify(match)
                self._leave(context, debug)
                return result
        context._match_after_notify(match)
        self._leave(context, debug)
        return 1

    def parse(self, context, debug=0):
        """TODO: Create docstring."""
        match = self.matchlist.when(context)
        return self._handle_match(context, match, debug)

    def dump(self, indent=0):
        """TODO: Create docstring."""
        res = f"{INDENT * indent}match:\n"
        res += self.matchlist.dump(indent + 1)
        for statement in self.statements:
            res += f"{statement.dump(indent + 2)}\n"
        return res
