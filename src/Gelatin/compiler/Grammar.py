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

    def get_statements(self, context):
        if not self.inherit:
            return self.statements
        inherited = context.grammars[self.inherit].get_statements(context)
        return inherited + self.statements

    def parse(self, context):
        statements = self.get_statements(context)
        matched    = True
        while matched:
            if context._eof():
                return
            matched = False
            #context._msg(self.name)
            for statement in statements:
                result = statement.parse(context)
                if result == 1:
                    matched = True
                    break
                elif result < 0:
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
