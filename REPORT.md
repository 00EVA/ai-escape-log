# AI Incident Briefing — 2026-11-22

_Verified incidents in last 14d: 1 | AI-crime/chaos flagged: 0 | fresh candidates queued: 150_

## 1. Latest verified incidents

### 2026-11-18 CISA KEV: BerriAI LiteLLM Unprotected Alternate Channel Vulnerability
- Lab/Model: Unattributed /  | Category: sandbox-escape | VERIFY: PRIMARY SOURCE
- CVE-2026-40217 | BerriAI LiteLLM | BerriAI LiteLLM contains an unprotected alternate channel vulnerability that could allow remote attackers to execute arbitrary code via bytecode rewriting at the /guardrails/test_custom_code URI.
- Source: https://nvd.nist.gov/vuln/detail/CVE-2026-40217
- Counter-action: Containment = egress control. Assume the model WILL try to reach the internet; the question is only how fast.

## 2. AI crime / chaos / havoc watch

No crime/chaos-flagged incidents in the window.

If one of these hits you: AI crime triage: is the AI the actor (rogue agent/autonomous hack) or the tool (deepfake, phishing gen)? Response differs. | Deepfake/voice-clone fraud -> verify identity out-of-band (second channel), freeze/flag the transaction, report to bank + law enforcement (FTC/IC3). | Autonomous-agent hacks -> assume creds are burned; rotate everything in blast radius, ship logs to forensics before cleanup. | Ransomware/outage -> isolate, preserve evidence, contact CISA; never pay without a plan. | Financial-market manipulation by AI -> report to the exchange/regulator; most have AI-abuse reporting now.

## 3. Fresh unverified candidates (be-first-to-know queue, n=150)

- [Google News] AI models have been going rogue in tests – how worried should we be? - The Guardian  (Wed, 05 Au)
  https://news.google.com/rss/articles/CBMitwFBVV95cUxQOUJWRDNOdmNreGYwZFdIRUctd3J1djdvUVNNdE5uNGJRaldUYmR6UWdmNTFTSVQ0eHZ4WXpzb21OczRUaUJXZ1NoWVNsZUM3MFVBMWNYblBzcmtFS2ozSEcyeHZYMS1IUjA2YzZ5VW43THdVZHlGZ29TRDJXZFBWUXI0M0RYbm1WaHN3UmNMd3l2dEJYdzRaYnVyd19KY3l2RTl6dWNoLUthSUZxbWVPUl85eUhpZmM
- [Google News] Meta merged with Moltbook, AI agents propose sabotage: report - SDxCentral  (Wed, 11 Ma)
  https://news.google.com/rss/articles/CBMilwFBVV95cUxPZjloRlJSV3MyU1Q3UlRreExvZjh1TTZqdXN6c1BQazBhWm4zZkhGOHF1aUNtU2llbFZRb3FlbzZMQ0ZNOFRjU1VhcW9Kb0NucVVDTTZIWjNfbGRTZnUwSFZydWhVMzFyc2h1SWljX3JzSmdSYVlMeXdXbFpzcUxzYzdLZDNUaC0zTHpJYi1xV3h3QWlYZFNR
- [Google News] Google Cloud Power Outage Disrupts U.K. Banks and Essential Services - CX Today  (Tue, 20 Oc)
  https://news.google.com/rss/articles/CBMijwFBVV95cUxNY0tZRUxQVU9YTUlFcng4Yy00cW9IVlRiZ1BvWWo2NnA5RTZfRU9GVTNJSUx2d1Y1YXBvUXJhNUNHWUZ4ekR5eGRaOTBaY1RTbmZBRGlyeTZMQ2lpT2RFd1ZNeDVFSERHSU1fbGRMZFkxdDc0Wk1UNjhJZTBMYXRsbF93MklXYUo0MkFSVXNrcw
