
try:
    from DateTime import DateTime
except ImportError:
    pass

from sashimi.generators.registry import registry

class DatetimeFuzzer(object):

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "datetime":
            return True
        return False

    def fuzz(self, field, content_types):
        return DateTime()

registry.register(DatetimeFuzzer)
