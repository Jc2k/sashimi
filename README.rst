Sashimi
=======

Something I threw together to automatically work out how to build a site from defined
content types and then find ways to break it.

Adding to test suite
--------------------

Add a new test module to your project::

    from myapp import BaseTestCase
    from sashimi.testsuite import TestSuite

    class TestCaseMixin(BaseTestCase):

        def afterSetUp(self):
            pass

        def beforeTearDown(self):
            pass

    def test_suite():
        return TestSuite(TestCaseMixin)

