#!/usr/bin/python
import time
import BaseHTTPServer
from pprint import pprint
import urlparse

HOST_NAME = 'localhost' 
PORT_NUMBER = 8080

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        def do_POST(s):
                request_path = s.path
                print "path:", request_path
                """Respond to a POST request."""
                length = int(s.headers['Content-Length'])
                post_data = urlparse.parse_qs(s.rfile.read(length).decode('utf-8'))
                for key, value in post_data.iteritems():
                    print "%s=%s" % (key, value)

                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()

if __name__ == '__main__':
        server_class = BaseHTTPServer.HTTPServer
        httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
        print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
        try:
                httpd.serve_forever()
        except KeyboardInterrupt:
                pass
        httpd.server_close()
        print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)