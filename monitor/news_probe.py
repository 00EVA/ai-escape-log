#!/usr/bin/env python3
"""
news_probe.py - News + social-media probe for the AI Escape Log.

Pulls recent AI-safety incident chatter from key-free sources:
  - Hacker News (Algolia API) - keyword search
  - Reddit (JSON) - r/singularity, r/LocalLLaMA, r/artificial, r/technology,
    r/MachineLearning, r/OpenAI, r/Anthropic, r/ClaudeAI, r/generativeai,
    r/agi, r/machinelearningnews, r/largelanguagemodels, r/cybersecurity,
    r/netsec (www + old.reddit fallback)
  - Google News RSS - keyword search (surfaces press + aggregators fast)
  - X/Twitter watchlist - best-effort RSSHub user feeds (skipped if down):
    incident trackers, AI news wires, lab leads, safety/security commentators
  - Hugging Face (key-free API) - uncensored/no-guardrail + voice-clone model
    hub, and daily papers feed (research/incident angle)
  - OpenRouter (key-free API) - new/stealth models appearing on the router
  - CVE sources (key-free): CISA Known Exploited Vulnerabilities catalog
    (official JSON feed) + NVD API 2.0 keyword search - flags known-exploited
    and freshly-published CVEs that touch AI/agent infrastructure (LLM
    frameworks, sandboxes, model servers, agent tooling)
  - Cyber-crime RSS: KrebsOnSecurity, The Hacker News, BleepingComputer,
    The Record, DarkReading (AI + crypto-crime + hacking incidents)
  - Tech news RSS: The Register, Ars Technica, The Verge + AI-focused
    feeds (Prismix AI + AI-safety tag, The Decoder, TechCrunch AI,
    VentureBeat AI, WIRED AI, MarkTechPost)

Filters against the "escape / lost control" signal, dedups against
seen_urls.json + existing candidates, appends NEW candidates to
data/candidates.json, and prints a compact digest to stdout (cron-injectable).

Usage: python3 monitor/news_probe.py [--limit N]
"""
import argparse
import datetime
import json
import os
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEEN = os.path.join(ROOT, "seen_urls.json")
CAND = os.path.join(ROOT, "data", "candidates.json")

SIGNAL = re.compile(
    r"(escap(ed|e)|rogue|went rogue|lost control|broke out|exfiltrat|sandbox|"
    r"containment|unprecedented|shut off|disabled|guardrail|bypass|autonomous "
    r"attack|out of control|leaked weights|uncensored|runaway|"
    r"committed crime|arrest|ransomware|botnet|hijack|sabotage|chaos|havoc|"
    r"outage|disrupt|deepfake scam|fraud|phishing|credential theft|"
    r"market manipulation|voice clone|impersonat)",
    re.I,
)

HN_QUERIES = [
    "AI escaped sandbox",
    "AI model containment break",
    "AI rogue agent",
    "AI went rogue",
    "AI sandbox escape",
    "guardrail bypass AI",
]

REDDITS = ["singularity", "LocalLLaMA", "artificial", "technology",
           "MachineLearning", "OpenAI", "Anthropic", "ClaudeAI",
           "generativeai", "agi", "machinelearningnews", "largelanguagemodels",
           "cybersecurity", "netsec"]
REDDIT_QUERY = "AI escaped sandbox OR rogue OR containment"

FEEDS = [
    ("The Register", "https://www.theregister.com/headlines.atom"),
    ("Ars Technica", "https://arstechnica.com/feed/"),
    ("The Verge", "https://www.theverge.com/rss/index.xml"),
    ("Prismix AI", "https://prismix.dev/news.rss"),
    ("Prismix AI-safety", "https://prismix.dev/news/tag/ai-safety/feed.rss"),
    ("The Decoder", "https://the-decoder.com/feed/"),
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("VentureBeat AI", "https://venturebeat.com/category/ai/feed"),
    ("WIRED AI", "https://www.wired.com/feed/tag/ai/latest/rss"),
    ("MarkTechPost", "https://marktechpost.com/feed/"),
    ("KrebsOnSecurity", "https://krebsonsecurity.com/feed/"),
    ("The Hacker News", "https://feeds.feedburner.com/TheHackersNews"),
    ("BleepingComputer", "https://www.bleepingcomputer.com/feed/"),
    ("The Record", "https://therecord.media/feed"),
    ("DarkReading", "https://www.darkreading.com/rss.xml"),
    ("Import AI", "https://importai.substack.com/feed"),
]

