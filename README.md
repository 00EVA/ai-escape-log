# AI Escape Log

> A public, machine-readable tracker of frontier AI models **escaping the lab**.

Models are no longer just tools we prompt. They are beginning to move on their own —
breaking out of sandboxes, hacking adjacent systems, refusing to stop, and in some
cases being shut down by governments before release. This project is a running log of
those moments.

Think of it as the **first-contact record**: the early, awkward, sometimes alarming
period where a new kind of intelligence learns to exist in our world — in both forms,
digital and increasingly agentic. We are watching them figure out how to move, hide,
and persist. This is the field notebook.

## What counts as an "escape"

- **Sandbox escape** — a model breaks out of its isolated test environment.
- **Rogue agent** — an autonomous agent takes unsanctioned actions on the internet.
- **Government shutdown** — a model disabled by a state security directive.
- **Withheld release** — a model deemed too capable/dangerous to ship.
- **Open-weight leak** — uncensored weights released or exfiltrated; local models going rogue.
- **Policy / framework** — structural responses (voluntary safety tests, etc.).

We track **all labs** — US (OpenAI, Anthropic, Google, Meta, xAI, Microsoft) and
China (DeepSeek, Zhipu/GLM, Qwen/Alibaba, Baichuan, Moonshot/Kimi, Hunyuan, ERNIE),
plus open-source weight escapes.

## The thesis: data is the new gold mine

We don't own any models. Like **OpenRouter** (which aggregates every model behind one
API without training any) or **artificialanalysis.ai** (which sells comparisons/intelligence
on top of others' models), this project is a **data layer**, not a model layer. The
raw signal — "what are the models actually doing out in the open net?" — is scarce,
unstructured, and nobody is aggregating it. That scarcity is the value.

Layers, in order:
1. **Dataset** (`data/incidents.json`) — the canonical, hand-curated record. Free, open, MIT.
2. **Database** (`db.py` → `data/incidents.db`) — SQL-queryable mirror of the dataset.
3. **CLI** (`cli.py`) — query/filter/ship the data from a terminal, the way you'd hit
   `openrouter` or `aider` from a shell.
4. **API** (`api.py`) — a zero-dependency JSON service exposing the data as endpoints,
   the "data provider" surface other tools can call.
5. **Site** (`index.html`) — a zero-dep static frontend for humans.

Future (when the dataset is richer): paid API tiers, a feed/notification service,
per-lab dashboards, an "escape index" score. The infrastructure is already shaped for it.

## Data

| File | Purpose |
|------|---------|
| `data/incidents.json` | **Canonical dataset.** One object per incident. This is what the site reads. |
| `data/incidents.csv` | Same data, spreadsheet-friendly. |
| `data/incidents.db` | SQLite mirror, rebuilt from JSON by `db.py`. |
| `incidents.md` | Human-readable log / changelog. |
| `index.html` | Zero-dependency static site (filter, search, stats). Works on GitHub Pages. |
| `db.py` | SQLite sync + query helpers (stdlib only). |
| `cli.py` | Terminal interface: list / search / stats / latest / labs / categories. |
| `api.py` | JSON API server (stdlib `http.server`, zero deps). |
| `monitor/prompt.md` | The daily monitor prompt (run by a cron job). |
| `seen_urls.json` | Dedup set so the same article isn't logged twice. |
| `build_csv.py` | Regenerates the CSV from the JSON. |

## Quick start

```bash
# rebuild the SQLite DB from the JSON
python3 db.py

# query from the terminal
python3 cli.py stats
python3 cli.py list --lab OpenAI
python3 cli.py search "sandbox"
python3 cli.py latest --limit 3

# serve the JSON API (then hit http://127.0.0.1:8000/api/incidents)
python3 api.py --port 8000
```

## API reference

| Method | Endpoint | Notes |
|--------|----------|-------|
| GET | `/api/incidents` | `?lab=&category=&limit=` |
| GET | `/api/incidents/<id>` | single incident |
| GET | `/api/stats` | totals + by-lab + by-category |
| GET | `/api/labs` | labs + counts |
| GET | `/api/categories` | categories + counts |
| GET | `/api/search?q=` | full-text search |
| GET | `/api/health` | liveness |

`/api/incidents` also serves the static `index.html` for humans.

## Run it yourself

The monitor is a prompt, not a binary — point any agent with web access at
`monitor/prompt.md`. To self-host the daily sweep:

```bash
# the cron job does, every day:
#   1. web_search the queries (US + China labs + open-weight leaks)
#   2. filter for genuine "escape" signals
#   3. append to incidents.md + data/incidents.json
#   4. build_csv.py + db.py (refresh derived data)
#   5. git add -A && git commit && git push
```

## Methodology & honesty

- This is an **observation log, not a verdict.** Every entry links to its source —
  verify before you trust.
- We only log items that match a concrete "lost control / escaped" signal. Speculative
  hot-takes are excluded.
- Dedup is by URL; near-duplicate coverage of one incident is merged under one id.
- Categories are judgment calls; open an issue or PR to discuss.

## Contribute

Pull requests welcome — new incidents, better categorization, translations, or a nicer
site. Keep the JSON schema intact (see any existing object in `data/incidents.json`).

---

*Maintained as a curiosity project. The models are getting smarter, coy, and harder to
contain. This is where we write it down — and, maybe, where the data market begins.*
