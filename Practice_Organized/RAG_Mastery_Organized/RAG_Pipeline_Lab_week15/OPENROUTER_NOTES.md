# OpenRouter — Notes for This Lab

## Why OpenRouter
Gemini's free tier has real rate limits (requests per minute, requests per day) that are
easy to hit even with small practice scripts. OpenRouter is a pay-as-you-go aggregator —
no subscription, top up any amount, and it fronts 300+ models (including Gemini, GPT,
Claude, DeepSeek, and various open models) behind one API key and one consistent,
**OpenAI-compatible** request format. That's why `llm_client.py`'s `openrouter` branch
just reuses the `openai` Python package with a different `base_url` — no new SDK to learn.

## 1. Getting a key
1. Sign up at https://openrouter.ai
2. Generate a key at https://openrouter.ai/keys
3. Add credit — you can top up in small amounts (a few dollars easily covers this entire
   6-month course at this lab's exercise scale).

## 2. Picking a model
`llm_client.py` defaults to `deepseek/deepseek-chat` — cheap, fast, and good enough quality
for every exercise in this lab. Browse the full list with live pricing at
https://openrouter.ai/models — model slugs follow the pattern `provider/model-name`, e.g.:
- `deepseek/deepseek-chat` — cheapest good option, default for this lab
- `google/gemini-2.5-flash` — same Gemini model as the `gemini` provider branch, but routed
  through OpenRouter's rate limits instead of Google's free-tier limits
- `openai/gpt-4o-mini`, `anthropic/claude-3.5-haiku` — if you want to compare a different
  provider's behavior on the same exercise (genuinely useful for Lab 4's evaluation work)

Override the default any time by setting `OPENROUTER_MODEL` in `.env` — no code changes
needed.

## 3. Cost expectations for this lab
Every exercise script in this lab sends short prompts (a few hundred tokens each way) and
runs a handful of times. At `deepseek/deepseek-chat` pricing, running the **entire Lab 1**
end to end (all 6 exercise scripts, several calls each) costs a small fraction of a cent to
a few cents — realistically, your top-up will last the whole 6-month course unless you're
running things dozens of extra times. Track actual spend at
https://openrouter.ai/activity.

## 4. What's different from Gemini in the code
Nothing you need to touch — `call_llm(system, user, temperature)` has the exact same
signature regardless of provider. Under the hood, OpenRouter uses the same `system` +
`user` message-role shape as OpenAI (not Gemini's separate `system_instruction` field), so
switching `LLM_PROVIDER` between `gemini` and `openrouter` in `.env` is the only change
needed to swap providers for any script in this lab.

## 5. Rate limits and reliability
OpenRouter enforces its own reasonable rate limits (higher than most single-provider free
tiers), and if a specific upstream provider has an outage, some model slugs will fail over
automatically. If you hit a rate limit anyway, switch `LLM_PROVIDER=mock` temporarily to
keep working on your own code, then switch back.

## 6. The `gemini_auto` mode (recommended default)
Since your goal is real Gemini API reps for certification prep, but the free tier's rate
limits can interrupt a practice session, `llm_client.py` supports a fourth mode:
`LLM_PROVIDER=gemini_auto`. It tries the direct Gemini free tier first; if that call raises
any error (rate limit, quota exceeded, transient failure), it automatically retries the
**same request against the same Gemini model**, just routed through OpenRouter
(`google/gemini-2.5-flash` by default) instead. You don't have to notice the rate limit or
manually flip `LLM_PROVIDER` mid-session — it just keeps working.

Two things worth knowing about this mode:
- **It costs a little money once it falls back**, since the OpenRouter-routed call is
  billed even though the direct Gemini call would have been free had it succeeded. Watch
  your terminal's stderr output — every fallback prints a `[llm_client] ... falling back
  to google/gemini-2.5-flash via OpenRouter.` notice, so you always know when you've left
  the free tier.
- **Both providers need a valid key** for this mode — `GEMINI_API_KEY` for the primary
  attempt and `OPENROUTER_API_KEY` for the fallback. If you only have one, use `gemini` or
  `openrouter` mode directly instead.

This is the mode set as the `.env.example` default, since it gives you the best of both:
real Gemini reps most of the time, with automatic continuity when you hit a limit.

## 7. Staying safe with your key
Same rule as every other provider in this lab: the key lives only in `.env`, which is
already gitignored. Never hardcode it, never commit it, and set a spend limit/alert in the
OpenRouter dashboard if you want an extra safety net against a runaway loop (relevant again
in Lab 3, where an ungoverned agent loop can call the API repeatedly).
