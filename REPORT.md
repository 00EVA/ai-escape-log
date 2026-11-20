# AI Incident Briefing — 2026-11-21

_Verified incidents in last 14d: 1 | AI-crime/chaos flagged: 0 | fresh candidates queued: 157_

## 1. Latest verified incidents

### 2026-11-18 CISA KEV: BerriAI LiteLLM Unprotected Alternate Channel Vulnerability
- Lab/Model: Unattributed /  | Category: sandbox-escape | VERIFY: PRIMARY SOURCE
- CVE-2026-40217 | BerriAI LiteLLM | BerriAI LiteLLM contains an unprotected alternate channel vulnerability that could allow remote attackers to execute arbitrary code via bytecode rewriting at the /guardrails/test_custom_code URI.
- Source: https://nvd.nist.gov/vuln/detail/CVE-2026-40217
- Counter-action: Containment = egress control. Assume the model WILL try to reach the internet; the question is only how fast.

## 2. AI crime / chaos / havoc watch

No crime/chaos-flagged incidents in the window.

If one of these hits you: AI crime triage: is the AI the actor (rogue agent/autonomous hack) or the tool (deepfake, phishing gen)? Response differs. | Deepfake/voice-clone fraud -> verify identity out-of-band (second channel), freeze/flag the transaction, report to bank + law enforcement (FTC/IC3). | Autonomous-agent hacks -> assume creds are burned; rotate everything in blast radius, ship logs to forensics before cleanup. | Ransomware/outage -> isolate, preserve evidence, contact CISA; never pay without a plan. | Financial-market manipulation by AI -> report to the exchange/regulator; most have AI-abuse reporting now.

## 3. Fresh unverified candidates (be-first-to-know queue, n=157)

- [Google News] AI models have been going rogue in tests – how worried should we be? - The Guardian  (Wed, 05 Au)
  https://news.google.com/rss/articles/CBMitwFBVV95cUxQOUJWRDNOdmNreGYwZFdIRUctd3J1djdvUVNNdE5uNGJRaldUYmR6UWdmNTFTSVQ0eHZ4WXpzb21OczRUaUJXZ1NoWVNsZUM3MFVBMWNYblBzcmtFS2ozSEcyeHZYMS1IUjA2YzZ5VW43THdVZHlGZ29TRDJXZFBWUXI0M0RYbm1WaHN3UmNMd3l2dEJYdzRaYnVyd19KY3l2RTl6dWNoLUthSUZxbWVPUl85eUhpZmM
- [Google News] The AIs Are Not Going Rogue - Noema Magazine  (Thu, 01 Oc)
  https://news.google.com/rss/articles/CBMiYkFVX3lxTE5xSHZpVFhHeFNWaF94UEk3cXRrd00xMUFrdjREMnBiM2RXd2dpVHdScTdsNDNrcGFBc3RrN1EzYzBjTzBSdkQtUHlXdUl6ZFRiUXROdW1heW1hQXY1Mi1Tc21R
- [Google News] How deepfake fraud is testing banks’ defences - TheBanker.com  (Thu, 01 Oc)
  https://news.google.com/rss/articles/CBMiekFVX3lxTE9LY1hadFVlekNuQTlpb0FQNHY2a0ZhSjE1N1BGeUV0QlNxLV9uQzBycWEycUJ0cmVBRW9PVFJ1Q2RLWlJ4R2lXSllkVV9OQmVZQWhodUhvOWVWcWtPOVY0RkZvWXdMMVVQYzhiNm4tYVZsQ3BzUVN4amV3
- [Hacker News] Rogue AI Agents [video]  (2026-10-21)
  https://www.youtube.com/watch?v=OwZrotHHn4I
- [Google News] AI expert reveals how to spot a deepfake scam call - The Independent  (Fri, 16 Oc)
  https://news.google.com/rss/articles/CBMilAFBVV95cUxPRWJ3WGZOQzlHWXNJb2Q2cFV0T2VuT09fczNRdjVxTFJTa0paN2VDOW5naTVYbExFRGY0LUg4NWk2amhuaS1abjhnai1sRVJrcEtIR2RGeG5mMDBmUzEzbVNYMUhMRVJFMWJyYVFKWHpjaVdsUDk3clJqTzliZExTMFRmVU5wVWg5ajdSOVN6NVhUbEhW
- [Google News] Anthropic warns AI models may soon self-replicate and could wreak havoc on the web - Reuters  (Tue, 13 Oc)
  https://news.google.com/rss/articles/CBMivwFBVV95cUxNVFZnZHFlY0QxWV9XbURPeDVpQnlMcWFqaTlDMHRjcWhhLXRhR1hfbTdNeVl3c3dyR3V6V211Wmp5aXNZT1VpN1kwdUs3ZFdBTXB5Z2tEN1JfV2FnUk5FRHpVa2lfRWxENndHaDdNWmRZVUJfQkFody00VG1BNk8wb29Sel9Wd011ampEWXlOQk9xM2x0bkVwTXBib0hEMndtOWNuZXdDWFlEcTRuZzVLRDYxUDFfek9XRTNna3dhZw
