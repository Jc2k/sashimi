Integration Sashimi
===================

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

