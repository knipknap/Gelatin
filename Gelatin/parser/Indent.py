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
from util  import eat_indent, count_indent, error
from Token import Token

class Indent(Token):
    def __call__(self, buffer, start, end):
        after_indent = eat_indent(buffer, start, end)
        new_indent   = count_indent(buffer, after_indent)
        if new_indent != self.processor.indent + 1:
            error(buffer, start, 'Indentation error')
        self.processor.indent = new_indent
        return after_indent
