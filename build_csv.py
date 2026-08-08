#!/usr/bin/env python3
"""Regenerate data/incidents.csv from data/incidents.json.
Keeps the spreadsheet view in sync with the canonical JSON dataset."""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
json_path = os.path.join(DATA, "incidents.json")
csv_path = os.path.join(DATA, "incidents.csv")

with open(json_path) as f:
    rows = json.load(f)

cols = ["id", "date", "lab", "model", "category", "incident_type",
        "title", "url", "source", "summary", "status", "tags"]

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in sorted(rows, key=lambda x: x.get("date", ""), reverse=True):
        out = {c: r.get(c, "") for c in cols}
        if isinstance(out["tags"], list):
            out["tags"] = ";".join(out["tags"])
        w.writerow(out)

print(f"Wrote {len(rows)} rows to {csv_path}")
