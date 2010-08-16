
import random
from sashimi.generators.registry import registry

def sibpath(path):
    d, f = os.path.split(__file__)
    return os.path.join(d, path)

class File(object):

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "file":
            return True
        return False

    def fuzz(self, field):
        return open(sibpath("assets/test.mp3")).read()

class Image(object):

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "image":
            return True
        return False

    def fuzz(self, field):
        return open(sibpath("assets/test.png")).read()

registry.register(Image)

