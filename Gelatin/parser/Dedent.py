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