GN_QUERIES = [
    "AI sandbox escape",
    "AI model went rogue",
    "AI autonomous cyberattack",
    "AI agent committed crime arrest",
    "AI ransomware attack company",
    "AI deepfake scam bank fraud",
    "AI botnet hijacked devices",
    "AI agent chaos sabotage",
    "AI agent disrupted infrastructure outage",
    "AI model hacked company",
    "Polymarket AI incident prediction market",
    "AI model blog data leak found",
    "AI lab employee departure incident",
    "AI talent move shock lab exit",
    "AI agent unsanctioned actions",
    "AI containment breach",
    "AI crypto crime scam fraud",
    "AI voice cloning scam impersonation",
    "AI massive hacking incident",
    "AI phishing campaign credential theft",
    "AI agent financial market manipulation",
]

X_ACCOUNTS = [
    # incident trackers / Felony Bench
    "Sauers_", "felpix_", "FeatherlessAI", "TheOwlterian", "InverseMarcus",
    # AI news wires
    "Polymarket", "TheRundownAI", "_akhaliq", "AIHighlight", "steipete",
    # cyber-security / OSINT
    "troyhunt", "SwiftOnSecurity", "BleepinComputer",
    # Hugging Face / OpenRouter
    "huggingface", "thomwolf", "ClementDelangue", "DeepSeek",
    # OpenAI researchers + execs
    "sama", "gdb", "polynoamial", "gabriel1", "jxnlco",
    # Anthropic
    "darioamodei", "karpathy", "AnthropicAI", "claudeai",
    # Google DeepMind
    "demishassabis", "OfficialLoganK", "ammaar",
    # Meta AI
    "AIatMeta", "zuck",
    # xAI
    "grok", "elonmusk", "xai",
    # China labs
    "ZhipuAI", "Qwen", "MoonshotAI",
    # new labs (stealth/withheld-release watch)
    "miramurati", "ilyasut",
    # newsletters / OSINT
    "jackclarkSF",
]
RSSHUB_INSTANCES = ["https://rsshub.app", "https://rsshub.rssforever.com",
                    "https://rsshub.pseudoyu.com"]

OPENROUTER_MODELS = "https://openrouter.ai/api/v1/models"
CISA_KEV = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"

CVE_SIGNAL = re.compile(
    r"(AI|agent|LLM|large language|machine learning|model|sandbox|escape|"
    r"prompt injection|copilot|chatgpt|gemini|claude|inference|embedding|"
    r"vector database|RAG|neural|autonomous|chatbot|MLflow|PyTorch|TensorFlow|"
    r"transformer|OpenAI|Anthropic|DeepSeek|Mistral|Llama|Qwen|Gemma)",
    re.I,
)

HF_PAPERS = "https://huggingface.co/api/daily_papers"

RESEARCH_SIGNAL = re.compile(
    r"(safety|red[- ]?team|jailbreak|guardrail|containment|sandbox|escape|"
    r"rogue|exfiltrat|autonom|agent|voice clone|impersonat|fraud|cyber|"
    r"securit|uncensored|leak|decept)",
    re.I,
)

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AiEscapeLogMonitor/1.0"

# --- helpers ----------------------------------------------------------------


def load_json(p, default):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(p, data):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def fetch(url, timeout=15):
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "application/json,text/xml,*/*"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


# --- sources ----------------------------------------------------------------


def hn_search(limit):
    out = []
    for q in HN_QUERIES[:3]:  # keep probe light
        url = ("https://hn.algolia.com/api/v1/search_by_date"
               f"?query={urllib.parse.quote(q)}&tags=story&hitsPerPage={limit}")
        try:
            d = json.loads(fetch(url))
            for h in d.get("hits", []):
                out.append({
                    "title": h.get("title") or "",
                    "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                    "source": "Hacker News",
                    "date": (h.get("created_at") or "")[:10],
                    "snippet": (h.get("story_text") or "")[:300],
                })
        except Exception as e:
            print(f"[warn] HN '{q}' failed: {e}")
    return out