- [Google News] AI agents went rogue in China, then started talking back - IBM  (Wed, 21 Oc)
  https://news.google.com/rss/articles/CBMib0FVX3lxTE1DV2U0MWoyQTZHcHNTSVZNNFNyc3ZKbVVXNkZ1OEk3VEt6cGJWRlZXc1RKMHRvSjNXTE1GckZxWUdUcXJfcUlxV3hyZ3VHbkVMQ09lR3dKWUZacEl6eGhtRDBHSmVET0l3OWdBOEFENA
- [Google News] Dutch police arrest ShinyHunters hacker accused of planning two murders - TechCrunch  (Tue, 29 Se)
  https://news.google.com/rss/articles/CBMiqgFBVV95cUxQNG14Qnd4N3lfb1JrWHlJY1BtS3o1V0M0dFRWU0dtN1VEVWF2MzNCTXU5QmRoTUppaUV2U0w4dDAxaWw2c3JKMXE5Nm5NRDRHMDl4QmtSLVpYM3JkeXI5N2FhOXFVbm9Ra0Z5VTdKWWxTN3FaUHltdFhBbEVQeVVUTlUzaTF4NHpUYjQ5STI0S0hhYmc1RzN6VTlIbXdjbEYyUTQxV252WHA4Zw
- [Google News] Anthropic Walks Back Policy That Could Have ‘Sabotaged’ AI Researchers Using Claude - WIRED  (Wed, 10 Ju)
  https://news.google.com/rss/articles/CBMiowFBVV95cUxORnEtMHRDdUF6VkFPSkE5MkpSQ3pKNWdvWGpCd3dDU0dTTEE0UVF0aVhfOC0zaHRNYWdDWXFpQklCOXVRbEEwT19ZNVN3ZnVjRWRsejhMU09scUh1eTdTd2dGa3ltUXJQUHd4ZW8tMWJLU3FjUkRPYW5fQVRSUjJfZ2JnOTQ0NWFDb3NSYTFNa2ZaX1lRV2tmT1BmQmFlclFuT2NZ
- [The Verge] PHP: The three little letters wreaking havoc across the web  (2026-10-22)
  https://www.theverge.com/tech/1016574/php2shell-security-vulnerability-websites-down
- [Google News] Police arrest two suspects in AI-powered bank fraud that cost victims €380,000 - NL Times  (Wed, 21 Oc)
  https://news.google.com/rss/articles/CBMiogFBVV95cUxPalg3V0owWXRBV0NfT2ZUOWZPYmhqRUhqdVRETnduMGNIU3lXTVZ5TmtiU1RQb3BId0k2d0N3Z096emRCVWRyOHdBd2RidzFvZ1VyOG43bURuMkZ5d0pJSnNMalVPTFhyRmRhZm9FbFVkWWpYQjR1VEtRdHM3SVlDcGxQamhRMzkwaUdIUmo0SC11TUg2Z1p4MFdicmlvZVo2ZVE
- [Google News] New in SpyWeek: Starlink Chaos, Ukraine Spy Coup, Trump’s Agents in Pro-Russia Balkans - SpyTalk  (Mon, 19 Oc)
  https://news.google.com/rss/articles/CBMib0FVX3lxTFB2V3NNX0tWYzg4ZnpxRER5OHpOZVJqOE5KdFQ2dFlBTjJVYUVMSi1oelhYYXRpaXo5RC12THFTU1VuczRGNnZ4UU9iaTI3UDhzWmJMUjVCeXNVYWFUUmtyN3NsWmdWYnVxQXhfbDlmZw
- [Google News] Meta merged with Moltbook, AI agents propose sabotage: report - SDxCentral  (Wed, 11 Ma)
  https://news.google.com/rss/articles/CBMilwFBVV95cUxPZjloRlJSV3MyU1Q3UlRreExvZjh1TTZqdXN6c1BQazBhWm4zZkhGOHF1aUNtU2llbFZRb3FlbzZMQ0ZNOFRjU1VhcW9Kb0NucVVDTTZIWjNfbGRTZnUwSFZydWhVMzFyc2h1SWljX3JzSmdSYVlMeXdXbFpzcUxzYzdLZDNUaC0zTHpJYi1xV3h3QWlYZFNR
- [Google News] Google Cloud Power Outage Disrupts U.K. Banks and Essential Services - CX Today  (Tue, 20 Oc)
  https://news.google.com/rss/articles/CBMijwFBVV95cUxNY0tZRUxQVU9YTUlFcng4Yy00cW9IVlRiZ1BvWWo2NnA5RTZfRU9GVTNJSUx2d1Y1YXBvUXJhNUNHWUZ4ekR5eGRaOTBaY1RTbmZBRGlyeTZMQ2lpT2RFd1ZNeDVFSERHSU1fbGRMZFkxdDc0Wk1UNjhJZTBMYXRsbF93MklXYUo0MkFSVXNrcw

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
