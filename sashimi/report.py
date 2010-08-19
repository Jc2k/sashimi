import sys
import codecs
import traceback
from cStringIO import StringIO

from zExceptions.ExceptionFormatter import format_exception

class HtmlReport(object):

    def __init__(self, log):
        self.log = codecs.open(log, "w", "utf-8")

    def start(self):
        self.log.write("<html><head><title>Fuzzing Report</title></head><body>")

    def finish(self):
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
            tb = tb[:idx]
        output.write(tb)
        output.write("</pre>")

        self.log.write(output.getvalue())

    def success(self, content):
        return
        output = StringIO()
        output.write("<p>Content created OK!</p>")
        self._common_blah(output, content)
        self.log.write(output.getvalue())

