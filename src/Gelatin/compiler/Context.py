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

def do_next(context):
    return 0

def do_skip(context):
    return 1

def do_fail(context, message = 'No matching statement found'):
    context._error(message)

def do_say(context, message):
    context._msg(message)
    return 0

def do_return(context, levels = 1):
    #print "do.return():", -levels
    return -levels

def out_add(context, path, data = None):
    #print "out.add():", path, data
    context.builder.add(path, data)
    context.builder.enter(path)
    context._trigger(context.on_add, context.re_stack[-1])
    context.builder.leave()
    return 0

def out_enter(context, path):
    #print "out.enter():", path
    context.builder.enter(path)
    context._trigger(context.on_add, context.re_stack[-1])
    context.stack[-1].on_leave.append((context.builder.leave, ()))
    return 0

def out_enqueue_before(context, regex, path, data = None):
    #print "ENQ BEFORE", regex.pattern, path, data
    context.on_match_before.append((regex, out_add, (context, path, data)))
    return 0

def out_enqueue_after(context, regex, path, data = None):
    #print "ENQ AFTER", regex.pattern, path, data
    context.on_match_after.append((regex, out_add, (context, path, data)))
    return 0

def out_enqueue_on_add(context, regex, path, data = None):
    #print "ENQ ON ADD", regex.pattern, path, data
    context.on_add.append((regex, out_add, (context, path, data)))
    return 0

class Context(object):
    def __init__(self):
        self.functions = {'do.fail':           do_fail,
                          'do.return':         do_return,
                          'do.next':           do_next,
                          'do.skip':           do_skip,
                          'do.say':            do_say,
                          'out.add':            out_add,
                          'out.enter':          out_enter,
                          'out.enqueue_before': out_enqueue_before,
                          'out.enqueue_after':  out_enqueue_after,
                          'out.enqueue_on_add': out_enqueue_on_add}
        self.lexicon  = {}
        self.grammars = {}
        self.input    = None
        self.builder  = None
        self.end      = 0
        self._init()

    def _init(self):
        self.start           = 0
        self.re_stack        = []
        self.stack           = []
        self.on_match_before = []
        self.on_match_after  = []
        self.on_add          = []

    def _trigger(self, triggers, match):
        matching = []
        for trigger in triggers:
            regex, func, args = trigger
            if regex.search(match.group(0)) is not None:
                matching.append(trigger)
        for trigger in matching:
            triggers.remove(trigger)
        for trigger in matching:
            regex, func, args = trigger
            func(*args)

    def _match_before_notify(self, match):
        self.re_stack.append(match)
        self._trigger(self.on_match_before, match)

    def _match_after_notify(self, match):
        self._trigger(self.on_match_after, match)
        self.re_stack.pop()

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
        if self.start < self.end:
            self._error('parser returned, but did not complete')

    def dump(self):
        for grammar in self.grammars.itervalues():
            print str(grammar)
