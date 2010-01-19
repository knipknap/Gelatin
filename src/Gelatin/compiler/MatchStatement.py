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

class MatchStatement(Token):
    def __init__(self):
        self.matchlist  = None
        self.statements = None
        self.on_leave   = []

    def _enter(self, context):
        context.stack.append(self)

    def _leave(self, context):
        for func, args in self.on_leave:
            func(*args)
        self.on_leave = []
        context.stack.pop()

    def parse(self, context):
        match = self.matchlist.match(context)
        if not match:
            return 0
        self._enter(context)
        context._match_before_notify(match)
        for statement in self.statements:
            result = statement.parse(context)
            if result == 1:
                break
            elif result < 0:
                context._match_after_notify(match)
                self._leave(context)
                return result
        context._match_after_notify(match)
        self._leave(context)
        return 1

    def dump(self, indent = 0):
        res  = INDENT * indent + 'match:\n'
        res += self.matchlist.dump(indent + 1)
        for statement in self.statements:
            res += statement.dump(indent + 2) + '\n'
        return res
