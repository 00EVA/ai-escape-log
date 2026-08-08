#!/usr/bin/env python3
"""
api.py - Minimal JSON API for the AI Escape Log.

A zero-dependency HTTP server (Python stdlib only) exposing the incident
dataset as a clean JSON API - the "data provider" layer analogous to how
OpenRouter / artificialanalysis.ai expose model & pricing data as a service
rather than owning the underlying models.

Endpoints:
    GET /api/incidents            -> list (query: ?lab=&category=&limit=)
    GET /api/incidents/<id>       -> one incident
    GET /api/stats                -> totals, by-lab, by-category
    GET /api/labs                 -> labs + counts
    GET /api/categories           -> categories + counts
    GET /api/search?q=<term>      -> full-text search
    GET /api/health               -> {ok:true}

Run:  python3 api.py [--port 8000]
"""
import argparse
import json
import sys
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))


def _send(handler, code, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(body)


def _rows_to_public(rows):
    out = []
    for r in rows:
        d = dict(r)
        d["tags"] = (d.get("tags") or "").split(";") if d.get("tags") else []
        out.append(d)
    return out


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass  # quiet

    def _dispatch(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path == "/api/health":
            return 200, {"ok": True}

        if path == "/api/incidents":
            sql = "SELECT * FROM incidents"
            conds, params = [], []
            if "lab" in qs:
                conds.append("lab = ?"); params.append(qs["lab"][0])
            if "category" in qs:
                conds.append("category = ?"); params.append(qs["category"][0])
            if conds:
                sql += " WHERE " + " AND ".join(conds)
            sql += " ORDER BY date DESC"
            if "limit" in qs:
                try:
                    sql += f" LIMIT {int(qs['limit'][0])}"
                except ValueError:
                    pass
            return 200, _rows_to_public(db.query(sql, params))

        if path.startswith("/api/incidents/"):
            inc_id = path[len("/api/incidents/"):]
            rows = db.query("SELECT * FROM incidents WHERE id = ?", (inc_id,))
            if not rows:
                return 404, {"error": "not found", "id": inc_id}
            return 200, _rows_to_public(rows)[0]

        if path == "/api/stats":
            return 200, db.stats()

        if path == "/api/labs":
            return 200, db.query(
                "SELECT lab, COUNT(*) c FROM incidents GROUP BY lab ORDER BY c DESC"
            )

        if path == "/api/categories":
            return 200, db.query(
                "SELECT category, COUNT(*) c FROM incidents GROUP BY category ORDER BY c DESC"
            )

        if path == "/api/search":
            q = (qs.get("q") or [""])[0].lower()
            if not q:
                return 400, {"error": "missing q"}
            rows = db.query(
                "SELECT * FROM incidents WHERE "
                "lower(lab||' '||model||' '||title||' '||summary||' '||source||' '||tags||' '||incident_type) "
                "LIKE ? ORDER BY date DESC",
                (f"%{q}%",),
            )
            return 200, _rows_to_public(rows)

        if path in ("/", "/index.html"):
            # serve the static site
            fp = os.path.join(STATIC_DIR, "index.html")
            if os.path.exists(fp):
                with open(fp, "rb") as f:
                    body = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return None, None
            return 404, {"error": "index.html not found"}

        return 404, {"error": "unknown endpoint", "path": path}

    def do_GET(self):
        db.sync()
        code, payload = self._dispatch()
        if code is None:
            return
        _send(self, code, payload)


def main():
    ap = argparse.ArgumentParser(description="AI Escape Log API server")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()
    db.sync()
    srv = HTTPServer((args.host, args.port), Handler)
    print(f"AI Escape Log API on http://{args.host}:{args.port}  (Ctrl-C to stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")


if __name__ == "__main__":
    main()
