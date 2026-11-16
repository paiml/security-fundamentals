"""A small orders site to practise security on. It only listens on this computer."""

import base64
import binascii
import json
import os
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

USERS = {"alice": "wonderland", "bob": "builder"}

SECURITY_TXT = Path(__file__).with_name("security.txt")

ORDERS = {
    1: {"id": 1, "owner": "alice", "item": "Notebook", "total": "4.50"},
    2: {"id": 2, "owner": "bob", "item": "Headphones", "total": "59.00"},
    3: {"id": 3, "owner": "alice", "item": "Desk lamp", "total": "22.00"},
}


class Handler(BaseHTTPRequestHandler):
    def version_string(self):
        return "OrdersSite"

    def do_GET(self):
        if self.path == "/health":
            return self.reply(200, {"status": "ok"})

        if self.path == "/.well-known/security.txt":
            return self.reply_text(200, SECURITY_TXT.read_text())

        user = self.signed_in_user()
        if user is None:
            return self.reply(401, {"error": "sign in first"})

        if self.path == "/orders":
            mine = [order for order in ORDERS.values() if order["owner"] == user]
            return self.reply(200, mine)

        if self.path.startswith("/orders/"):
            order = ORDERS.get(order_id(self.path))
            if order is None:
                return self.reply(404, {"error": "no such order"})
            return self.reply(200, order)

        self.reply(404, {"error": "no such page"})

    def signed_in_user(self):
        """The user name from the sign-in header, if the password matches."""
        header = self.headers.get("Authorization", "")
        if not header.startswith("Basic "):
            return None
        try:
            name, _, password = base64.b64decode(header[6:]).decode().partition(":")
        except (binascii.Error, UnicodeDecodeError):
            return None
        return name if USERS.get(name) == password else None

    def reply(self, status, body):
        data = (json.dumps(body, indent=2) + "\n").encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        if status == 401:
            self.send_header("WWW-Authenticate", 'Basic realm="orders"')
        self.end_headers()
        self.wfile.write(data)

    def reply_text(self, status, text):
        data = text.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        pass  # requests are not printed, so they don't mix with your commands


def order_id(path):
    """The number at the end of /orders/<number>, or None."""
    number = path.removeprefix("/orders/")
    return int(number) if number.isdigit() else None


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
