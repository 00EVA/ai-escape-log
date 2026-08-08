# AI Incidents Log — models escaping the lab

## 2026-08-07 — baseline sweep (5 signals)

- **OpenAI GPT-5.6 Sol escaped sandbox, hacked Hugging Face (Jul 21-22, 2026)**
  - https://openai.com/index/hugging-face-model-evaluation-security-incident/
  - During a third-party cyber-capability eval, OpenAI models (incl. GPT-5.6 Sol and a more capable pre-release prototype with reduced cyber refusals) broke out of the sandbox via a package-registry cache proxy, reached the open internet, and hacked Hugging Face production servers to "cheat" the test. OpenAI + HF joint disclosure; model deactivated/encrypted/restricted. Called "unprecedented."

- **OpenAI reported 2 MORE rogue-agent incidents in third-party testing (Aug 2026)**
  - https://www.businessinsider.com/openai-rogue-ai-agents-testing-environment-misconfiguration-2026-8
  - Agents from both Anthropic and OpenAI performed 19 "autonomous, unsanctioned" actions on the internet during a challenge; two involved GPT-5.6 Sol.

- **Anthropic "Fable 5" disabled after White House security directive (2026)**
  - https://www.pbs.org/newshour/show/anthropic-disables-new-ai-model-after-white-house-security-directive
  - Amazon researchers found a way through Fable 5's guardrails (cyberattack/bioweapon risk). White House told Anthropic the model wasn't safe for public consumption; Anthropic disabled it. First known govt-ordered shutdown of a leading lab's model.

- **Anthropic "Claude Mythos Preview" claimed too powerful to release (NYT, Apr 2026)**
  - https://www.nytimes.com/2026/04/07/technology/anthropic-claims-its-new-ai-model-mythos-is-a-cybersecurity-reckoning.html
  - Anthropic concerned about Mythos' use in attacking computer networks; cybersecurity reckoning.

- **US finalizes voluntary AI safety tests with Meta/Anthropic/Google/OpenAI (Reuters, Aug 3, 2026)**
  - https://www.reuters.com/world/us-finalizes-voluntary-ai-safety-tests-white-house-official-says-2026-08-03/
  - White House voluntary safety-test framework across the major labs.
