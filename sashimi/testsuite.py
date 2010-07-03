
import unittest

from AccessControl.SecurityManagement import newSecurityManager
from Testing.makerequest import makerequest
import transaction

from sashimi.contenttypes import ContentTypeVisitor
from sashimi.content import ContentMapVisitor


class TestCase(object):

    def login(app, manager_user):
        user = app.acl_users.getUserById(manager_user).__of__(app.acl_users)
        newSecurityManager(None, user)
        return makerequest(app)

    def test_fuzz(self):
        #app = login(app, "zopeadmin")

        a = ContentTypeVisitor(self.portal)
        map = a.visit_types()

        b = ContentMapVisitor(map)
        b.fuzz()


class TestSuite(unittest.TestSuite):

    def __init__(self, mixin):
        super(TestSuite, self).__init__()
        cls = type('TestFuzzing', (mixin, TestCase), {})
        self.addTest(unittest.makeSuite(cls))

