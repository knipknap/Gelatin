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
from .Builder import Builder


class Dummy(Builder):
    """TODO: Create docstring."""

    def __init__(self):
        """TODO: Create docstring."""
        pass

    def serialize(self):
        """TODO: Create docstring."""
        return ""

    def set_root_name(self, name):
        """TODO: Create docstring."""
        pass

    def dump(self):
        """TODO: Create docstring."""
        print(self.serialize())

    def add(self, path, data=None, replace=False):
        """TODO: Create docstring."""
        pass

    def add_attribute(self, path, name, value):
        """TODO: Create docstring."""
        pass

    def open(self, path):
        """TODO: Create docstring."""
        pass

    def enter(self, path):
        """TODO: Create docstring."""
        pass

    def leave(self):
        """TODO: Create docstring."""
        pass