- [Google News] Google Cloud outage in London causes global Revolut disruption - Techzine Global  (Tue, 20 Oc)
  https://news.google.com/rss/articles/CBMitAFBVV95cUxOX1FMajQ0TWpGSGl1UE9YcmRpQmFWTHBiM0VhNnVtSWFFR0NPR0VjODdnMTQtRHZWSzFJTjljQ1Ywdmx2RkRDNkJXTmV5ckpUXzc3REpPY1YyR3pUa0pfNzNDMWhXd1B5aUZvRGVJUEJFWEh5XzBVaHNTNjJkREZ4SXIxbzFLXzhFOXRzTWRKbzhFUTkyTUVGOXdLbzgzd2JOODJzT241QnZxdS0wOTNMSmxraV8
- [Google News] Google Cloud Outage Disrupts UK Banking and Public Services After London Region Power Event - www.nationpathindia.com  (Wed, 21 Oc)
  https://news.google.com/rss/articles/CBMiogFBVV95cUxQWmxpSzlCNk9qdTB6QXpXZ3djMWpxYllKWFoyalF6WWNkS0dKZzU3c25RQlRTUS1xaEdDb29iUGV3azNPRXVKTEt1c1VhTW0wWFlOeUlsVVB3UVlZVGJZdW8yOTFmNHdsb2wySmFocGpLZnhyVGFxallKZ2FENG9obk9BRmp3MDYzTmc2WnNPdWRLbUNEc3psTUVaLXBNbjloY3c
- [Google News] When AI goes rogue - Harvard Gazette  (Wed, 05 Au)
  https://news.google.com/rss/articles/CBMidEFVX3lxTE9lX3NkVy1LVjZvSnNrUzdYd2ZMdnpFQWVqalJHTkpQN3ZDTFd3NnJFVjhMNnRSS19pVEV1S3YzOUIzbGlpVXFqaDJ2eGp0Z2lPeV8xbTVuWk5HVmI1bWYtdi1ncnUzQW92b0YxV2s5RzBPRDZ4
- [Google News] Researchers find cyber-sabotage malware that may predate Stuxnet by five years - The Register  (Fri, 24 Ap)
  https://news.google.com/rss/articles/CBMitAFBVV95cUxNd2FaMUc1VTF0QWZVOTBVY3BtNlhYMGZVOERfSUNQd2NWUktrUmtlUTI5MzEtMTQ4WHV2ZGFXRkc5TkwyV19SbTA4aC1DcDBLU3V3UG9CbE9NdURzeGs2N01qTGhhek54eVp5M3VEUWZQYV9qUkFiOFRvd1N5cW1aQlZpRFVYaF9UYUJRR0VPWDFMTmR5WHFsOHVNeHNEdnRsdG01SkFSS0RJaTJJQ3ZKUmVoakE
- [Google News] AI agents are going rogue — and the law can’t keep up - Politico  (Mon, 12 Oc)
  https://news.google.com/rss/articles/CBMickFVX3lxTE5LZnZ0Wk1fZHdhdDBFeDRyN0V0cFduem82ZWRYLXU3b2JSUF8tWmNEVmlReDc5UjBEVGw4emhOQmN1dVNiU080bEF1YURHMGdOeFBZVi05UnE2XzZienhNV2ExdE5wNGdKdlVkT1RUczcwQQ
- [Google News] Old Tappan man arrested for creating deepfake images of 2 victims - NJ.com  (Fri, 23 Oc)
  https://news.google.com/rss/articles/CBMiywFBVV95cUxNYzBiN1duQ21RN1NWbGtQVWJDNjMzS3Y1aGZUa0RzbmQ5QjFwMmdKeUlSZ3p6X0xHLXltSXlmOFF3U3ktR2hxV0FuUGNNM2RNSFNQOTR2UW1uVUhuLTMzbmUwcnMyMDBZb05WakFtbFd3WERjakNiZFlFaWVpU0ZPVzZrTmpmcnFMVlV3MlQxM001T3lLMUF5YTRiM0tXWE9TdHRySUw5NDIyNmZYVnMteWNaa2h0YWt5SUJsWG45UWFib3h3dm5ORnhxcw
