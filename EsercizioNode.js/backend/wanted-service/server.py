from datetime import date
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import mimetypes
import os
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from utils.converter import item_to_json

FBI_API_URL = "https://api.fbi.gov/wanted/v1/list"
PORT = int(os.environ.get("WANTED_PORT", "3002"))
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
PUBLIC_DIR = FRONTEND_DIR / "public"
FBI_PAGE = FRONTEND_DIR / "fbi.html"


def get_daily_item():
    # User-Agent identifica il servizio; Accept dichiara che vogliamo dati JSON.
    request = Request(FBI_API_URL,
        headers={
            "Accept": "application/json",
            "User-Agent": "FBI-Wanted-Daily-Service/1.0",
        },
    )

    try:
        # timeout evita di lasciare la richiesta bloccata se l'API non risponde.
        with urlopen(request, timeout=10) as response:
            payload = json.load(response)
    except (URLError, OSError, ValueError) as error:
        raise RuntimeError("Impossibile contattare l'API FBI.") from error

    # API restituisce le schede nella proprietà "items".
    items = payload.get("items") if isinstance(payload, dict) else None

    if not isinstance(items, list):
        raise RuntimeError("La risposta dell'API FBI non contiene una lista valida.")
    valid_items = [item for item in items if isinstance(item, dict)]
    # persona ricercata e non catturata (more funny).
    wanted_items = [
        item
        for item in valid_items
        if str(item.get("poster_classification", "")).lower() == "wanted"
        and str(item.get("status", "")).lower() != "captured"
    ]
    # se non ne troviamo, usiamo una scheda disponibile qualsiasi.
    candidates = wanted_items or valid_items
    if not candidates:
        raise RuntimeError("L'API FBI non ha restituito schede disponibili.")

    # La data fa si che tutti vedano la stessa scheda durante il giorno.
    return candidates[(date.today().toordinal() - 1) % len(candidates)]


class WantedHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # server usa la cartella pubblica del frontend per pagina, CSS e JavaScript.
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def send_content(self, content, content_type, status=200):
        # Content-Type dice al browser come interpretare la risposta.
        encoded = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def send_file(self, file_path, status=200):
        try:
            with open(file_path, "rb") as file:
                payload = file.read()
        except FileNotFoundError:
            self.send_error(404, "File not found")
            return

        mime_type, _ = mimetypes.guess_type(str(file_path))
        if not mime_type:
            mime_type = "application/octet-stream"

        self.send_response(status)
        self.send_header("Content-Type", mime_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        path = urlparse(self.path).path

        if path in ("/", "/api/v1", "/api/v1/") or path in ("/api/v1/fbi.html", "/wanted", "/api/v1/wanted", "/api/v1/wanted/"):
            self.send_file(FBI_PAGE)
            return

        if path == "/api/v1/wanted/today":
            try:
                person = item_to_json(get_daily_item())
            except RuntimeError as error:
                print(f"Errore API FBI: {error}", flush=True)
                body = json.dumps({"error": str(error)}, ensure_ascii=False)
                self.send_content(body, "application/json; charset=utf-8", 502)
                return

            body = json.dumps(person, ensure_ascii=False)
            self.send_content(body, "application/json; charset=utf-8")
            return

        if path.startswith("/api/v1/"):
            relative = path[len("/api/v1") :]
            target = PUBLIC_DIR / relative.lstrip("/")
            if target.is_file():
                self.send_file(target)
                return
            self.send_error(404, "File not found")
            return

        if path.startswith("/"):
            candidate = PUBLIC_DIR / path.lstrip("/")
            if candidate.is_file():
                self.send_file(candidate)
                return

        super().do_GET()


if __name__ == "__main__":
    print(f"Wanted service avviato su http://localhost:{PORT}", flush=True)
    # HTTPServer resta in ascolto e passa ogni richiesta al gestore qui sopra.
    HTTPServer(("0.0.0.0", PORT), WantedHandler).serve_forever()