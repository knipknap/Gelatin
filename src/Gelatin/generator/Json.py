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
import json
from collections import defaultdict
from Builder import Builder
from pprint import PrettyPrinter

class Node:
    def __init__(self, name, attribs = None):
        self.name = name
        self.attribs = attribs and attribs or []
        self.children = defaultdict(list)
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
        thedict = dict(('@' + k, v) for (k, v) in self.attribs)
        children_dict = dict()
        for name, child_list in self.children.iteritems():
            if len(child_list) == 1:
                children_dict[name] = child_list[0].to_dict()
                continue
            children_dict[name] = [child.to_dict() for child in child_list]
        thedict.update(children_dict)
        if self.text is not None:
            thedict['#text'] = self.text
        return thedict

    def dump(self, indent = 0):
        for name, children in self.children.iteritems():
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
        return json.dumps(self.tree.to_dict(), indent = 4)

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
