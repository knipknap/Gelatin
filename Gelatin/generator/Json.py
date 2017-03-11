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
import json
from collections import OrderedDict, Callable, defaultdict
from .Builder import Builder
from pprint import PrettyPrinter

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

class Node(object):
    def __init__(self, name, attribs = None):
        self.name = name
        self.attribs = attribs and attribs or []
        self.children = OrderedDefaultDict(list)
        self.text = None

    def add(self, child):
        self.children[child.name].append(child)
        return child

    def get_child(self, name, attribs = None):
        """
        Returns the first child that matches the given name and
        attributes.
        """
        if name == '.':
            if attribs is None or len(attribs) == 0:
                return self
            if attribs == self.attribs:
                return self
        for child in self.children[name]:
            if child.attribs == attribs:
                return child
        return None

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

    def dump(self, indent = 0):
        for name, children in self.children.items():
            for child in children:
                child.dump(indent + 1)

class Json(Builder):
    """
    Abstract base class for all generators.
    """
    def __init__(self):
        self.tree    = Node('root')
        self.current = [self.tree]

    def serialize(self):
        return json.dumps(self.tree.to_dict(), indent=4, ensure_ascii=False)

    def dump(self):
        #pp = PrettyPrinter(indent = 4)
        #pp.pprint(self.tree.to_dict())
        self.tree.dump()

    def create(self, path, data = None):
        node    = self.current[-1]
        path    = self._splitpath(path)
        n_items = len(path)
        for n, item in enumerate(path):
            tag, attribs = self._splittag(item)

            # The leaf node is always newly created.
            if n == n_items:
                node = node.add(Node(tag, attribs))
                break

            # Parent nodes are only created if they do not exist yet.
            existing = node.get_child(tag, attribs)
            if existing:
                node = existing
            else:
                node = node.add(Node(tag, attribs))
        return node

    def add(self, path, data = None, replace = False):
        node = self.current[-1]
        for item in self._splitpath(path):
            tag, attribs = self._splittag(item)
            next_node    = node.get_child(tag, attribs)
            if next_node is not None:
                node = next_node
            else:
                node = node.add(Node(tag, attribs))
        if replace:
            node.text = ''
        if data:
            node.text = data
        return node

    def add_attribute(self, path, name, value):
        node = self.add(path)
        node.attribs.append((name, value))
        return node

    def open(self, path):
        self.current.append(self.create(path))
        return self.current[-1]

    def enter(self, path):
        self.current.append(self.add(path))
        return self.current[-1]

    def leave(self):
        self.current.pop()
