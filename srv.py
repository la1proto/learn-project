import os
import socketserver
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime

now = datetime.now().year

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")

def message_bye(hour):
    if hour < 6:
        return "GoodNight.."
    elif hour < 12:
        return "GoodMorning.."
    elif hour < 18:
        return "Good Day.."
    elif hour < 23:
        return "Good Evening.."
    else:
        return "GoodNight.."

def page_goodbye(qs):
    return f"""
        {message_bye(datetime.today().hour)}
        time: {datetime.today()}
            """

def get_name(qs):
    if "name" in qs:
    	return qs["name"][0]
    else:
    	return "KTO Tbl?"

def get_year(qs):
    if "age" in qs:
    	today = datetime.today().year
    	age = int(qs["age"][0])
    	return str(today - age)
    else:
    	return "X3"

def page_hello(qs):
    if qs != "":
    	qs = parse_qs(qs)
    name = get_name(qs)
    year = get_year(qs)
    return f"""
    hi {name}
    you were born in {year}
    """

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path, qs = self.path.split("?") if '?' in self.path else [self.path, ""]
        path = path.rstrip('/')
        switcher = {"/hello": page_hello, "/goodbye": page_goodbye}
        if path in switcher:
            msg = switcher[path](qs)

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