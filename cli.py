#!/usr/bin/env python3
"""
cli.py - The AI Escape Log CLI.

A small, zero-dependency command-line interface over the incident dataset.
Think of it as the `openrouter`/`artificialanalysis` equivalent for "models
escaping the lab" data: a lean surface that aggregates, filters, and ships
structured incident data.

Usage:
    python3 cli.py list [--lab LAB] [--category CAT] [--limit N]
    python3 cli.py search "query"
    python3 cli.py stats
    python3 cli.py latest [--limit N]
    python3 cli.py labs
    python3 cli.py categories

Run `python3 cli.py --help` for details.
"""
import argparse
import json
import sys
import os

# allow running from anywhere
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db


def _print_table(rows, fields=("date", "lab", "model", "title")):
    for r in rows:
        line = " | ".join(str(r.get(f, "")) for f in fields)
        print(line)


def cmd_list(args):
    sql = "SELECT * FROM incidents"
    conds, params = [], []
    if args.lab:
        conds.append("lab = ?"); params.append(args.lab)
    if args.category:
        conds.append("category = ?"); params.append(args.category)
    if conds:
        sql += " WHERE " + " AND ".join(conds)
    sql += " ORDER BY date DESC"
    if args.limit:
        sql += f" LIMIT {int(args.limit)}"
    rows = db.query(sql, params)
    _print_table(rows)
    print(f"\n{len(rows)} incident(s).")


def cmd_search(args):
    q = args.query
    rows = db.query(
        "SELECT * FROM incidents WHERE "
        "lower(lab||' '||model||' '||title||' '||summary||' '||source||' '||tags||' '||incident_type) "
        "LIKE ? ORDER BY date DESC",
        (f"%{q.lower()}%",),
    )
    _print_table(rows)
    print(f"\n{len(rows)} match(es) for '{q}'.")


def cmd_stats(args):
    s = db.stats()
    print(f"Total incidents : {s['total']}")
    print(f"Latest         : {s['latest_date']}")
    print("\nBy lab:")
    for k, v in sorted(s["labs"].items(), key=lambda x: -x[1]):
        print(f"  {v:3}  {k}")
    print("\nBy category:")
    for k, v in sorted(s["categories"].items(), key=lambda x: -x[1]):
        print(f"  {v:3}  {k}")


def cmd_latest(args):
    rows = db.query("SELECT * FROM incidents ORDER BY date DESC LIMIT ?", (args.limit or 5,))
    for r in rows:
        print(f"- {r['date']} | {r['lab']} | {r['title']}\n  {r['url']}")


def cmd_labs(args):
    rows = db.query(
        "SELECT lab, COUNT(*) c FROM incidents GROUP BY lab ORDER BY c DESC"
    )
    for r in rows:
        print(f"{r['c']:3}  {r['lab']}")


def cmd_categories(args):
    rows = db.query(
        "SELECT category, COUNT(*) c FROM incidents GROUP BY category ORDER BY c DESC"
    )
    for r in rows:
        print(f"{r['c']:3}  {r['category']}")


def build():
    p = argparse.ArgumentParser(
        prog="cli.py",
        description="AI Escape Log CLI - aggregate, filter, and ship AI 'escape' incident data.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list", help="List incidents (optionally filtered).")
    pl.add_argument("--lab", help="Filter by lab.")
    pl.add_argument("--category", help="Filter by category.")
    pl.add_argument("--limit", type=int, help="Max rows.")
    pl.set_defaults(func=cmd_list)

    ps = sub.add_parser("search", help="Full-text search across all fields.")
    ps.add_argument("query", help="Search term.")
    ps.set_defaults(func=cmd_search)

    sub.add_parser("stats", help="Show totals, by-lab and by-category counts.").set_defaults(func=cmd_stats)

    pl2 = sub.add_parser("latest", help="Show most recent incidents.")
    pl2.add_argument("--limit", type=int, default=5, help="How many (default 5).")
    pl2.set_defaults(func=cmd_latest)

    sub.add_parser("labs", help="List labs and counts.").set_defaults(func=cmd_labs)
    sub.add_parser("categories", help="List categories and counts.").set_defaults(func=cmd_categories)

    return p


def main(argv=None):
    parser = build()
    args = parser.parse_args(argv)
    db.sync()  # ensure DB fresh
    args.func(args)


if __name__ == "__main__":
    main()
