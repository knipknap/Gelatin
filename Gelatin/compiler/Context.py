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
import codecs
import sys


def do_next(context):
    """Function for do.next."""
    return 0


def do_skip(context):
    """Function for do.skip."""
    return 1


def do_fail(context, message="No matching statement found"):
    """Function for do.fail."""
    context._error(message)


def do_say(context, message):
    """Function for do.say."""
    context._msg(message)
    return 0


def do_warn(context, message):
    """Function for do.warn."""
    context._warn(message)
    return 0


def do_return(context, levels=1):
    """Function for do.return."""
    return -levels


def out_create(context, path, data=None):
    """Function for out.create."""
    context.builder.create(path, data)
    context.builder.enter(path)
    context._trigger(context.on_add, context.re_stack[-1])
    context.builder.leave()
    return 0


def out_replace(context, path, data=None):
    """Function for out.replace."""
    context.builder.add(path, data, replace=True)
    context.builder.enter(path)
    context._trigger(context.on_add, context.re_stack[-1])
    context.builder.leave()
    return 0


def out_add(context, path, data=None):
    """Function for out.add."""
    context.builder.add(path, data)
    context.builder.enter(path)
    context._trigger(context.on_add, context.re_stack[-1])
    context.builder.leave()
    return 0


def out_add_attribute(context, path, name, value):
    """Function for out.add_attribute."""
    context.builder.add_attribute(path, name, value)
    context.builder.enter(path)
    context._trigger(context.on_add, context.re_stack[-1])
    context.builder.leave()
    return 0


def out_open(context, path):
    """Function for out.open."""
    context.builder.open(path)
    context._trigger(context.on_add, context.re_stack[-1])
    context.stack[-1].on_leave.append((context.builder.leave, ()))
    return 0


def out_enter(context, path):
    """Function for out.enter."""
    context.builder.enter(path)
    context._trigger(context.on_add, context.re_stack[-1])
    context.stack[-1].on_leave.append((context.builder.leave, ()))
    return 0


def out_enqueue_before(context, regex, path, data=None):
    """Function for out.enqueue_before."""
    context.on_match_before.append((regex, out_add, (context, path, data)))
    return 0


def out_enqueue_after(context, regex, path, data=None):
    """Function for out.enqueue_after."""
    context.on_match_after.append((regex, out_add, (context, path, data)))
    return 0


def out_enqueue_on_add(context, regex, path, data=None):
    """Function for out.enqueue_on_add."""
    context.on_add.append((regex, out_add, (context, path, data)))
    return 0


def out_clear_queue(context):
    """Function for out.clear_queue."""
    context._clear_triggers()
    return 1


def out_set_root_name(context, name):
    """Function for out.set_root_name."""
    context.builder.set_root_name(name)
    return 0


class Context(object):
    """TODO: Create docstring."""

    def __init__(self):
        """TODO: Create docstring."""
        self.functions = {
            "do.fail": do_fail,
            "do.return": do_return,
            "do.next": do_next,
            "do.skip": do_skip,
            "do.say": do_say,
            "do.warn": do_warn,
            "out.create": out_create,
            "out.replace": out_replace,
            "out.add": out_add,
            "out.add_attribute": out_add_attribute,
            "out.open": out_open,
            "out.enter": out_enter,
            "out.enqueue_before": out_enqueue_before,
            "out.enqueue_after": out_enqueue_after,
            "out.enqueue_on_add": out_enqueue_on_add,
            "out.clear_queue": out_clear_queue,
            "out.set_root_name": out_set_root_name,
        }
        self.lexicon = {}
        self.grammars = {}
        self.input = None
        self.builder = None
        self.end = 0
        self._init()

    def _init(self):
        """TODO: Create docstring."""
        self.start = 0
        self.re_stack = []
        self.stack = []
        self._clear_triggers()

    def _clear_triggers(self):
        """TODO: Create docstring."""
        self.on_match_before = []
        self.on_match_after = []
        self.on_add = []

    def _trigger(self, triggers, match):
        """TODO: Create docstring."""
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
        """TODO: Create docstring."""
        self.re_stack.append(match)
        self._trigger(self.on_match_before, match)

    def _match_after_notify(self, match):
        """TODO: Create docstring."""
        self._trigger(self.on_match_after, match)
        self.re_stack.pop()

    def _get_lineno(self):
        """Returns current line number."""
        return self.input.count("\n", 0, self.start) + 1

    def _get_line(self, number=None):
        """Returns current line."""
        if number is None:
            number = self._get_lineno()
        return self.input.split("\n")[number - 1]

    def _get_line_position_from_char(self, char):
        """TODO: Create docstring."""
        line_start = char
        while line_start != 0:
            if self.input[line_start - 1] == "\n":
                break
            line_start -= 1
        line_end = self.input.find("\n", char)
        return line_start, line_end

    def _format(self, error):
        """Print error to console."""
        start, end = self._get_line_position_from_char(self.start)
        line_number = self._get_lineno()
        line = self._get_line()
        offset = self.start - start
        token_len = 1
        output = f"{line}\n"
        if token_len <= 1:
            output += f"{' ' * offset}^\n"
        else:
            output += f"{' ' * offset}'{'-' * (token_len - 2)}'\n"
        output += f"{error} in line {line_number}"
        return output

    def _msg(self, error):
        """Print error to console."""
        print(self._format(error))

    def _warn(self, error):
        """Print error to stderr."""
        sys.stderr.write(self._format(error) + "\n")

    def _error(self, error):
        """Raise exception with error message."""
        raise Exception(self._format(error))

    def _eof(self):
        """Returns true if end of file has been reached."""
        return self.start >= self.end

    def parse_string(self, input, builder, debug=0):
        """Parses a string with the given builder."""
        self._init()
        self.input = input
        self.builder = builder
        self.end = len(input)
        self.grammars["input"].parse(self, debug)
        if self.start < self.end:
            self._error("parser returned, but did not complete")

    def parse(self, filename, builder, encoding="utf8", debug=0):
        """Parses a file with the given builder."""
        with codecs.open(filename, "r", encoding=encoding) as input_file:
            return self.parse_string(input_file.read(), builder, debug)

    def dump(self):
        """Print all grammars of the context."""
        for grammar in self.grammars.values():
            print(grammar)