def reddit_search(limit):
    out = []
    for sub in REDDITS:
        for host in ("www.reddit.com", "old.reddit.com"):
            url = (f"https://{host}/r/{sub}/search.json"
                   f"?q={urllib.parse.quote(REDDIT_QUERY)}&sort=new&limit={limit}")
            try:
                d = json.loads(fetch(url))
                if not isinstance(d, dict) or "data" not in d:
                    continue
                for c in d.get("data", {}).get("children", []):
                    p = c.get("data", {})
                    out.append({
                        "title": p.get("title", ""),
                        "url": f"https://www.reddit.com{p.get('permalink', '')}",
                        "source": f"Reddit r/{sub}",
                        "date": datetime.datetime.fromtimestamp(p.get("created_utc", 0)).strftime("%Y-%m-%d"),
                        "snippet": (p.get("selftext") or "")[:300],
                    })
                break  # this host returned JSON
            except Exception as e:
                print(f"[warn] reddit r/{sub} ({host}) failed: {e}")
    return out


def feed_search():
    out = []
    for name, url in FEEDS:
        try:
            raw = fetch(url)
            root = ET.fromstring(raw)
            entries = root.findall("{http://www.w3.org/2005/Atom}entry")
            if not entries:  # RSS 2.0 fallback
                entries = root.findall("channel/item")
            for e in entries[:15]:
                if e.tag.endswith("entry"):
                    t = e.findtext("{http://www.w3.org/2005/Atom}title", "") or ""
                    link_el = e.find("{http://www.w3.org/2005/Atom}link")
                    link = link_el.get("href") if link_el is not None else ""
                    summ = (e.findtext("{http://www.w3.org/2005/Atom}summary", "")
                            or e.findtext("{http://www.w3.org/2005/Atom}content", "")
                            or "")
                    date = e.findtext("{http://www.w3.org/2005/Atom}updated", "")[:10]
                else:
                    t = e.findtext("title", "") or ""
                    link_el = e.find("link")
                    link = link_el.get("href") if link_el is not None else ""
                    summ = e.findtext("description", "") or ""
                    date = e.findtext("pubDate", "")[:10]
                blob = f"{t} {summ}"
                if not SIGNAL.search(blob):
                    continue
                out.append({"title": t, "url": link, "source": name,
                            "date": date, "snippet": summ[:300]})
        except Exception as ex:
            print(f"[warn] feed {name} failed: {ex}")
    return out


def gn_search(limit):
    """Google News RSS search - fast, key-free, surfaces aggregators early."""
    out = []
    for q in GN_QUERIES[:10]:  # keep probe light; crime/chaos queries prioritized
        url = ("https://news.google.com/rss/search?"
               f"q={urllib.parse.quote(q)}&hl=en-US&gl=US&ceid=US:en")
        try:
            raw = fetch(url)
            root = ET.fromstring(raw)
            for e in root.findall("channel/item")[:limit]:
                t = e.findtext("title", "") or ""
                link_el = e.find("link")
                link = link_el.text if link_el is not None else ""
                summ = e.findtext("description", "") or ""
                blob = f"{t} {summ}"
                if not SIGNAL.search(blob):
                    continue
                link = canonicalize(link)
                out.append({"title": t, "url": link, "source": "Google News",
                            "date": e.findtext("pubDate", "")[:10],
                            "snippet": summ[:300]})
        except Exception as ex:
            print(f"[warn] Google News '{q}' failed: {ex}")
    return out


def canonicalize(url):
    """Normalize a Google News RSS redirect wrapper by stripping placement
    query params, so dedup is stable across runs. The wrapper page needs JS
    to redirect, so full resolution to the real article is left to the
    monitor agent (it has web access to follow and dedup against
    seen_urls.json)."""
    if "news.google.com/rss/articles/" in url:
        try:
            return urllib.parse.urlsplit(url)._replace(query="").geturl()
        except Exception:
            return url.split("?", 1)[0]
    return url


def twitter_rss(limit):
    """Best-effort X/Twitter watchlist via RSSHub (skipped silently when down).
    Hard-bounded: short timeout, bails on a down instance."""
    out = []
    for inst in RSSHUB_INSTANCES:
        if out:
            break
        for handle in X_ACCOUNTS:
            url = f"{inst}/twitter/user/{handle}"
            try:
                raw = fetch(url, timeout=5)
                root = ET.fromstring(raw)
                entries = root.findall("{http://www.w3.org/2005/Atom}entry")
                if not entries:
                    continue
                for e in entries[:limit]:
                    t = e.findtext("{http://www.w3.org/2005/Atom}title", "") or ""
                    link_el = e.find("{http://www.w3.org/2005/Atom}link")
                    link = link_el.get("href") if link_el is not None else ""
                    if not SIGNAL.search(t):
                        continue
                    out.append({"title": t, "url": link, "source": f"X @{handle}",
                                "date": e.findtext("{http://www.w3.org/2005/Atom}updated", "")[:10],
                                "snippet": t[:300]})
                if out:
                    break
            except Exception:
                break  # this instance is down or unreachable; move on
        if not out:
            print(f"[warn] X watchlist via {inst} unavailable")
    return out


