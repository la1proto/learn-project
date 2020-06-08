import os
import socketserver
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime

now = datetime.now().year

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")

def get_n(qs):
    if qs == "":
        return "anonymouse"
    else:
        qs = parse_qs(qs)
        if "name" not in qs:
            return "anonymouse"
        else:
            return qs["name"][0]

def get_y(qs):
    if qs == "":
        return "X3"
    else:
        qs = parse_qs(qs)
        if "age" not in qs:
            return "X3"
        else:
            today = datetime.today().year
            return str(today - int(qs["age"][0]))


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
            if self.path.startswith("/hello"):
                path, qs = self.path.split("?") if "?" in self.path else [self.path,""]

                name = get_n(qs)
                year = get_y(qs)

                msg = f"""
                hello {name}!
                You were born in {year}
                Your path:  {self.path}
            """
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.send_header("Content-length", str(len(msg)))
                self.end_headers()
                self.wfile.write(msg.encode())
            else:
                return SimpleHTTPRequestHandler.do_GET(self)
        

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it" + " works")
    httpd.serve_forever()