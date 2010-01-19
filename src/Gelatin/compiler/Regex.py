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

class Regex(Token):
    data   = None
    re_obj = None

    def re_value(self):
        return self.data

    def value(self):
        if not self.re_obj:
            self.re_obj = re.compile(self.data)
        return self.re_obj

    def dump(self, indent = 0):
        return INDENT * indent + '/' + self.data + '/'
