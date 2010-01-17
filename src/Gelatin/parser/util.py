# Copyright (C) 2010 Samuel Abels.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
import re
from Gelatin import INDENT_WIDTH

whitespace_re = re.compile(' *')

def _format(buffer, end, msg):
    line_start = buffer.rfind('\n', 0, end) + 1
    line_end   = buffer.find('\n', line_start)
    line_no    = buffer.count('\n', 0, end) + 1
    line       = buffer[line_start:line_end]
    offset     = end - line_start
    mark       = ' ' + ' ' * offset + '^'
    return '%s in line %d:\n%s\n%s' % (msg, line_no, repr(line), mark)

def say(buffer, end, msg):
    print _format(buffer, end, msg)

def error(buffer, end, msg = 'Syntax error'):
    msg = _format(buffer, end, msg)
    raise Exception(msg)

def eat_indent(buffer, start, end, expected_indent = None):
    result = whitespace_re.match(buffer, start, end)
    if result is None:
        raise Exception('BUG: failed to parse indent')
    whitespace     = result.group(0)
    whitespace_len = len(whitespace)
    indent         = whitespace_len / INDENT_WIDTH
    if whitespace_len % INDENT_WIDTH != 0:
        msg = 'indent must be a multiple of %d' % INDENT_WIDTH
        error(buffer, start, msg)
    if expected_indent is None or expected_indent == indent:
        return start + whitespace_len
    return start

def count_indent(buffer, start):
    indent = start - buffer.rfind('\n', 0, start) - 1
    if indent % INDENT_WIDTH != 0:
        msg = 'indent must be a multiple of %d' % INDENT_WIDTH
        error(buffer, start, msg)
    if indent / INDENT_WIDTH > 2:
        msg = 'maximum indent (2 levels) exceeded.'
        error(buffer, start, msg)
    return indent / INDENT_WIDTH
