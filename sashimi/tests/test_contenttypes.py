import unittest
from mock import Mock

from sashimi.contenttypes import ContentTypeVisitor, ContentTypeRoot


class IndexableObject(object):
    '''Creates an object that wraps around the mock object so when it is
    indexable: mock_object[id] is the same as getattr(mock_object[id]) and
    similarly with set'''

    def __init__(self, mock_object):
        # self._inner = mock_object means mock_object._inner = mock_object
        # which causes a recursive call when we do a getattr for _inner
        object.__setattr__(self, '_inner', mock_object)

    def __getattr__(self, attr):
        return getattr(self._inner, str(attr))

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __setattr__(self, attr, value):
        setattr(self._inner, attr, value)

    def __setitem__(self, item, value):
        self.__setattr__(item, value)


class TestContentTypes(unittest.TestCase):

    def test_no_content_types(self):
        portal = Mock()
        portal.portal_types.listContentTypes.return_value = []
        c = ContentTypeVisitor(portal)
        retval = c.visit_types()
        self.failUnless(isinstance(retval, ContentTypeRoot))

    def test_simple_content_type(self):
        portal = Mock()
        portal.portal_types = IndexableObject(Mock())
        portal.portal_types['Folder'].allowed_content_types = ['Folder']
        portal.portal_types.listContentTypes.return_value = ["Folder"]
        c = ContentTypeVisitor(portal)
        retval = c.visit_types()

        visitor = Mock()
        retval.visit(visitor)

        for args, kwargs in visitor.visit_node.call_args_list:
            node = args[0]
            print node.get_breadcrumb()

