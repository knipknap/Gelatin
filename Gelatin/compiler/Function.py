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

class Function(Token):
    def __init__(self):
        self.name = None
        self.args = []

    def parse(self, context):
        # Function names that have NO dot in them are references to another
        # grammar.
        if '.' not in self.name:
            start   = context.start
            grammar = context.grammars.get(self.name)
            if not grammar:
                raise Exception('call to undefined grammar ' + self.name)
            grammar.parse(context)
            if context.start != start:
                return 1
            return 0

        # Other functions are utilities.
        func = context.functions.get(self.name)
        if not func:
            raise Exception('unknown function ' + self.name)
        return func(context, *[a.value() for a in self.args])

    def dump(self, indent = 0):
        args = ', '.join(a.dump() for a in self.args)
        return INDENT * indent + self.name + '(' + args + ')'
