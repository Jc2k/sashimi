import sys
import traceback


class TracebackWrapper(object):

    def __init__(self, ex_type, ex_value, tb, info=None):
        self.ex_type = ex_type
        self.ex_value = ex_value
        self.tb = tb
        self.info = info

    def __hash__(self):
        return hash(self.format(limit=3))

    def extract_tb(self, limit=None):
        return traceback.extract_tb(self.tb, limit)

    def format(self, limit=None):
        # This is a hack because testbrowser exceptions BLOW
        ex_value = ""
        return ''.join(traceback.format_exception(self.ex_type, ex_value, self.tb, limit))

    def format_tb(self, limit=None):
        return ''.join(traceback.format_list(self.extract_tb(limit)))

    def format_exception(self):
        return ''.join(traceback.format_exception_only(self.ex_type, ""))

    def __eq__(self, tb):
        if type(self) != type(tb):
            return False
        return self.format() == tb.format()


class TracebackCollector(object):

    def __init__(self):
        self.tracebacks = {}

    def collect(self, ex_type, ex_value, tb, info):
        t = TracebackWrapper(ex_type, ex_value, tb, info)
        h = hash(t)

        if not h in self.tracebacks:
            self.tracebacks[h] = (t.format_exception(), [])

        self.tracebacks[h][1].append(t)

    def collect_from_callable(self, cble, info, *args, **kwargs):
        try:
            return cble(*args, **kwargs)
        except:
            ex_type, ex_value, tb = sys.exc_info()
            self.collect(ex_type, ex_value, tb, info)
            raise

    def iter_batches(self):
        return self.tracebacks.itervalues()

