
import unittest

from AccessControl.SecurityManagement import newSecurityManager
from Testing.makerequest import makerequest

from sashimi.contenttypes import ContentTypeVisitor
from sashimi.content import ContentMapVisitor


class MixinTestCase(object):

    def promote(self, app, manager_user):
        user = app.acl_users.getUserById(manager_user).__of__(app.acl_users)
        newSecurityManager(None, user)
        return makerequest(app)

    def test_fuzz(self):
        #portal = self.promote(self.portal, "editor")
        self.loginAsPortalOwner()

        a = ContentTypeVisitor(self.portal)
        map = a.visit_types()

        b = ContentMapVisitor(map, self.portal)
        urls = b.fuzz()

        self.browser_login('editor')

        f = open("log.txt", "w")
        errors, pos, size = 0, 1, len(urls)
        for url, content in urls:
            f.write("test: %d of %d (%d errors so far)\n" % (pos, size, errors))
            f.write("breadcrumb: %s\n" % content.content_type.get_breadcrumb())
            f.write("url: %s\n" % url)
            f.write("data: %s\n\n" % content.data)

            try:
                self.browser.open(url)
            except:
                errors += 1
                import traceback
                traceback.print_exc(file=f)

            f.write("--------------------------------------------------------------\n\n\n")
            pos += 1

        f.write("Test summary: %d tests run, %d tests passed, %d tests failed.\n" % (size, size-errors, errors))

        f.close()


class TestSuite(unittest.TestSuite):

    def __init__(self, mixin):
        super(TestSuite, self).__init__()
        cls = type('TestFuzzing', (mixin, MixinTestCase), {})
        self.addTest(unittest.makeSuite(cls))

