# AI Incident Briefing — 2026-09-19

_Verified incidents in last 14d: 0 | AI-crime/chaos flagged: 0 | fresh candidates queued: 458_

## 1. Latest verified incidents

None in the window.
## 2. AI crime / chaos / havoc watch

No crime/chaos-flagged incidents in the window.

If one of these hits you: AI crime triage: is the AI the actor (rogue agent/autonomous hack) or the tool (deepfake, phishing gen)? Response differs. | Deepfake/voice-clone fraud -> verify identity out-of-band (second channel), freeze/flag the transaction, report to bank + law enforcement (FTC/IC3). | Autonomous-agent hacks -> assume creds are burned; rotate everything in blast radius, ship logs to forensics before cleanup. | Ransomware/outage -> isolate, preserve evidence, contact CISA; never pay without a plan. | Financial-market manipulation by AI -> report to the exchange/regulator; most have AI-abuse reporting now.

## 3. Fresh unverified candidates (be-first-to-know queue, n=458)

- [Google News] Ubuntu DDoS Attack: What Canonical’s Outage Reveals About DDoS Disruption - Security Boulevard  (Thu, 16 Ju)
  https://news.google.com/rss/articles/CBMirwFBVV95cUxNam5hME1lVUVUMENwUEJwTld5SURWVndTaTRIY01LTjRIUTd2U2RfeWxvcnlnbjRsWDdNQ2VNX3Y5cWs2Z1BmOVRyeC1aMVRobjVCQVRxVUExZkVyOTJfdlhTYnN1X1liUTZkUGhWM3pFUWFMUC1kWnhNSDRNXzllZUJWbVU3RXVxaEszd19ZMHFQaTM4WjQ3R3lTU1ROcngzakk3MXFQYlhMV25tUXNz
- [Google News] Autonomous attacks ushered cybercrime into AI era in 2025 - Cybersecurity Dive  (Wed, 04 Fe)
  https://news.google.com/rss/articles/CBMikgFBVV95cUxOTWljcm9kbEF4T0FtQW9GX3ZubzBLei1KUDhBV0NOaDJVUFkzbFVNVlkxSHZDMlpRQ1I1ell6VEFHZGVPalJxdEllZ2E0cmd5bzhzRTR3Q29iMHQ1X2RWUUNRTkE3UGJzN2RIWUhDMWtsX3FubW9XNDhvQXRBcGFaVWdha1F3MlY5TmdqQWtxeEE4UQ
- [Google News] AI code suggestions sabotage software supply chain - The Register  (Sat, 12 Ap)
  https://news.google.com/rss/articles/CBMiswFBVV95cUxNMTNJbEFvMk15Yk9ETFVpVkxjM2syM2tjWVQ5S3p1cDhwMXpNNnFkcjNtWXhxQWMyU05Dc0R2LVE5MXFzbTM0QjVpQ2wwc3VwUWNFT3ItRHpib05YcE1mQjZ6ejdQTDlLWk43Y2JYbmdWV3oySDdWYXg0YTBadTk5dmtBUU1iUWZ1QlVGVUk5ZTFiM01FNFhnQlRZX0M2SUhTMGVjeGM3elBNMWV4OENBQmVCYw
- [Google News] Cyberattacks target water utilities in Minnesota, disrupting OT operations and triggering multi-agency cyber response - Industrial Cyber  (Thu, 30 Ju)
  https://news.google.com/rss/articles/CBMiiwJBVV95cUxOZW4wNnYzOWxNcm1iTjRnLTA3eXIwODBDSWpELUt4NVR1dGNFM1BVcFRSLUpXckRCV3lCRlVKdVRIeG9EUm91NGNfZEI1cjFNTHhjQkVvajBLNE4tZ19EbWpfTE1zOGhQc0tJUjVOZ1ZrQW1JcEt0ZEQyX3pVRFJrYVllZFhTbWlfV3dFZnVhNUFyZWhDa0ZmLUdzc0t2aFdfZ01qOUFucUVQWkNlQXA2Rk5YcEpRd3gtaFZxanlRZzhWNXlqT0lEM2hzQlRKMkFXNUNhNXNUTUQ1MF9QZC1ZVXhGanZaWEJyWUZGTXN2amN0MzFnMnp4dVVvZTRQdTFUdDJsUlFNTU5UV2M

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
