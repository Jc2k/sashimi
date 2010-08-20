import sys
import codecs
import traceback
import re
import cgi
from cStringIO import StringIO

from zExceptions.ExceptionFormatter import format_exception

class HtmlReport(object):

    def __init__(self, log):
        self.log = codecs.open(log, "w", "utf-8")
        self.successes = 0
        self.exceptions = 0
        self.exception_log = {}

        self.traceback_info_re = re.compile(r"- __traceback_info__: (.*)$", re.M)

    def start(self):
        style = "<style>h2 pre { display: inline; }</style>"
        self.log.write("<html><head><title>Fuzzing Report</title>%s</head><body>" % style)

    def finish(self):
        self.log.write("<h2>Summary</h2>")
        self.log.write("<p>%d tests done, %d successes, %d failures</p>" % (self.successes+self.exceptions, self.successes, self.exceptions))

        keys = self.exception_log.keys()
        keys.sort()

        self.log.write('<table cellspacing="0" cellpadding="2">')
        self.log.write("<tr><th>Go</th><th>Exception</th><th>TB Info</th><th>Occurences</th></tr>")
        for i, key in enumerate(keys):
            row_class = i % 2 and 'even' or 'odd'
            self.log.write('<tr class="%s">' % row_class )
            self.log.write("<td><a href='#%s'>&darr;</a></td>" % hash(key))
            self.log.write("<td><pre>%s</pre></td>" % key[0])
            self.log.write("<td><pre>%s</pre></td>" % key[1])
            self.log.write("<td>%d</td>" % len(self.exception_log[key]))
            self.log.write("</tr>")
        self.log.write("</table>")

        for key, info in self.exception_log.iteritems():
            self.log.write("<h2><a name='%s'>Exception: <pre>%s</pre>, TB Info: <pre>%s</pre></a></h2>" %
                (hash(key), key[0], key[1]))
            for error in info:
                self.log.write(error.getvalue())

        self.log.write("</body></html>")
        self.log.close()

    def _common_blah(self, output, content):
        output.write("<h3>%s</h3>" % content.content_type.get_breadcrumb())

        output.write("<h4>Generated Data</h4>")
        output.write("<table>")
        for field, schema in content.content_type.info["fields"].iteritems():
            output.write("<tr>")
            output.write("<td>%s</td>" % field)
            output.write("<td>%s</td>" % schema["type"])
            if field in content.data:
                if schema["type"] not in ("file", "image"):
                    output.write("<td><pre>%s</pre></td>" % content.data[field])
                else:
                    output.write("<td>A file from assets/ dir</td>")
            else:
                output.write("<td>Not set</td>")
            output.write("</tr>")
        output.write("</table>")

    def exception(self, content):
        self.exceptions += 1

        output = StringIO()
        self._common_blah(output, content)

        if len(content.errors) > 0:
            output.write("<h4>Validation Errors</h4>")
            output.write("<table>")
            for key, value in content.errors.iteritems():
                output.write("<tr>")
                output.write("<td>%s</td><td>%s</td>" % (key, value))
                output.write("</tr>")
            output.write("</table>")

        #output.write("<h4>Error Info</h4>")
        #output.write("<table>")
        #for key in ('username', 'url', 'userid', 'value', 'time', 'type', 'id'):
        #    output.write("<tr><td>%s</td><td>%s</td></tr>" % (key, site_error[key]))
        #output.write("</table>")

        output.write("<h4>Traceback</h4>")
        output.write("<pre>")
        #srsly? there has to be a better way :(
        traceback = content.traceback
        if not traceback:
            traceback = sys.exc_info()
        tb = ''.join(format_exception(*traceback, **{"as_html":0}))
        idx = tb.find("<!DOCTYPE")
        if idx >= 0:
            tb = tb[:idx].strip()
        output.write(cgi.escape(tb))
        output.write("</pre>")

        tb_info = "".join(self.traceback_info_re.findall(tb)[-1:])
        exception = "".join(tb.strip().split("\n")[-1:])

        self.exception_log.setdefault((exception, tb_info), []).append(output)

    def success(self, content):
        self.successes += 1
        return
        output = StringIO()
        output.write("<p>Content created OK!</p>")
        self._common_blah(output, content)
        self.log.write(output.getvalue())

