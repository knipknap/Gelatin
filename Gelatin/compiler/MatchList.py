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
from .Token import Token


class MatchList(Token):
    """TODO: Create docstring."""

    def __init__(self):
        """TODO: Create docstring."""
        self.field_lists = []

    def when(self, context):
        """TODO: Create docstring."""
        for field_list in self.field_lists:
            match = field_list.when(context)
            if match:
                return match
        return None

    def match(self, context):
        """TODO: Create docstring."""
        for field_list in self.field_lists:
            match = field_list.match(context)
            if match:
                return match
        return None

    def dump(self, indent=0):
        """TODO: Create docstring."""
        res = ""
        for field_list in self.field_lists:
            res += f"{field_list.dump(indent)}\n"
        return f"{res.rstrip()}:\n"
