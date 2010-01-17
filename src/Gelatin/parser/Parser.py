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
import os
from simpleparse import parser
from Newline     import Newline
from Indent      import Indent
from Dedent      import Dedent
from util        import error

_ebnf_file = os.path.join(os.path.dirname(__file__), 'syntax.ebnf')
_ebnf      = open(_ebnf_file).read()

class Parser(parser.Parser):
    def __init__(self):
        self.indent = 0
        offside     = (
            ("NEWLINE", Newline(self).table()),
            ("INDENT",  Indent(self).table()),
            ("DEDENT",  Dedent(self).table()),
        )
        parser.Parser.__init__(self, _ebnf, 'root', prebuilts = offside)

    def parse(self, input, compiler):
        start, _, end = parser.Parser.parse(self, input, processor = compiler)
        if end < len(input):
            error(input, end)
        if not compiler.context.grammars.has_key('input'):
            error(input, end, 'Required grammar "input" not found.')
        return compiler.context
