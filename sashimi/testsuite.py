
import unittest

from AccessControl.SecurityManagement import newSecurityManager
from Testing.makerequest import makerequest

from sashimi.contenttypes import ContentTypeVisitor
from sashimi.report import HtmlReport

class ContentMapVisitor(object):

    def __init__(self, map):
        self.map = map
        self.content_types = []

    def enter_node(self, node):
        self.content_types.append(node)

    def leave_node(self, node):
        pass

    def __iter__(self):
        self.map.visit(self)
        return iter(self.content_types)

def fuzz_content_types(map, portal, report):
    visitor = ContentMapVisitor(map)
    urls = []
    for content_type in visitor:
        try:
            c = content_type.create_chain(portal)
            assert len(c.errors) == 0
            urls.append(c)
        except:
            report.exception(c)
        else:
            report.success(c)

    return urls


class MixinTestCase(object):

    def test_fuzz(self):
        report = HtmlReport("log.html")
        report.start()

        self.loginAsPortalOwner()

        a = ContentTypeVisitor(self.portal)
        map = a.visit_types()

        fuzz_content_types(map, self.portal, report)

        self.browser_login('editor')

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

