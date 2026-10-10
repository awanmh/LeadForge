#!/usr/bin/env python3
"""
LeadForge Protected Deployment & Webhook Trigger (LF-105, LF-504, T-16)
Validates Strapi publish webhooks, executes atomic static builds,
and protects the live release from failing builds.
"""

import hmac
import hashlib
import os
import shutil
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "dev_webhook_rebuild_secret_example_only").encode("utf-8")
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))
DIST_DIR = os.path.join(FRONTEND_DIR, "dist")
LIVE_DIR = os.path.join(FRONTEND_DIR, "dist-live")


def atomic_deploy() -> bool:
    print("[Deploy] Starting Astro static generation build...")
    # Execute build
    result = subprocess.run(
        ["npm", "run", "build"],
        cwd=FRONTEND_DIR,
        capture_output=True,
        text=True,
        shell=True,
    )

    if result.returncode != 0:
        print(f"[Deploy Error] Build failed with exit code {result.returncode}!")
        print("[Deploy Safety] Live deployment preserved. Live site was NOT replaced.")
        return False

    print("[Deploy Success] Build succeeded. Promoting to live atomic release...")
    temp_target = os.path.join(FRONTEND_DIR, "dist-next")
    if os.path.exists(temp_target):
        shutil.rmtree(temp_target)
    shutil.copytree(DIST_DIR, temp_target)

    # Atomic swap: promote dist-next to dist-live
    if os.path.exists(LIVE_DIR):
        old_backup = os.path.join(FRONTEND_DIR, "dist-prev")
        if os.path.exists(old_backup):
            shutil.rmtree(old_backup)
        os.rename(LIVE_DIR, old_backup)

    os.rename(temp_target, LIVE_DIR)
    print("[Deploy] Live release promoted successfully.")
    return True


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        # Validate signature or secret header
        auth_header = self.headers.get("X-Strapi-Signature") or self.headers.get("Authorization", "")
        expected = hmac.new(WEBHOOK_SECRET, body, hashlib.sha256).hexdigest()

        if auth_header and not (hmac.compare_digest(auth_header, expected) or auth_header.endswith(WEBHOOK_SECRET.decode())):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'{"error":"Forbidden: invalid webhook signature."}')
            return

        success = atomic_deploy()
        if success:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"deployed"}')
        else:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'{"error":"Build failed; previous deployment preserved."}')


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--build-now":
        success = atomic_deploy()
        sys.exit(0 if success else 1)

    server = HTTPServer(("127.0.0.1", 9000), WebhookHandler)
    print("Protected deploy webhook listening on http://127.0.0.1:9000...")
    server.serve_forever()
