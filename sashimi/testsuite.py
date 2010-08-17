
import unittest

from AccessControl.SecurityManagement import newSecurityManager
from Testing.makerequest import makerequest

from sashimi.contenttypes import ContentTypeVisitor
from sashimi.content import fuzz_content_types
from sashimi.report import HtmlReport

class MixinTestCase(object):

    def test_fuzz(self):
        report = HtmlReport("log.html")
        report.start()

        print self.portal.portal_types[self.portal.portal_type].allowed_content_types

        self.loginAsPortalOwner()

        a = ContentTypeVisitor(self.portal)
        map = a.visit_types()

        fuzz_content_types(map, self.portal, report)

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

