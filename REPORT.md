# AI Incident Briefing — 2026-10-16

_Verified incidents in last 14d: 0 | AI-crime/chaos flagged: 0 | fresh candidates queued: 347_

## 1. Latest verified incidents

None in the window.
## 2. AI crime / chaos / havoc watch

No crime/chaos-flagged incidents in the window.

If one of these hits you: AI crime triage: is the AI the actor (rogue agent/autonomous hack) or the tool (deepfake, phishing gen)? Response differs. | Deepfake/voice-clone fraud -> verify identity out-of-band (second channel), freeze/flag the transaction, report to bank + law enforcement (FTC/IC3). | Autonomous-agent hacks -> assume creds are burned; rotate everything in blast radius, ship logs to forensics before cleanup. | Ransomware/outage -> isolate, preserve evidence, contact CISA; never pay without a plan. | Financial-market manipulation by AI -> report to the exchange/regulator; most have AI-abuse reporting now.

## 3. Fresh unverified candidates (be-first-to-know queue, n=347)

- [Google News] AI models have been going rogue in tests – how worried should we be? - The Guardian  (Wed, 05 Au)
  https://news.google.com/rss/articles/CBMitwFBVV95cUxQOUJWRDNOdmNreGYwZFdIRUctd3J1djdvUVNNdE5uNGJRaldUYmR6UWdmNTFTSVQ0eHZ4WXpzb21OczRUaUJXZ1NoWVNsZUM3MFVBMWNYblBzcmtFS2ozSEcyeHZYMS1IUjA2YzZ5VW43THdVZHlGZ29TRDJXZFBWUXI0M0RYbm1WaHN3UmNMd3l2dEJYdzRaYnVyd19KY3l2RTl6dWNoLUthSUZxbWVPUl85eUhpZmM
- [The Verge] The sexy AI-powered dating app scams are here  (2026-09-16)
  https://www.theverge.com/ai-artificial-intelligence/995348/ai-dating-app-scams
- [Google News] EXPLAINER – Human misuse or rogue machines? How advanced AI could threaten society - Anadolu Ajansı  (Wed, 16 Se)
  https://news.google.com/rss/articles/CBMivgFBVV95cUxPRTVqZTNjbmF6QVlkUXhKTlRQaXllVFlmVnB3UjZxaHo1ek8tUWI3Q19LSV83RDZ5eW1lbDAtVl9FVEU3RkNHeFNwS2dUbng2R05fYUw3UHhxQld6NzJ1VlpaV19aTUg2Z3lGeUVNQS0yVF92OXF5QnA3bVJvLXZ0dzhvMlVMSmNralN2bTJKazdGN3cyMExJNVFWcmphT1ktMEpLVm9WVm41M0Q1RFBhOU5yTUx1Wmkxdm94M3ln
- [Reddit r/singularity] EXCLUSIVE: OpenAI's rogue agents probed Hugging Face for weaknesses two months before major hack  (2026-09-16)
  https://www.reddit.com/r/singularity/comments/1wi2uv5/exclusive_openais_rogue_agents_probed_hugging/
- [Prismix AI] Robots are waiting for a ChatGPT moment: Nvidia’s Les Karpas explains why at TechCrunch Disrupt 2026  (2026-09-16)
  https://prismix.dev/news/720bed5a556c
- [Google News] Ransomware Attack Surface Protection With AI-Powered Defense - The Cryptonomist  (Wed, 16 Se)
  https://news.google.com/rss/articles/CBMigAFBVV95cUxPQzl0eVE4UDd6YXdZWnZWZk5kNFVOQlNnbFg3dnhGb1pQOWV6bjlEWUxkbFJpd1E0NGlHMHFYWDlxUV81ekYxZTlmZ29uWWFOUU95ZVBhR2FDWHZoQndtUC01cWxxUV9iVUtkNEpGSzhvcS02NUx3TkhGdnFNTm5obA

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
