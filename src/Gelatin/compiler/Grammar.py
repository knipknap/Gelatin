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

    def parse(self, context):
        if self.inherit:
            inherited = context.grammars[self.inherit].statements
        else:
            inherited = []

        matched = True
        while matched:
            matched = False
            context._msg(self.name)
            for statement in inherited + self.statements:
                if statement.parse(context) != 0:
                    matched = True
                    print "MATCH", statement.__class__.__name__
                    break
        return 0

    def dump(self, indent = 0):
        res = INDENT * indent + 'grammar ' + self.name
        if self.inherit:
            res += '(' + self.inherit + ')'
        res += ':\n'
        for statement in self.statements:
            res += statement.dump(indent + 1)
        return res
