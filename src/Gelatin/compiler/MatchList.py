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
from Gelatin import INDENT
from Token   import Token

class MatchList(Token):
    def __init__(self):
        self.field_lists = []

    def match(self, context):
        for field_list in self.field_lists:
            match = field_list.match(context)
            if match:
                return match
        return None

    def dump(self, indent = 0):
        res = ''
        for field_list in self.field_lists:
            res += field_list.dump(indent) + '\n'
        return res.rstrip() + ':\n'
