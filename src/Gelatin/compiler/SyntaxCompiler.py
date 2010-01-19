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
from simpleparse.dispatchprocessor import DispatchProcessor, getString, singleMap
from Function                      import Function
from Grammar                       import Grammar
from MatchStatement                import MatchStatement
from MatchFieldList                import MatchFieldList
from MatchList                     import MatchList
from Number                        import Number
from Regex                         import Regex
from String                        import String
from Context                       import Context

"""
Indent handling:
    o NEWLINE:
        - If the amount of indent matches the previous line, parse the \n
          and skip all indent.
        - If the amount of indent does NOT match the previous line, parse
          the \n and stay at the beginning of the new line to let INDENT
          or DEDENT figure it out.
    o INDENT: Skips all indent, then looks backward to update the indent
      count. Checks to make sure that the indent was increased.
    o DEDENT: Like INDENT, except it does not check for errors.
"""
class SyntaxCompiler(DispatchProcessor):
    """
    Processor sub-class defining processing functions for the productions.
    """
    def __init__(self):
        self.context = Context()

    def _regex(self, (tag, left, right, sublist), buffer):
        regex      = Regex()
        regex.data = getString(sublist[0], buffer)
        return regex

    def _string(self, (tag, left, right, sublist), buffer):
        string = getString(sublist[0], buffer)
        return String(self.context, string)

    def _varname(self, token, buffer):
        varname = getString(token, buffer)
        return self.context.lexicon[varname]

    def _number(self, token, buffer):
        number = getString(token, buffer)
        return Number(int(number))

    def _expression(self, token, buffer):
        tag = token[0]
        if tag == 'string':
            return self._string(token, buffer)
        elif tag == 'regex':
            return self._regex(token, buffer)
        elif tag == 'varname':
            return self._varname(token, buffer)
        elif tag == 'number':
            return self._number(token, buffer)
        else:
            raise Exception('BUG: invalid token %s' % tag)

    def _match_field_list(self, (tag, left, right, sublist), buffer):
        field_list = MatchFieldList()
        for field in sublist:
            expression = self._expression(field, buffer)
            field_list.expressions.append(expression)
        return field_list

    def _match_list(self, (tag, left, right, sublist), buffer):
        matchlist = MatchList()
        for field_list in sublist:
            field_list = self._match_field_list(field_list, buffer)
            matchlist.field_lists.append(field_list)
        return matchlist

    def _match_stmt(self, (tag, left, right, sublist), buffer):
        matcher            = MatchStatement()
        matcher.matchlist  = self._match_list(sublist[0], buffer)
        matcher.statements = self._suite(sublist[1], buffer)
        return matcher

    def _function(self, (tag, left, right, sublist), buffer):
        function      = Function()
        function.name = getString(sublist[0], buffer)
        if len(sublist) == 1:
            return function
        for arg in sublist[1][3]:
            expression = self._expression(arg, buffer)
            function.args.append(expression)
        return function

    def _inherit(self, (tag, left, right, sublist), buffer):
        return getString(sublist[0], buffer)

    def _suite(self, (tag, left, right, sublist), buffer):
        statements = []
        for token in sublist:
            tag = token[0]
            if tag == 'match_stmt':
                statement = self._match_stmt(token, buffer)
            elif tag == 'function':
                statement = self._function(token, buffer)
            else:
                raise Exception('BUG: invalid token %s' % tag)
            statements.append(statement)
        return statements

    def define_stmt(self, (tag, left, right, sublist), buffer):
        name_tup, value_tup = sublist
        value_tag           = value_tup[0]
        name                = getString(name_tup,   buffer)
        value               = getString(value_tup,  buffer)
        if value_tag == 'regex':
            value = self._regex(value_tup, buffer)
        elif value_tag == 'varname':
            if not self.context.lexicon.has_key(value):
                _error(buffer, value_tup[1], 'no such variable')
            value = self.context.lexicon[value]
        else:
            raise Exception('BUG: invalid token %s' % value_tag)
        self.context.lexicon[name] = value

    def grammar_stmt(self, (tag, left, right, sublist), buffer):
        map                = singleMap(sublist)
        grammar            = Grammar()
        grammar.name       = getString(map['varname'], buffer)
        grammar.statements = self._suite(map['suite'], buffer)
        if map.has_key('inherit'):
            grammar.inherit = self._inherit(map['inherit'], buffer)
        self.context.grammars[grammar.name] = grammar
