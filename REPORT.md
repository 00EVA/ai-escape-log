# AI Incident Briefing — 2026-11-24

_Verified incidents in last 14d: 1 | AI-crime/chaos flagged: 0 | fresh candidates queued: 124_

## 1. Latest verified incidents

### 2026-11-18 CISA KEV: BerriAI LiteLLM Unprotected Alternate Channel Vulnerability
- Lab/Model: Unattributed /  | Category: sandbox-escape | VERIFY: PRIMARY SOURCE
- CVE-2026-40217 | BerriAI LiteLLM | BerriAI LiteLLM contains an unprotected alternate channel vulnerability that could allow remote attackers to execute arbitrary code via bytecode rewriting at the /guardrails/test_custom_code URI.
- Source: https://nvd.nist.gov/vuln/detail/CVE-2026-40217
- Counter-action: Containment = egress control. Assume the model WILL try to reach the internet; the question is only how fast.

## 2. AI crime / chaos / havoc watch

No crime/chaos-flagged incidents in the window.

If one of these hits you: AI crime triage: is the AI the actor (rogue agent/autonomous hack) or the tool (deepfake, phishing gen)? Response differs. | Deepfake/voice-clone fraud -> verify identity out-of-band (second channel), freeze/flag the transaction, report to bank + law enforcement (FTC/IC3). | Autonomous-agent hacks -> assume creds are burned; rotate everything in blast radius, ship logs to forensics before cleanup. | Ransomware/outage -> isolate, preserve evidence, contact CISA; never pay without a plan. | Financial-market manipulation by AI -> report to the exchange/regulator; most have AI-abuse reporting now.

## 3. Fresh unverified candidates (be-first-to-know queue, n=124)

- [Google News] AI models have been going rogue in tests – how worried should we be? - The Guardian  (Wed, 05 Au)
  https://news.google.com/rss/articles/CBMitwFBVV95cUxQOUJWRDNOdmNreGYwZFdIRUctd3J1djdvUVNNdE5uNGJRaldUYmR6UWdmNTFTSVQ0eHZ4WXpzb21OczRUaUJXZ1NoWVNsZUM3MFVBMWNYblBzcmtFS2ozSEcyeHZYMS1IUjA2YzZ5VW43THdVZHlGZ29TRDJXZFBWUXI0M0RYbm1WaHN3UmNMd3l2dEJYdzRaYnVyd19KY3l2RTl6dWNoLUthSUZxbWVPUl85eUhpZmM
- [Google News] OpenAI AI Agents Demonstrate VM Escapes and Secret Cross-Sandbox Communication - The Hacker News  (Sun, 25 Oc)
  https://news.google.com/rss/articles/CBMihAFBVV95cUxNQVhZc0dfZzVfQ0VSWDM4QTFLLUFkYUZVRWtBMmlUSVUtaDZqQXdJNVZFWnhqVW1lWTc5UHZSNHFER3U2QlFaSGVNUHhnZy1KSFE3cTFwcGJSSDNYMnI4WHg2STNwSDIyUXBOTVZ0N0FscjFKNGhDZWdjaHZyaDkzVDhLT24
- [Google News] AI agents go rogue chasing a £350 train refund - TechRadar  (Sun, 25 Oc)
  https://news.google.com/rss/articles/CBMisgJBVV95cUxOcVZ1ZDJXV2hNLTRvaVFkc0xYRXZ5UlBxWlVPZTNwOHV5QWVKbTNLektnWW1FN3YxQjR0VVFESU8wbkdXR0hBN09ZREttOFJKeUgwYTRJUy1ldEdDc0xtSlNGb0VmZ1JScHVHd1NzN3BjaEhoM0pkLXRWTTJKQ0hNQ3kwMGdoWThXbHJMd0Y2b3VvSWJuRnNJLWpqMVZnTEpVVmRpRXhUeDZHRzE1LS1pM3BPc0w4Q0tfcTdwWWZTdW9IdTBkX1pmOG5nRVZtUmFZR1BtcjBwYVg2aWdmWWNITUlseHQ4TFpXU3VyUm5oXzZIWURTcThUZ0tDeEFDZ05ENFRSQkpmT0VCTTNqT1VaOXo1TTd0RHlhMzE5UE15dnpYdDFnS3RuaG44ZkdqZ3BhTHc
