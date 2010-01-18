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

class Grammar(Token):
    def __init__(self):
        self.name       = None
        self.inherit    = None
        self.statements = None
        self.on_leave   = []

    def get_statements(self, context):
        if not self.inherit:
            return self.statements
        inherited = context.grammars[self.inherit].get_statements(context)
        return inherited + self.statements

    def _enter(self, context):
        context.stack.append(self)
        #print "ENTER", self.__class__.__name__

    def _leave(self, context):
        for func, args in self.on_leave:
            func(*args)
        self.on_leave = []
        context.stack.pop()
        #print "LEAVE", self.__class__.__name__

    def parse(self, context):
        self._enter(context)
        statements = self.get_statements(context)
        matched    = True
        while matched:
            if context._eof():
                self._leave(context)
                return
            matched = False
            #context._msg(self.name)
            for statement in statements:
                result = statement.parse(context)
                if result == 1:
                    matched = True
                    break
                elif result < 0:
                    self._leave(context)
                    return result + 1
        context._error('no match found, context was ' + self.name)

    def dump(self, indent = 0):
        res = INDENT * indent + 'grammar ' + self.name
        if self.inherit:
            res += '(' + self.inherit + ')'
        res += ':\n'
        for statement in self.statements:
            res += statement.dump(indent + 1)
        return res
