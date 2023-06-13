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
import sys
import shutil
from tempfile import NamedTemporaryFile
if sys.version_info[0] > 3 or sys.version_info[0] == 3 and sys.version_info[1] >= 10:
    from collections.abc import Callable
else:
    from collections import Callable
from collections import OrderedDict, defaultdict
try:
    from urllib.parse import urlparse, parse_qs, unquote
except ImportError:
    from urlparse import urlparse, unquote
    from cgi import parse_qs

value = r'"(?:\\.|[^"])*"'
attrib = r'(?:[\$\w\-]+=%s)' % value
path_re = re.compile(r'^[^/"\?]+(?:\?%s?(?:&%s?)*)?' % (attrib, attrib))


class OrderedDefaultDict(OrderedDict):

    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and
           not isinstance(default_factory, Callable)):
            raise TypeError('first argument must be callable')
        OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        import copy
        return type(self)(self.default_factory,
                          copy.deepcopy(self.items()))

    def __repr__(self):
        return 'OrderedDefaultDict(%s, %s)' % (self.default_factory,
                                               OrderedDict.__repr__(self))

def nodehash(name, attribs):
    return name + '/' + str(hash(frozenset(attribs)))

class Node(object):

    def __init__(self, name, attribs=None):
        self.name = name
        self.attribs = attribs and attribs or []
        self.children = OrderedDefaultDict(list)
        self.child_index = dict()
        self.text = None

    def add(self, child):
        self.children[child.name].append(child)
        self.child_index[nodehash(child.name, child.attribs)] = child
        return child

    def get_child(self, name, attribs=None):
        """
        Returns the first child that matches the given name and
        attributes.
        """
        if name == '.':
            if attribs is None or len(attribs) == 0:
                return self
            if attribs == self.attribs:
                return self
        return self.child_index.get(nodehash(name, attribs))

    def to_dict(self):
        thedict = OrderedDict(('@' + k, v) for (k, v) in self.attribs)
        children_dict = OrderedDict()
        for name, child_list in self.children.items():
            if len(child_list) == 1:
                children_dict[name] = child_list[0].to_dict()
                continue
            children_dict[name] = [child.to_dict() for child in child_list]
        thedict.update(children_dict)
        if self.text is not None:
            thedict['#text'] = self.text
        return thedict

    def dump(self, indent=0):
        for name, children in self.children.items():
            for child in children:
                child.dump(indent + 1)


class Builder(object):

    """
    Abstract base class for all generators.
    """

    def __init__(self):
        self.tree = Node(None)
        self.current = [self.tree]

    def serialize(self, serializer):
        return serializer.serialize_doc(self.tree)

    def serialize_to_file(self, filename):
        with NamedTemporaryFile(delete=False, encoding='utf-8') as thefile:
            thefile.write(self.serialize())
        if os.path.exists(filename):
            os.unlink(filename)
        shutil.move(thefile.name, filename)

    def set_root_name(self, name):
        self.tree.name = name

    def dump(self):
        # pp = PrettyPrinter(indent = 4)
        # pp.pprint(self.tree.to_dict())
        self.tree.dump()

    def _splitpath(self, path):
        match = path_re.match(path)
        result = []
        while match is not None:
            result.append(match.group(0))
            path = path[len(match.group(0)) + 1:]
            match = path_re.match(path)
        return result

    def _splittag(self, tag):
        url = urlparse(tag)
        attribs = []
        for key, value in parse_qs(url.query).items():
            value = value[0]
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            attribs.append((key.lower(), value))
        return url.path.replace(' ', '-').lower(), attribs

    def create(self, path, data=None):
        """
        Creates the given node, regardless of whether or not it already
        exists.
        Returns the new node.
        """
        node = self.current[-1]
        path = self._splitpath(path)
        n_items = len(path)
        for n, item in enumerate(path):
            tag, attribs = self._splittag(item)

            # The leaf node is always newly created.
            if n == n_items-1:
                node = node.add(Node(tag, attribs))
                break

            # Parent nodes are only created if they do not exist yet.
            existing = node.get_child(tag, attribs)
            if existing is not None:
                node = existing
            else:
                node = node.add(Node(tag, attribs))
        if data:
            node.text = unquote(data)
        return node

    def add(self, path, data=None, replace=False):
        """
        Creates the given node if it does not exist.
        Returns the (new or existing) node.
        """
        node = self.current[-1]
        for item in self._splitpath(path):
            tag, attribs = self._splittag(item)
            next_node = node.get_child(tag, attribs)
            if next_node is not None:
                node = next_node
            else:
                node = node.add(Node(tag, attribs))
        if replace:
            node.text = ''
        if data:
            if node.text is None:
                node.text = unquote(data)
            else:
                node.text += unquote(data)
        return node

    def add_attribute(self, path, name, value):
        """
        Creates the given attribute and sets it to the given value.
        Returns the (new or existing) node to which the attribute was added.
        """
        node = self.add(path)
        node.attribs.append((name, value))
        return node

    def open(self, path):
        """
        Creates and enters the given node, regardless of whether it already
        exists.
        Returns the new node.
        """
        self.current.append(self.create(path))
        return self.current[-1]

    def enter(self, path):
        """
        Enters the given node. Creates it if it does not exist.
        Returns the node.
        """
        self.current.append(self.add(path))
        return self.current[-1]

    def leave(self):
        """
        Returns to the node that was selected before the last call to enter().
        The history is a stack, to the method may be called multiple times.
        """
        self.current.pop()
