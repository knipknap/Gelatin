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
from Builder import Builder
from pprint  import PrettyPrinter

class Node:
    def __init__(self, name, attribs = None):
        self.name     = name
        self.attribs  = attribs and attribs or []
        self.children = []
        self.text     = None

    def add(self, child):
        self.children.append(child)
        return child

    def get_child(self, name, attribs):
        if name == '.' and attribs == self.attribs:
            return self
        for child in self.children:
            if child.name == name and child.attribs == attribs:
                return child
        return None

    def to_dict(self):
        nodes    = dict(('@' + k, v) for (k, v) in self.attribs)
        children = dict((c.name, c.to_dict()) for c in self.children)
        nodes.update(children)
        if self.text is not None:
            nodes['#text'] = self.text
        return nodes

    def dump(self, indent = 0):
        print '  ' * indent + self.name + str(self.attribs) + ':'
        print '  ' * (indent + 1) + '#text: ' + str(self.text)
        for child in self.children:
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

    def add(self, path, data = None):
        node = self.current[-1]
        for item in self._splitpath(path):
            tag, attribs = self._splittag(item)
            next_node    = node.get_child(tag, attribs)
            if next_node:
                node = next_node
            else:
                node = node.add(Node(tag, attribs))
        if data:
            node.text = data
        return node

    def enter(self, path):
        self.current.append(self.add(path))
        return self.current[-1]

    def leave(self):
        self.current.pop()
