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
from Gelatin import INDENT
from Token   import Token

class WhenStatement(Token):
    def __init__(self):
        self.matchlist  = None
        self.statements = None
        self.on_leave   = []

    def _enter(self, context):
        context.stack.append(self)

    def _leave(self, context):
        for func, args in self.on_leave:
            func(*args)
        self.on_leave = []
        context.stack.pop()

    def _handle_match(self, context, match):
        if not match:
            return 0
        self._enter(context)
        context._match_before_notify(match)
        for statement in self.statements:
            result = statement.parse(context)
            if result == 1:
                break
            elif result < 0:
                context._match_after_notify(match)
                self._leave(context)
                return result
        context._match_after_notify(match)
        self._leave(context)
        return 1

    def parse(self, context):
        match = self.matchlist.when(context)
        return self._handle_match(context, match)

    def dump(self, indent = 0):
        res  = INDENT * indent + 'match:\n'
        res += self.matchlist.dump(indent + 1)
        for statement in self.statements:
            res += statement.dump(indent + 2) + '\n'
        return res
