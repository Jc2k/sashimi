
import unittest

from AccessControl.SecurityManagement import newSecurityManager
from Testing.makerequest import makerequest

from sashimi.contenttypes import ContentTypeVisitor
from sashimi.content import ContentMapVisitor
from sashimi.report import HtmlReport

class MixinTestCase(object):

    def promote(self, app, manager_user):
        user = app.acl_users.getUserById(manager_user).__of__(app.acl_users)
        newSecurityManager(None, user)
        return makerequest(app)

    def test_fuzz(self):
        report = HtmlReport("log.html")
        report.start()

        #portal = self.promote(self.portal, "editor")
        self.loginAsPortalOwner()

        a = ContentTypeVisitor(self.portal)
        map = a.visit_types()

        b = ContentMapVisitor(map, self.portal)
        urls = b.fuzz(report)

        self.browser_login('editor')

        for url, content in urls:
            try:
                self.browser.open(url)
            except:
                report.exception(content)
                continue

            report.success(content)

        report.finish()


class TestSuite(unittest.TestSuite):

    def __init__(self, mixin):
        super(TestSuite, self).__init__()
        cls = type('TestFuzzing', (mixin, MixinTestCase), {})
        self.addTest(unittest.makeSuite(cls))