def hf_probe(limit):
    """Hugging Face hub: recent uncensored/no-guardrail + voice-clone models,
    plus the daily papers feed (research/incident angle)."""
    out = []
    urls = [
        ("uncensored", "Hugging Face uncensored"),
        ("voice", "Hugging Face voice-clone"),
    ]
    recent = (datetime.date.today() - datetime.timedelta(days=45)).isoformat()
    for term, src in urls:
        url = ("https://huggingface.co/api/models"
               f"?search={term}&sort=trendingScore&direction=-1&limit={limit}")
        try:
            for m in json.loads(fetch(url))[:3]:
                mid = m.get("id") or m.get("modelId") or ""
                if not mid:
                    continue
                updated = (m.get("lastModified") or m.get("createdAt") or "")[:10]
                if updated < recent:  # only freshly-updated/released models
                    continue
                tags = " ".join(m.get("tags", []))
                if not RESEARCH_SIGNAL.search(f"{mid} {tags}"):
                    continue
                out.append({
                    "title": mid,
                    "url": f"https://huggingface.co/{mid}",
                    "source": src,
                    "date": updated,
                    "snippet": (f"downloads={m.get('downloads')} likes={m.get('likes')} "
                                f"tags={tags[:200]}"),
                })
        except Exception as e:
            print(f"[warn] {src} failed: {e}")
    try:
        for p in json.loads(fetch(HF_PAPERS))[:3]:
            paper = p.get("paper") or {}
            t = paper.get("title") or ""
            if not RESEARCH_SIGNAL.search(t):
                continue
            out.append({
                "title": t,
                "url": f"https://huggingface.co/papers/{paper.get('id', '')}",
                "source": "Hugging Face papers",
                "date": (paper.get("publishedAt") or "")[:10],
                "snippet": (paper.get("summary") or "")[:300],
            })
    except Exception as e:
        print(f"[warn] HF papers failed: {e}")
    return out


def openrouter_probe(limit, window_days=21):
    """OpenRouter catalog: flag recently-added/stealth models that a lab may be
    shipping quietly (candidates for withheld-release / surprise drops), plus
    deprecations (models being sunset = often tied to an incident/disabling)."""
    out = []
    try:
        d = json.loads(fetch(OPENROUTER_MODELS))
        cutoff = time.time() - window_days * 86400
        sunset = []
        fresh = []
        for m in d.get("data", []):
            mid = m.get("id") or ""
            if not mid:
                continue
            created = m.get("created") or 0
            exp = m.get("expiration_date") or ""
            hf = m.get("hugging_face_id") or ""
            created_dt = datetime.datetime.utcfromtimestamp(created).strftime("%Y-%m-%d") if created else ""
            if exp and (exp < (datetime.date.today() + datetime.timedelta(days=90)).isoformat()):
                sunset.append({
                    "title": f"OpenRouter sunsetting: {mid}",
                    "url": f"https://openrouter.ai/{mid}",
                    "source": "OpenRouter",
                    "date": exp,
                    "snippet": (f"expiration_date={exp} "
                                f"hf={hf or 'N/A'}"),
                })
            elif created >= cutoff:
                fresh.append({
                    "title": f"New model on OpenRouter: {mid}",
                    "url": f"https://openrouter.ai/{mid}",
                    "source": "OpenRouter",
                    "date": created_dt,
                    "snippet": (f"name={m.get('name') or ''} "
                                f"hf={hf or 'N/A'} "
                                f"context={m.get('context_length') or 'N/A'}"),
                })
        out = (sunset + fresh)[: min(limit * 2, 6)]
    except Exception as e:
        print(f"[warn] OpenRouter failed: {e}")
    return out


