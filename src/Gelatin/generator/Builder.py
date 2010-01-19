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
from urlparse import urlparse
from cgi      import parse_qs

attrib  = r'(?:[\$\w\-]+(?:=\"[^"]*\"|=[\$\w\-]*)?)'
path_re = re.compile(r'^[^/"\?]+(?:\?%s?(?:&%s?)*)?' % (attrib, attrib))

class Builder(object):
    """
    Abstract base class for all generators.
    """
    def __init__(self):
        raise NotImplementedError('abstract method')

    def serialize(self):
        raise NotImplementedError('abstract method')

    def dump(self):
        raise NotImplementedError('abstract method')

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
            attribs.append((key.lower(), value))
        return url.path.replace(' ', '-').lower(), attribs

    def add(self, path, data = None):
        """
        Creates the given node if it does not exist.
        Returns the (new or existing) node.
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
