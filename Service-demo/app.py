import json
import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

HOSTNAME = socket.gethostname()
SERVICE_TYPE = os.getenv("SERVICE_TYPE", "Unknown")
APP_NAME = os.getenv("APP_NAME", "service-demo")
NAMESPACE = os.getenv("NAMESPACE", "default")

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{app_name}</title>
    <style>
      body {{
        font-family: Arial, sans-serif;
        background: linear-gradient(135deg, #eef7ff, #f7f9ff);
        margin: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
      }}
      .card {{
        width: min(720px, 90vw);
        background: white;
        border-radius: 18px;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.12);
        padding: 32px;
      }}
      .badge {{
        display: inline-block;
        background: #2563eb;
        color: white;
        padding: 8px 14px;
        border-radius: 999px;
        font-size: 14px;
        font-weight: bold;
      }}
      h1 {{
        margin: 20px 0 10px;
        color: #111827;
      }}
      .grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
        margin-top: 22px;
      }}
      .item {{
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px;
      }}
      .label {{
        color: #64748b;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
      }}
      .value {{
        margin-top: 8px;
        color: #0f172a;
        font-weight: bold;
        font-size: 18px;
      }}
    </style>
  </head>
  <body>
    <div class="card">
      <div class="badge">Kubernetes Service Demo</div>
      <h1>{app_name}</h1>
      <p>This pod is serving traffic for the <strong>{service_type}</strong> service type.</p>
      <div class="grid">
        <div class="item">
          <div class="label">Service type</div>
          <div class="value">{service_type}</div>
        </div>
        <div class="item">
          <div class="label">Pod name</div>
          <div class="value">{hostname}</div>
        </div>
        <div class="item">
          <div class="label">Namespace</div>
          <div class="value">{namespace}</div>
        </div>
      </div>
    </div>
  </body>
</html>
"""


class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/healthz":
            payload = {
                "status": "ok",
                "serviceType": SERVICE_TYPE,
                "appName": APP_NAME,
                "hostname": HOSTNAME,
                "namespace": NAMESPACE,
            }
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        body = HTML_TEMPLATE.format(
            app_name=APP_NAME,
            service_type=SERVICE_TYPE,
            hostname=HOSTNAME,
            namespace=NAMESPACE,
        ).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), DemoHandler)
    print(f"Service demo running on 0.0.0.0:8000 for {SERVICE_TYPE}")
    server.serve_forever()
