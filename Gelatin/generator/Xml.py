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
import sys
from lxml import etree
from .Builder import Builder

class Xml(Builder):
    def __init__(self):
        self.etree   = etree.Element('xml')
        self.current = [self.etree]
        self.stack   = []

    def serialize(self):
        return etree.tostring(self.etree, encoding='unicode', pretty_print=True)

    def dump(self):
        print(self.serialize())

    def _splittag(self, path):
        tag, attribs = Builder._splittag(self, path)
        theattribs   = []
        for key, value in attribs:
            theattribs.append((key, value))
        return tag, theattribs

    def _tag2xpath(self, tag, attribs):
        tag = tag.replace(' ', '-')
        if not attribs:
            return tag
        attribs = ['@' + k + '="' + v.replace('"', '%22') + '"' for k, v in attribs]
        return './' + tag + '[' + ' and '.join(attribs) + ']'

    def create(self, path, data = None):
        node    = self.current[-1]
        path    = self._splitpath(path)
        n_items = len(path)
        for n, item in enumerate(path, 1):
            tag, attribs = self._splittag(item)

            # The leaf node is always newly created.
            if n == n_items:
                node = etree.SubElement(node, tag, **dict(attribs))
                break

            # Parent nodes are only created if the do not exist yet.
            xp = self._tag2xpath(tag, attribs)
            existing = node.find(xp)
            if existing is not None:
                node = existing
            else:
                node = etree.SubElement(node, tag, **dict(attribs))

        if data:
            node.text = data
        return node

    def add(self, path, data = None, replace = False):
        node = self.current[-1]
        for item in self._splitpath(path):
            tag, attribs = self._splittag(item)
            xpath        = self._tag2xpath(tag, attribs)
            try:
                next_node = node.xpath(xpath)
            except etree.XPathEvalError:
                msg = 'Invalid path: %s (%s)' % (repr(path), repr(xpath))
                raise Exception(msg)
            if next_node:
                node = next_node[0]
            else:
                node = etree.SubElement(node, tag, **dict(attribs))
        if replace:
            node.text = ''
        if data:
            node.text = node.text is not None and node.text or ''
            node.text += data
        return node

    def add_attribute(self, path, name, value):
        node = self.add(path)
        node.attrib[name] = value
        return node

    def open(self, path):
        #print "OPEN", path
        node = self.create(path)
        self.stack.append(self.current[-1])
        self.current.append(node)
        return node

    def enter(self, path):
        #print "ENTER", path
        node = self.add(path)
        self.stack.append(self.current[-1])
        self.current.append(node)
        return node

    def leave(self):
        #print "LEAVE"
        node = self.stack.pop()
        while self.current[-1] != node:
            self.current.pop()
