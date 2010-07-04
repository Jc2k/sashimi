
class Registry(object):

    def __init__(self):
        self.fuzzers = []

    def register(self, fuzzer):
        self.fuzzers.append(fuzzer)

    def fuzz_field(self, field):
        for fuzzer in self.fuzzers:
            if fuzzer.can_fuzz(field):
                return fuzzer.fuzz(field)


# There is one registry
registry = Registry()

