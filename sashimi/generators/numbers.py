
import random
from sashimi.generators.registry import registry

class Numbers(object):

    @classmethod
    def can_fuzz(cls, field):
        return False

    def fuzz(self, field):
        return random.randint(0, 9999999999999)


registry.register(Numbers)

