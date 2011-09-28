Sashimi
=======

Sashimi is an automatic and dynamic test case for finding and breaking untested
code paths in your application. It uses fuzzing techniques combined with
knowledge of how content types fit together in order to build a test site
with random content and then spiders it to find broken views.

This is not 'production ready'; its something i hacked together whilst learning Plone.

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

