
class Registry(object):

    def __init__(self):
        self.fuzzers = []

    def register(self, fuzzer):
        self.fuzzers.append(fuzzer)

    def get_fuzzers(self, field):
        for fuzzer in self.fuzzers:
            if fuzzer.can_fuzz(field):
                yield fuzzer()


# There is one registry
registry = Registry()

