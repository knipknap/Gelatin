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

def t2x_skip(context):
    return 0

def t2x_fail(context, message = 'No matching statement found'):
    context._error(message)

def t2x_return(context, levels = 1):
    #print "t2x.return():", -levels
    return -levels

def out_add(context, path, data = None):
    #print "out.add():", path, data
    context.builder.add(path, data)
    return 0

def out_enter(context, path):
    #print "out.enter():", path
    context.builder.enter(path)
    context.stack[-1].on_leave.append((context.builder.leave, ()))
    return 0

class Context(object):
    def __init__(self):
        self.functions = {'t2x.fail':   t2x_fail,
                          't2x.return': t2x_return,
                          't2x.skip':   t2x_skip,
                          'out.add':    out_add,
                          'out.enter':  out_enter}
        self.lexicon  = {}
        self.grammars = {}
        self.input    = None
        self.builder  = None
        self.end      = 0
        self._init()

    def _init(self):
        self.start    = 0
        self.re_stack = []
        self.stack    = []

    def _get_lineno(self):
        return self.input.count('\n', 0, self.start) + 1

    def _get_line(self, number = None):
        if number is None:
            number = self._get_lineno()
        return self.input.split('\n')[number - 1]

    def _get_line_position_from_char(self, char):
        line_start = char
        while line_start != 0:
            if self.input[line_start - 1] == '\n':
                break
            line_start -= 1
        line_end = self.input.find('\n', char)
        return line_start, line_end

    def _format(self, error):
        start, end  = self._get_line_position_from_char(self.start)
        line_number = self._get_lineno()
        line        = self._get_line()
        offset      = self.start - start
        token_len   = 1
        output      = line + '\n'
        if token_len <= 1:
            output += (' ' * offset) + '^\n'
        else:
            output += (' ' * offset) + "'" + ('-' * (token_len - 2)) + "'\n"
        return output + '%s in line %s' % (error, line_number)

    def _msg(self, error):
        print self._format(error)

    def _error(self, error):
        raise Exception(self._format(error))

    def _eof(self):
        return self.start >= self.end

    def parse(self, input, builder):
        self._init()
        self.input   = input
        self.builder = builder
        self.end     = len(input)
        self.grammars['input'].parse(self)

    def dump(self):
        for grammar in self.grammars.itervalues():
            print str(grammar)
