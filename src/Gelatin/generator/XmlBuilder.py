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
import re
from urlparse import urlparse, parse_qs
from lxml     import etree

attrib  = r'(?:[\$\w\-]+(?:=\"[^"]*\"|=[\$\w\-]*)?)'
path_re = re.compile(r'^[^/"\?]+(?:\?%s?(?:&%s?)*)?' % (attrib, attrib))

class XmlBuilder(object):
    def __init__(self):
        self.etree   = etree.Element('root')
        self.current = self.etree

    def dump(self):
        print etree.tostring(self.etree, pretty_print = True)

    def _splitpath(self, path):
        match  = path_re.match(path)
        result = []
        while match is not None:
            result.append(match.group(0))
            path = path[len(match.group(0)) + 1:]
            match  = path_re.match(path)
        return result

    def _splittag(self, tag):
        url     = urlparse(tag)
        attribs = []
        for key, value in parse_qs(url.query).iteritems():
            value = value[0]
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            attribs.append((key, value))
        return url.path.replace(' ', '-'), attribs

    def _tag2xpath(self, tag, attribs):
        tag = tag.replace(' ', '-')
        if not attribs:
            return tag
        attribs = ' and '.join('@' + k + '="' + v + '"' for k, v in attribs)
        return './' + tag + '[' + attribs + ']'

    def add(self, path, data = None):
        """
        Creates the given node if it does not exist.
        Returns the (new or existing) node.
        """
        print "ADD:", path, data
        node = self.current
        for item in self._splitpath(path):
            tag, attribs = self._splittag(item)
            xpath        = self._tag2xpath(tag, attribs)
            next_node    = self.current.xpath(xpath)
            if next_node:
                node = next_node[0]
            else:
                node = etree.SubElement(node, tag, **dict(attribs))
        node.text = data
        return node

    def enter(self, path):
        """
        Enters the given node. Creates it if it does not exist.
        Returns the node.
        """
        print "ENTER", path
        self.current_node = self.add(path)
        return self.current_node
