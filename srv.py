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
        {bye(datetime.today().hour)}
        time: {datetime.today()}
            """

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

def page(query):
    path, qs = query.split("?") if '?' in query else [query,""]
    path = path.rstrip('/')

    switcher = {
        "/hello": page_hello,
        "/goodbye": page_goodbye,
    }

    return switcher[path](qs) if path in switcher else "X3 page"

def page_hello(qs):
    qs = parse_qs(qs) if qs != "" else ""
    name = get_n(qs)
    year = get_y(qs)
    return f"""
                    Hi {name}! 
                    You were born in {year}.
                """

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
            if self.path != "":
                msg = page(self.path)

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