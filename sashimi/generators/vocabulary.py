
import random
from sashimi.generators.registry import registry


class TextFuzzer(object):

    ipsum = Ipsum()

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "text" and "vocabulary" in field:
            return True
        return False

    def fuzz(self, field):
        return random.choice(field["vocabulary"])


class StringFuzzer(object):

    ipsum = Ipsum()

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "string" and "vocabulary" in field:
            return True
        return False

    def fuzz(self, field):
        return random.choice(field["vocabulary"])


class LinesFuzzer(object):

    ipsum = Ipsum()

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "lines" and "vocabulary" in field:
            return True
        return False

    def fuzz(self, field):
        return random.choice(field["vocabulary"])


registry.register(TextFuzzer)
registry.register(StringFuzzer)
registry.register(LinesFuzzer)

