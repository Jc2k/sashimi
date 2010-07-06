
import datetime
from sashimi.generators.registry import registry

class DatetimeFuzzer(object):

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "datetime":
            return True
        return False

    def fuzz(self, field):
        return datetime.datetime.now()

registry.register(DatetimeFuzzer)
