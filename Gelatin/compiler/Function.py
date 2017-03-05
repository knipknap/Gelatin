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

class Function(Token):
    def __init__(self):
        self.name = None
        self.args = []

    def parse(self, context):
        # Function names that have NO dot in them are references to another
        # grammar.
        if '.' not in self.name:
            start   = context.start
            grammar = context.grammars.get(self.name)
            if not grammar:
                raise Exception('call to undefined grammar ' + self.name)
            grammar.parse(context)
            if context.start != start:
                return 1
            return 0

        # Other functions are utilities.
        func = context.functions.get(self.name)
        if not func:
            raise Exception('unknown function ' + self.name)
        return func(context, *[a.value() for a in self.args])

    def dump(self, indent = 0):
        args = ', '.join(a.dump() for a in self.args)
        return INDENT * indent + self.name + '(' + args + ')'
