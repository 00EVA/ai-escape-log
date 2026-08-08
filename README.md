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

## Data

| File | Purpose |
|------|---------|
| `data/incidents.json` | **Canonical dataset.** One object per incident. This is what the site reads. |
| `data/incidents.csv` | Same data, spreadsheet-friendly. |
| `incidents.md` | Human-readable log / changelog. |
| `index.html` | Zero-dependency static site (filter, search, stats). Works on GitHub Pages. |
| `monitor/prompt.md` | The daily monitor prompt (run by a cron job). |
| `seen_urls.json` | Dedup set so the same article isn't logged twice. |
| `build_csv.py` | Regenerates the CSV from the JSON. |

## Run it yourself

The monitor is a prompt, not a binary — point any agent with web access at
`monitor/prompt.md`. To self-host the daily sweep:

```bash
# the cron job does, every day:
#   1. web_search the 10 queries
#   2. filter for genuine "escape" signals
#   3. append to incidents.md + data/incidents.json
#   4. build_csv.py
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
contain. This is where we write it down.*
