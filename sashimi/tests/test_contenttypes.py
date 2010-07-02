import unittest
from mock import Mock

from sashimi.contenttypes import ContentTypeVisitor, ContentTypeRoot

class TestContentTypes(unittest.TestCase):

    def test_no_content_types(self):
        portal = Mock()
        portal.portal_types.listContentTypes.return_value = []
        c = ContentTypeVisitor(portal)
        retval = c.visit_types()
        self.failUnless(isinstance(retval, ContentTypeRoot))