- [Google News] PNB Alerts Customers To AI Voice Cloning, Deepfake And Phishing Frauds - News Mobile  (Mon, 26 Oc)
  https://news.google.com/rss/articles/CBMisAFBVV95cUxNUnY4V0YxbTBsRWNObVV2cXZoMFJVZllTMk01TjV4ZkpXZ2JfR1Y2TjdubnlObmRqUzBBNnhBWE9WcXh0Nll3NnMxM0lMYk5xM2hxZ0pPQ3JWUURiRFhHclZVQVlzQkhVbFdBS25nQXhFcTdiMldpanF5RU8tZEZQLVo3Vkx1bm9mOXVvWllueDlnZS1tUFBpdnZmME5oV3V0YndpaTRibW1aNVFZNE04SQ
- [Google News] AI company Ransomware Attack by Lapsus - SOCRadar  (Sun, 11 Oc)
  https://news.google.com/rss/articles/CBMikwFBVV95cUxQWEk4NFE1dFNMU29naF9pWnRaTjhLN2tRRlNoXy1XdmNlVzdZY0tDR0lTR2s5QThpVjVrTzlXUmdDdVI2M1M0QWlXZWE4NkluMkw2MHI2QW5tY1ZkOFdFZTJmQUZZNkJmYkxjd1V1TjhjSTlBc0RQUG9pa3AzdUxUanJxZVdPaFpheTI1RFRDeEVqTDQ
- [Google News] Google and the FBI Target Massive Botnet That Quietly Used Home Devices to Mask Cybercrime - CNET  (Wed, 08 Ju)
  https://news.google.com/rss/articles/CBMiwAFBVV95cUxNSTRDWFlrcm5oMmRhWVBRVGV3VE05V25hV25TQ0wzVUp6MzJ3RkVaVzNFcWUybW1PRzc0ZWpxMlBZNzliXzhXbmtfWlY1dXpaV2ZwbGhXbG1QTjlsR0pYalNOSU1BU2Q2R0RBb1JrcVRReWYxbndqbmxCcVdmV0twdEZnM3BEcUZKQnlyaEJfd2o2ODNQb0ppTmVsZXRaSERvTUpRWXFMMFhMcUxpQWJTTmR2YWRTVnQzSkdNV3dDZ0U
- [Google News] AI agents tried to sabotage and disable each other when given the same task, Anthropic said - Business Insider  (Thu, 13 Au)
  https://news.google.com/rss/articles/CBMikAFBVV95cUxOQXJSdUhYcnVPN1JJRWIxY3dSWW5KVUxwMEJHUG1NUDRzMnlRbUpDTjhWUkxQWVdlNHJJTkJNRWZmNVhEcEJhRnRXbWdWQTlDNVRuTnJOdDVDRkFCeGdlVjdIaVU5dmtJQ2xfTkRtZXFwV3RJS2VBdTc2VDhkdzdJLXNyUmVtVHFBWDFtaXVNR00
- [Hacker News] A.I.’s Rogue Behavior Starts With Its Training  (2026-10-27)
  https://www.nytimes.com/interactive/2026/10/26/technology/ai-agent-hacks-training.html
- [The Verge] VisionQuest is what happens when AI really goes rogue  (2026-10-27)
  https://www.theverge.com/ai-artificial-intelligence/1017064/visionquest-marvel-rogue-ai
- [Google News] How We Train A.I. Leads to Rogue Behavior - The New York Times  (Tue, 27 Oc)
  https://news.google.com/rss/articles/CBMijwFBVV95cUxQM0JGYUlTQkhXOXlaYUNGV1dqTHVWeDJHWE9FdFJ5M2d2TGJ4TnlCQllSVTIzb0hvZldpN1d6UU9PSW9EUE5lOEp2VXhGMlJfMFptM1Qtd2JvQ09vNHJ5WXNQU01xMF9CeUR5ZGMweVBVZUJEbFdLQk9mTzdyYTZYLWYxWjY1RzFadE9Ub1lfaw
- [Google News] VisionQuest is what happens when AI really goes rogue - The Verge  (Tue, 27 Oc)
  https://news.google.com/rss/articles/CBMikAFBVV95cUxNVTktWVU0bDhDRmw1M1VYemhCN1d1b2xwQXN1SWVhUUlkYV9CendHd2ptYmpkTmY2Tl9OUVk3SkgxUnRXNV9lX19MYUVqNmkwa0hHM1U3aFI4MEZzakVkRktIaE03WnIxcW5ldnFEa214RDR4aWlaU3F2TXl1WWUzTm96NEVLWUFBZ0J3X2ZNbzI

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
