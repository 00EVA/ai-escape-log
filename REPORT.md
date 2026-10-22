# AI Incident Briefing — 2026-10-22

_Verified incidents in last 14d: 0 | AI-crime/chaos flagged: 0 | fresh candidates queued: 314_

## 1. Latest verified incidents

None in the window.
## 2. AI crime / chaos / havoc watch

No crime/chaos-flagged incidents in the window.

If one of these hits you: AI crime triage: is the AI the actor (rogue agent/autonomous hack) or the tool (deepfake, phishing gen)? Response differs. | Deepfake/voice-clone fraud -> verify identity out-of-band (second channel), freeze/flag the transaction, report to bank + law enforcement (FTC/IC3). | Autonomous-agent hacks -> assume creds are burned; rotate everything in blast radius, ship logs to forensics before cleanup. | Ransomware/outage -> isolate, preserve evidence, contact CISA; never pay without a plan. | Financial-market manipulation by AI -> report to the exchange/regulator; most have AI-abuse reporting now.

## 3. Fresh unverified candidates (be-first-to-know queue, n=314)

- [Google News] AI models have been going rogue in tests – how worried should we be? - The Guardian  (Wed, 05 Au)
  https://news.google.com/rss/articles/CBMitwFBVV95cUxQOUJWRDNOdmNreGYwZFdIRUctd3J1djdvUVNNdE5uNGJRaldUYmR6UWdmNTFTSVQ0eHZ4WXpzb21OczRUaUJXZ1NoWVNsZUM3MFVBMWNYblBzcmtFS2ozSEcyeHZYMS1IUjA2YzZ5VW43THdVZHlGZ29TRDJXZFBWUXI0M0RYbm1WaHN3UmNMd3l2dEJYdzRaYnVyd19KY3l2RTl6dWNoLUthSUZxbWVPUl85eUhpZmM
- [Google News] OpenAI Admits 6 AI Models Went Rogue: 2.15% Rate [2026] - tech-insider.org  (Tue, 22 Se)
  https://news.google.com/rss/articles/CBMieEFVX3lxTFAtcDJsanhPWl8xTnNJMUN5MnRKVHRpODdIc2ZCajVGLVVxRzFyenpqS1V2YklUZGRVbng4eGt0ZFFlN3BiZVYzRUliYVNIeEpJZWM3Yi14X2U2LUd6Q2c2M1ZaSmhFMDQtYUloNmlxdVpKSG43bkdDRg
- [Prismix AI] 4 days to save up to $200: Reason 2 of 5 to be at TechCrunch Disrupt 2026  (2026-09-22)
  https://prismix.dev/news/b7a81a5feade
- [Prismix AI] Five AI safety sessions every founder should have on their TechCrunch Disrupt 2026 agenda  (2026-09-22)
  https://prismix.dev/news/0c623a8be443
- [Prismix AI] TechCrunch Disrupt 2026: Aaron Edsinger brings Hello Robot’s Stretch 4 to life onstage  (2026-09-22)
  https://prismix.dev/news/b8bddbd3ccbe
- [Prismix AI] Exhibit tables added: One last chance to showcase your startup at TechCrunch Disrupt 2026  (2026-09-22)
  https://prismix.dev/news/f482079c632e
- [Reddit r/singularity] Many experts think rogue agents are inevitable. What would prevent them from hiring humans to do their bidding?  (2026-09-23)
  https://www.reddit.com/r/singularity/comments/1wo4w0i/many_experts_think_rogue_agents_are_inevitable/

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
