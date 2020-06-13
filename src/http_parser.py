from http.server import BaseHTTPRequestHandler
from io import BytesIO

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

    def get_headers(self):
        return {header: val for header, val in self.headers._headers}

    def get_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = dict()
        if content_length:
            raw = self.rfile.read(content_length)
            for pairs in raw.split('&'):
                k, v = pairs.split('=')
                body[k] = v
        return body

