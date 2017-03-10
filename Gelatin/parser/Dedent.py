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
from simpleparse.objectgenerator import Prebuilt
from simpleparse.stt.TextTools   import Call, Skip
from util                        import eat_indent, count_indent
from Token                       import Token

class Dedent(Token):
    def __call__(self, buffer, start, end):
        if start > end:
            return start + 1
        after_indent = eat_indent(buffer, start, end)
        self.processor.indent = count_indent(buffer, after_indent)
        return after_indent + 1  # +1/-1 hack

    def table(self):
        table = (None, Call, self), (None, Skip, -1)  # +1/-1 hack
        return Prebuilt(value = table, report = False)
