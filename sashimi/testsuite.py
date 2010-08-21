
import unittest

from AccessControl.SecurityManagement import newSecurityManager
from Testing.makerequest import makerequest

from sashimi.contenttypes import ContentTypeVisitor
from sashimi.report import HtmlReport

class CreateSiteStructure(object):

    def __init__(self, map, portal):
        self.map = map
        self.portal = portal
        self.parents = [None]
        self.created = []

    def enter_node(self, node):
        c = node.create(self.parents[-1], self.portal)
        if c.traceback or len(c.errors) > 0:
            self.report.exception(c)
        else:
            self.report.success(c)
        self.created.append(c)
        self.parents.append(c)

    def leave_node(self, node):
        self.parents.pop()

    def create(self, report):
        self.report = report
        self.map.visit(self)
        return self.created


class MixinTestCase(object):

    def test_fuzz(self):
        report = HtmlReport("log.html")
        report.start()

        self.loginAsPortalOwner()

        a = ContentTypeVisitor(self.portal)
        map = a.visit_types()

        urls = CreateSiteStructure(map, self.portal).create(report)

        try:
            self.browser_login('editor')
        except:
            # login will generally work, but the redirect to /portal might kill us
            pass

        for content in urls:
            try:
                content.browse(self.browser)
            except:
                report.exception(content)
            else:
                report.success(content)

        report.finish()


class TestSuite(unittest.TestSuite):

    def __init__(self, mixin):
        super(TestSuite, self).__init__()
        cls = type('TestFuzzing', (mixin, MixinTestCase), {})
        self.addTest(unittest.makeSuite(cls))

