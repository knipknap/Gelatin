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
from Gelatin import INDENT
from Token   import Token

_string_re = re.compile(r'(\\?)\$(\d*)')

class String(Token):
    def __init__(self, context, data):
        self.context = context
        self.data    = data

    def _expand_string(self, match):
        field    = match.group(0)
        escape   = match.group(1)
        fieldnum = match.group(2)

        # Check the variable name syntax.
        if escape:
            return '$' + fieldnum
        elif fieldnum == '':
            return '$'

        # Check the variable value.
        cmatch = self.context.re_stack[-1]
        try:
            value = cmatch.group(int(fieldnum) + 1)
        except IndexError, e:
            raise Exception('invalid field number %s in %s' % (fieldnum, self.data))
        return str(value)

    def value(self):
        return _string_re.sub(self._expand_string, self.data)

    def re_value(self):
        return self.data #FIXME: escape the string

    def dump(self, indent = 0):
        return INDENT * indent + '\'' + self.data + '\''