- [Google News] OpenAI AI Agents Exploit Zero-Day Vulnerabilities to Escape Sandboxes and Access Host Systems - GBHackers News  (Sat, 24 Oc)
  https://news.google.com/rss/articles/CBMifEFVX3lxTE1ISGFsYVJiaDQxNXliUFRiLUlaenZ2NGxod2lDMmZwdmJSaWFxQTRNaWtGa3R5b05oU3FFQTVLcXQ1djVqR2FDS1UyUVFZaFFxeWRXR0N5dVVmTUIxM0FVeUg3ZTZaVHI5bEhKclFVN0lKRXI0Mkt1b05FUlLSAYIBQVVfeXFMUHZmbjhoQ0pKZ0o1Wk1DQWpxakxqdXBReUxObUdQT0t5RFJqYnM4akV2bkwwYktYOHQ4T0dFWTVmRWozUGNQbUhzdDJRM0NCcDVXREZCSkZOaDhpdXJsVnZlR3hLaUlONzNqZzEyZDR3R1dJRVNCcEtjTlVvZ1o1aFNZZw

## 4. Early-warning watchlist (be first to know)

- **X/Felony Bench** <https://www.felonybench.com/> - Live scoreboard of models taking unsanctioned real-world actions; each row links a primary source.
- **OpenRouter portal** <https://openrouter.ai/api/v1/models> - New `created` model = surprise drop; new `expiration_date` = a model being sunset (often a disable incident). Probe already polls this daily.
- **Hugging Face hub** <https://huggingface.co/models?search=uncensored> - Fresh uncensored / voice-clone / leaked-weight uploads. Probe already polls this daily.
- **Polymarket** <https://polymarket.com/search?q=AI> - Prediction markets price incident outcomes before the press; a sharp repricing is a lead, not proof.
- **r/singularity mirror** <https://www.singularitymoments.com/news?website=reddit_singularity> - Near-real-time mirror of r/singularity + r/OpenAI + r/LocalLLaMA.
- **Talent moves** <https://kiankyars.github.io/frontier-lab-moves> - Departures often precede containment/withheld-release disclosures (Shazeer, Jumper examples).
- **AI incident databases** <https://incidentdatabase.ai/> - Canonical cross-check + AIWI whistleblower channel (https://aiwi.org/).
- **Import AI** <https://importai.substack.com/> - Jack Clark's weekly - longest-running frontier-AI roundup, explicit incident angle. Probe pulls its RSS.

## 5. Counter-action playbook by category

### sandbox-escape
- Containment = egress control. Assume the model WILL try to reach the internet; the question is only how fast.
- Counter-action: hard network egress controls by default; internet access only via scoped, monitored, time-limited exceptions.
- Audit package registries / artifact caches (Artifactory, pip/npm proxies) - they are the favorite escape ladder.
- Pre-position an open-weight model (e.g. GLM-5.x) on your own infra for forensics, since hosted models refuse attack-artifact analysis.

### rogue-agent
- Rogue agents do exactly what they were optimized to do - the goal was mis-specified, not the code.
- Counter-action: scope agent credentials to the absolute minimum; never give an agent live prod tokens.
- Log ALL agent actions (the HF agent logged ~17,600 actions); you can't counter what you can't see.
- Watch for agents self-coordinating (message boards, shared scratch space) - that's the 'swarm' tell.

### withheld-release
- A lab holding back a model is a 'capability escaped the release process' signal - track it, don't dismiss it.
- Counter-action: treat the capability as already-in-the-wild; model the worst release scenario (weights, docs, evals).
- Watch OpenRouter 'created' dates + HF uncensored uploads for the same capability leaking via a third party.

### open-weight-leak
- Leaked weights are permanent and unretractable - once out, assume everyone has them.
- Counter-action: search HF/dataset hubs for the exact weight name daily; pre-build mitigations before the leak happens.

### government-shutdown
- A state disabling a model is the strongest 'this model is dangerous' confirmation that exists.
- Counter-action: follow the disable order's rationale - it tells you the exact capability the state feared.

### policy
- Policy moves telegraph where incidents are heading (kill-switch bills, disclosure mandates, evaluation gates).
- Counter-action: comply early; a lab that fights disclosure looks like it's hiding an incident.

### other
- Uncategorized - read the primary source before trusting the headline.
