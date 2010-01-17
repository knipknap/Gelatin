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
from util                        import eat_indent
from Token                       import Token

class Newline(Token):
    def __call__(self, buffer, start, end):
        # Skip empty lines.
        thestart = start
        try:
            if buffer[thestart] != '\n':
                return thestart
            while buffer[thestart] == '\n':
                thestart += 1
        except IndexError:
            return thestart + 2 # +1/-1 hack #EOF

        # If the indent of the non-empty line matches, we are done.
        return eat_indent(buffer, thestart, end, self.processor.indent) + 1 # +1/-1 hack

    def table(self):
        table = (None, Call, self), (None, Skip, -1) # +1/-1 hack
        return Prebuilt(value = table, report = False)
