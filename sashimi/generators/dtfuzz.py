
from DateTime import DateTime
from sashimi.generators.registry import registry

class DatetimeFuzzer(object):

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "datetime":
            return True
        return False

    def fuzz(self, field):
        return DateTime()

registry.register(DatetimeFuzzer)
