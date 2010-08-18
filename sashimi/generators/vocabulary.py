
import random
from sashimi.generators.registry import registry


class TextFuzzer(object):

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "text" and "vocabulary" in field:
            return True
        return False

    def fuzz(self, field, content_types):
        return random.choice(field["vocabulary"])


class StringFuzzer(object):

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "string" and "vocabulary" in field:
            return True
        return False

    def fuzz(self, field, content_types):
        return random.choice(field["vocabulary"])


class LinesFuzzer(object):

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "lines" and "vocabulary" in field:
            return True
        return False

    def fuzz(self, field, content_types):
        return random.choice(field["vocabulary"])


registry.register(TextFuzzer)
registry.register(StringFuzzer)
registry.register(LinesFuzzer)

