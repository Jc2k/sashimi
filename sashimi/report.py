import codecs
import traceback
from cStringIO import StringIO

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

        output.write("<h4>Traceback</h4>")
        output.write("<pre>")
        traceback.print_exc(file=output)
        output.write("</pre>")

        self.log.write(output.getvalue())

    def success(self, content):
        return
        output = StringIO()
        output.write("<p>Content created OK!</p>")
        self._common_blah(output, content)
        self.log.write(output.getvalue())

