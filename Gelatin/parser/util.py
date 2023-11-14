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

from Gelatin import INDENT_WIDTH

whitespace_re = re.compile(r" *")


def _format(buffer, end, msg):
    """TODO: Create docstring."""
    line_start = buffer.rfind("\n", 0, end) + 1
    line_end = buffer.find("\n", line_start)
    line_no = buffer.count("\n", 0, end) + 1
    line = buffer[line_start:line_end]
    offset = end - line_start
    mark = f" {' ' * offset}^"
    return f"{msg} in line {line_no}:\n{repr(line)}\n{mark}"


def say(buffer, end, msg):
    """TODO: Create docstring."""
    print(_format(buffer, end, msg))


def error(buffer, end, msg="Syntax error"):
    """TODO: Create docstring."""
    msg = _format(buffer, end, msg)
    raise Exception(msg)


def eat_indent(buffer, start, end, expected_indent=None):
    """TODO: Create docstring."""
    result = whitespace_re.match(buffer, start, end)
    if result is None:
        # pyre2 returns None if the start parameter to match() is larger
        # than the length of the buffer.
        return start
    whitespace = result.group(0)
    whitespace_len = len(whitespace)
    indent = whitespace_len / INDENT_WIDTH
    if whitespace_len % INDENT_WIDTH != 0:
        msg = f"indent must be a multiple of {INDENT_WIDTH}"
        error(buffer, start, msg)
    if expected_indent is None or expected_indent == indent:
        return start + whitespace_len
    return start


def count_indent(buffer, start):
    """TODO: Create docstring."""
    indent = start - buffer.rfind("\n", 0, start) - 1
    if indent % INDENT_WIDTH != 0:
        msg = f"indent must be a multiple of {INDENT_WIDTH}, is {indent}"
        error(buffer, start, msg)
    if indent / INDENT_WIDTH > 2:
        msg = "maximum indent (2 levels) exceeded."
        error(buffer, start, msg)
    return indent / INDENT_WIDTH
