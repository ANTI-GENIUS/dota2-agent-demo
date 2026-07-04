from __future__ import annotations

import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from agent import Dota2DraftAgent
from tools import build_hero_index, display_hero_name, display_role_name


ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / "static"
DATA_DIR = ROOT / "data"
AGENT = Dota2DraftAgent(DATA_DIR)


class Dota2AgentHandler(BaseHTTPRequestHandler):
    server_version = "Dota2AgentDemo/1.0"

    def do_GET(self) -> None:
        path = unquote(urlparse(self.path).path)
        if path == "/":
            self._send_file(STATIC_DIR / "index.html")
            return
        if path == "/api/heroes":
            self._send_json(self._hero_list())
            return
        if path == "/healthz":
            self._send_json({"status": "ok"})
            return
        if path.startswith("/static/"):
            self._send_file(STATIC_DIR / path.replace("/static/", "", 1))
            return
        self._send_error(404, "Not found")

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path != "/api/analyze":
            self._send_error(404, "Not found")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode("utf-8")
            payload = json.loads(body) if body else {}
            result = AGENT.run(payload)
            self._send_json(result)
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON body")
        except Exception as exc:  # noqa: BLE001 - demo server should surface failures as JSON.
            self._send_error(500, f"Agent error: {exc}")

    def _hero_list(self) -> list[dict[str, str]]:
        heroes = AGENT.client.get_hero_stats()
        hero_index = build_hero_index(heroes)
        indexed_ids = {
            int(hero["id"])
            for hero in hero_index.values()
            if hero.get("id") is not None
        }
        unique = [hero for hero in heroes if int(hero.get("id") or 0) in indexed_ids]
        unique.sort(key=display_hero_name)
        return [
            {
                "id": str(hero.get("id")),
                "name": display_hero_name(hero),
                "english_name": str(hero.get("localized_name", "")),
                "roles": ", ".join(display_role_name(role) for role in hero.get("roles", [])),
            }
            for hero in unique
        ]

    def _send_file(self, path: Path) -> None:
        path = path.resolve()
        if not str(path).startswith(str(STATIC_DIR.resolve())) or not path.exists() or not path.is_file():
            self._send_error(404, "File not found")
            return

        content_type, _ = mimetypes.guess_type(str(path))
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type or "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, data: object, status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, status: int, message: str) -> None:
        self._send_json({"error": message}, status=status)

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"[server] {self.address_string()} - {fmt % args}")


def run(host: str | None = None, port: int | None = None) -> None:
    port = port or int(os.environ.get("PORT", "8770"))
    host = host or os.environ.get("HOST") or ("0.0.0.0" if os.environ.get("PORT") else "127.0.0.1")
    server = ThreadingHTTPServer((host, port), Dota2AgentHandler)
    print(f"Dota2 Draft Agent running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