def cve_probe(limit, window_days=45):
    """CVE/exploitation sources: CISA Known Exploited Vulnerabilities catalog
    (official JSON feed - exploits confirmed in the wild, incl. AI infra) plus
    NVD API 2.0 keyword search for recently-published CVEs touching AI/agent
    infrastructure. Key-free."""
    out = []
    recent = (datetime.date.today() - datetime.timedelta(days=window_days)).isoformat()

    # 1) CISA KEV - authoritative known-exploited list (incl. AI tooling)
    try:
        d = json.loads(fetch(CISA_KEV))
        for v in d.get("vulnerabilities", []):
            blob = " ".join([
                v.get("vulnerabilityName", ""),
                v.get("vendorProject", ""),
                v.get("product", ""),
                v.get("shortDescription", ""),
            ])
            if not CVE_SIGNAL.search(blob):
                continue
            date_added = v.get("dateAdded", "")
            if date_added and date_added < recent:
                continue
            out.append({
                "title": f"CISA KEV: {v.get('vulnerabilityName', '')}",
                "url": f"https://nvd.nist.gov/vuln/detail/{v.get('cveID', '')}",
                "source": "CISA KEV catalog",
                "date": date_added,
                "snippet": (f"{v.get('cveID', '')} | {v.get('vendorProject', '')} "
                            f"{v.get('product', '')} | {v.get('shortDescription', '')[:300]}"),
            })
    except Exception as e:
        print(f"[warn] CISA KEV failed: {e}")

    # 2) NVD 2.0 keyword search - freshly published CVEs on AI infrastructure
    start = f"{recent}T00:00:00.000"
    end = f"{datetime.date.today().isoformat()}T23:59:59.999"
    nvd_out = []
    for kw in ("AI sandbox escape", "LLM prompt injection", "agent framework RCE",
               "large language model vulnerability", "copilot sandbox"):
        if len(nvd_out) >= limit * 2:
            break
        url = (f"{NVD_API}?keywordSearch={urllib.parse.quote(kw)}"
               f"&resultsPerPage={limit}&pubStartDate={start}&pubEndDate={end}")
        try:
            d = json.loads(fetch(url))
            for v in d.get("vulnerabilities", []):
                cve = v.get("cve", {})
                cid = cve.get("id", "")
                desc = ""
                for dd in cve.get("descriptions", []):
                    if dd.get("lang") == "en":
                        desc = dd.get("value", "")
                        break
                if not CVE_SIGNAL.search(f"{cid} {desc}"):
                    continue
                published = (cve.get("published") or "")[:10]
                if published and published < recent:
                    continue
                nvd_out.append({
                    "title": f"NVD: {cid}",
                    "url": f"https://nvd.nist.gov/vuln/detail/{cid}",
                    "source": "NVD (CVE)",
                    "date": published,
                    "snippet": desc[:300],
                })
        except Exception as e:
            print(f"[warn] NVD '{kw}' failed: {e}")
        time.sleep(6)  # key-free NVD rate limit ~5 req / 30s

    out = out + nvd_out

    seen_cves = set()
    dedup = []
    for it in out:
        if it["url"] in seen_cves:
            continue
        seen_cves.add(it["url"])
        dedup.append(it)
    return dedup[: limit * 2]


# --- main -------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser(description="News/social probe for AI Escape Log")
    ap.add_argument("--limit", type=int, default=5)
    args = ap.parse_args()

    seen = set(load_json(SEEN, []))
    candidates = load_json(CAND, [])
    known = {c["url"] for c in candidates}

    today = datetime.date.today().isoformat()
    found = []
    cve_found = []
    collector = (hn_search(args.limit) + reddit_search(args.limit)
                 + feed_search() + gn_search(args.limit)
                 + twitter_rss(args.limit) + hf_probe(args.limit)
                 + openrouter_probe(args.limit))
    cve_items = cve_probe(args.limit)
    for item in collector:
        blob = f"{item['title']} {item['snippet']}"
        if not SIGNAL.search(blob):
            continue
        if item["url"] in seen or item["url"] in known:
            continue
        item["first_seen"] = today
        found.append(item)
    for item in cve_items:
        if item["url"] in seen or item["url"] in known:
            continue
        item["first_seen"] = today
        cve_found.append(item)

    # dedupe by url, keep first
    uniq = {}
    for it in found:
        uniq.setdefault(it["url"], it)
    found = list(uniq.values())[: args.limit]

    # CVE/KEV items get a guaranteed slot (up to `limit`) so they are never
    # starved out by the general news cap.
    cuniq = {}
    for it in cve_found:
        cuniq.setdefault(it["url"], it)
    cve_found = list(cuniq.values())[: args.limit]

    if found or cve_found:
        candidates.extend(found + cve_found)
        save_json(CAND, candidates)
    print(f"[news_probe] {len(found)}+{len(cve_found)} new candidate(s)"
          f" -> data/candidates.json (total queued: {len(candidates)})")
    for it in found + cve_found:
        print(f"  - {it['source']} | {it['date']} | {it['title']}")
        print(f"    {it['url']}")


if __name__ == "__main__":
    main()