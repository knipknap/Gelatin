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
import os
import re
import shutil
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse
from cgi import parse_qs

value   = r'"(?:\\.|[^"])*"'
attrib  = r'(?:[\$\w\-]+=%s)' % value
path_re = re.compile(r'^[^/"\?]+(?:\?%s?(?:&%s?)*)?' % (attrib, attrib))

class Builder(object):
    """
    Abstract base class for all generators.
    """
    def __init__(self):
        raise NotImplementedError('abstract method')

    def serialize(self):
        raise NotImplementedError('abstract method')

    def serialize_to_file(self, filename):
        with NamedTemporaryFile(delete=False, encoding='utf-8') as thefile:
            thefile.write(self.serialize())
        if os.path.exists(filename):
            os.unlink(filename)
        shutil.move(thefile.name, filename)

    def dump(self):
        raise NotImplementedError('abstract method')

    def _splitpath(self, path):
        match  = path_re.match(path)
        result = []
        while match is not None:
            result.append(match.group(0))
            path  = path[len(match.group(0)) + 1:]
            match = path_re.match(path)
        return result

    def _splittag(self, tag):
        url     = urlparse(tag)
        attribs = []
        for key, value in parse_qs(url.query).items():
            value = value[0]
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            attribs.append((key.lower(), value))
        return url.path.replace(' ', '-').lower(), attribs

    def create(self, path, data = None):
        """
        Creates the given node, regardless of whether or not it already
        exists.
        Returns the new node.
        """
        raise NotImplementedError('abstract method')

    def add(self, path, data = None, replace = False):
        """
        Creates the given node if it does not exist.
        Returns the (new or existing) node.
        """
        raise NotImplementedError('abstract method')

    def add_attribute(self, path, name, value):
        """
        Creates the given attribute and sets it to the given value.
        Returns the (new or existing) node to which the attribute was added.
        """
        raise NotImplementedError('abstract method')

    def open(self, path):
        """
        Creates and enters the given node, regardless of whether it already
        exists.
        Returns the new node.
        """
        raise NotImplementedError('abstract method')

    def enter(self, path):
        """
        Enters the given node. Creates it if it does not exist.
        Returns the node.
        """
        raise NotImplementedError('abstract method')

    def leave(self):
        """
        Returns to the node that was selected before the last call to enter().
        The history is a stack, to the method may be called multiple times.
        """
        raise NotImplementedError('abstract method')
