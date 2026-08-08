#!/usr/bin/env python3
"""
db.py - SQLite layer for the AI Escape Log.

The canonical dataset is data/incidents.json. This module mirrors it into a
SQLite DB (data/incidents.db) so the data can be queried with SQL, exposed via
the CLI and the API. If the DB is missing or stale, it rebuilds from the JSON.

Zero-dependency: uses only the stdlib (sqlite3, json, os).
"""
import json
import os
import sqlite3
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
JSON_PATH = os.path.join(DATA_DIR, "incidents.json")
DB_PATH = os.path.join(DATA_DIR, "incidents.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS incidents (
    id TEXT PRIMARY KEY,
    date TEXT,
    lab TEXT,
    model TEXT,
    category TEXT,
    incident_type TEXT,
    title TEXT,
    url TEXT,
    source TEXT,
    summary TEXT,
    status TEXT,
    tags TEXT,
    updated_at TEXT
);
"""


def _now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def load_json():
    with open(JSON_PATH, encoding="utf-8") as f:
        return json.load(f)


def sync(force=False):
    """Rebuild the DB from JSON. Returns (rows_written, db_path)."""
    if os.path.exists(DB_PATH) and not force:
        # rebuild every time for simplicity & correctness on a tiny dataset
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(SCHEMA)
    rows = load_json()
    now = _now()
    for r in rows:
        conn.execute(
            "INSERT OR REPLACE INTO incidents "
            "(id,date,lab,model,category,incident_type,title,url,source,summary,status,tags,updated_at) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                r.get("id"),
                r.get("date"),
                r.get("lab"),
                r.get("model"),
                r.get("category"),
                r.get("incident_type"),
                r.get("title"),
                r.get("url"),
                r.get("source"),
                r.get("summary"),
                r.get("status"),
                ";".join(r.get("tags", []) or []),
                now,
            ),
        )
    conn.commit()
    conn.close()
    return len(rows), DB_PATH


def get_conn():
    if not os.path.exists(DB_PATH):
        sync()
    return sqlite3.connect(DB_PATH)


def query(sql, params=()):
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def all_incidents():
    return query("SELECT * FROM incidents ORDER BY date DESC")


def stats():
    rows = all_incidents()
    labs = {}
    cats = {}
    for r in rows:
        labs[r["lab"]] = labs.get(r["lab"], 0) + 1
        cats[r["category"]] = cats.get(r["category"], 0) + 1
    latest = max((r["date"] for r in rows if r["date"]), default=None)
    return {
        "total": len(rows),
        "labs": labs,
        "categories": cats,
        "latest_date": latest,
    }


if __name__ == "__main__":
    n, p = sync()
    print(f"Synced {n} incidents -> {p}")
