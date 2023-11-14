"""TODO: Create docstring."""
# Copyright (c) 2010-2017 Samuel Abels
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import re

from simpleparse.dispatchprocessor import DispatchProcessor, getString, singleMap

from .Context import Context
from .Function import Function
from .Grammar import Grammar
from .MatchFieldList import MatchFieldList
from .MatchList import MatchList
from .MatchStatement import MatchStatement
from .Number import Number
from .Regex import Regex
from .SkipStatement import SkipStatement
from .String import String
from .WhenStatement import WhenStatement

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
    """Processor sub-class defining processing functions for the productions."""

    def __init__(self):
        """TODO: Create docstring."""
        self.context = None

    def reset(self):
        """Reset the context."""
        self.context = Context()

    def _regex(self, token, buffer):
        """TODO: Create docstring."""
        tag, left, right, sublist = token
        regex = Regex()
        regex.data = getString(sublist[0], buffer)
        return regex

    def _string(self, token, buffer):
        """TODO: Create docstring."""
        tag, left, right, sublist = token
        string = getString(sublist[0], buffer)
        return String(self.context, string)

    def _varname(self, token, buffer):
        """TODO: Create docstring."""
        varname = getString(token, buffer)
        return self.context.lexicon[varname]

    def _number(self, token, buffer):
        """TODO: Create docstring."""
        number = getString(token, buffer)
        return Number(int(number))

    def _expression(self, token, buffer):
        """TODO: Create docstring."""
        tag = token[0]
        if tag == "string":
            return self._string(token, buffer)
        elif tag == "regex":
            return self._regex(token, buffer)
        elif tag == "varname":
            return self._varname(token, buffer)
        elif tag == "number":
            return self._number(token, buffer)
        else:
            raise Exception(f"BUG: invalid token {tag}")

    def _match_field_list(self, token, buffer, flags):
        """TODO: Create docstring."""
        tag, left, right, sublist = token
        field_list = MatchFieldList(flags)
        for field in sublist:
            expression = self._expression(field, buffer)
            field_list.expressions.append(expression)
        return field_list

    def _match_list(self, token, buffer, flags):
        """TODO: Create docstring."""
        tag, left, right, sublist = token
        matchlist = MatchList()
        for field_list in sublist:
            field_list = self._match_field_list(field_list, buffer, flags)
            matchlist.field_lists.append(field_list)
        return matchlist

    def _match_stmt(self, token, buffer, flags=0):
        """TODO: Create docstring."""
        tag, left, right, sublist = token
        matcher = MatchStatement()
        matcher.matchlist = self._match_list(sublist[0], buffer, flags)
        matcher.statements = self._suite(sublist[1], buffer)
        return matcher

    def _when_stmt(self, token, buffer, flags=0):
        """TODO: Create docstring."""
        tag, left, right, sublist = token
        matcher = WhenStatement()
        matcher.matchlist = self._match_list(sublist[0], buffer, flags)
        matcher.statements = self._suite(sublist[1], buffer)
        return matcher

    def _skip_stmt(self, token, buffer):
        """TODO: Create docstring."""
        tag, left, right, sublist = token
        matcher = SkipStatement()
        matcher.match = self._expression(sublist[0], buffer)
        return matcher

    def _function(self, token, buffer):
        """TODO: Create docstring."""
        tag, left, right, sublist = token
        function = Function()
        function.name = getString(sublist[0], buffer)
        if len(sublist) == 1:
            return function
        for arg in sublist[1][3]:
            expression = self._expression(arg, buffer)
            function.args.append(expression)
        return function

    def _inherit(self, token, buffer):
        """TODO: Create docstring."""
        tag, left, right, sublist = token
        return getString(sublist[0], buffer)

    def _suite(self, token, buffer):
        """TODO: Create docstring."""
        tag, left, right, sublist = token
        statements = []
        for token in sublist:
            tag = token[0]
            if tag == "match_stmt":
                statement = self._match_stmt(token, buffer)
            elif tag == "imatch_stmt":
                statement = self._match_stmt(token, buffer, re.I)
            elif tag == "when_stmt":
                statement = self._when_stmt(token, buffer)
            elif tag == "skip_stmt":
                statement = self._skip_stmt(token, buffer)
            elif tag == "function":
                statement = self._function(token, buffer)
            else:
                raise Exception(f"BUG: invalid token {tag}")
            statements.append(statement)
        return statements

    def define_stmt(self, token, buffer):
        """TODO: Create docstring."""
        tag, left, right, sublist = token
        name_tup, value_tup = sublist
        value_tag = value_tup[0]
        name = getString(name_tup, buffer)
        value = getString(value_tup, buffer)
        if value_tag == "regex":
            value = self._regex(value_tup, buffer)
        elif value_tag == "varname":
            if value not in self.context.lexicon:
                self.context._error(buffer, value_tup[1], "no such variable")
            value = self.context.lexicon[value]
        else:
            raise Exception(f"BUG: invalid token {tag}")
        self.context.lexicon[name] = value

    def grammar_stmt(self, token, buffer):
        """TODO: Create docstring."""
        tag, left, right, sublist = token
        map = singleMap(sublist)
        grammar = Grammar()
        grammar.name = getString(map["varname"], buffer)
        grammar.statements = self._suite(map["suite"], buffer)
        if "inherit" in map:
            grammar.inherit = self._inherit(map["inherit"], buffer)
        self.context.grammars[grammar.name] = grammar
