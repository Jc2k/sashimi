from unittest import TestCase
from sashimi.generators.registry import Registry, registry

class TestRegistry(TestCase):

    def test_actual_registry(self):
        fuzzers = registry.get_fuzzers({"type": "dummy"})
        self.failUnlessEqual(len(list(fuzzers)), 0)
