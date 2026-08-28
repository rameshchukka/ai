# Gemini API — Notes for This Lab

Quick reference for the Gemini-specific details that differ from OpenAI/Anthropic (which
the tutorial's original examples were written against). Read this once before running
anything — a few of these are easy to trip over.

## 1. SDK: use `google-genai`, not the older `google-generativeai`
Google's current unified SDK is `google-genai` (`from google import genai`). The older
`google-generativeai` package still works but is being phased out — this lab's
`llm_client.py` uses the current one.

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="...")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Why is the sky blue?",
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful assistant.",
        temperature=0.0,
    ),
)
print(response.text)
```

## 2. There's no separate "system" message — it's a config field
OpenAI/Anthropic take a `system` message as part of the conversation. Gemini instead takes
`system_instruction` as a field inside `GenerateContentConfig`, separate from `contents`
(which is just the user's message). Same concept, different shape — `llm_client.py`
already handles this for you.

## 3. Temperature range is 0–2, same idea as OpenAI
Same directional meaning as covered in Article 1.4 of the tutorial (0 = deterministic,
higher = more random) — no change to how you reason about it.

## 4. Structured/JSON output: `response_mime_type`
Instead of a separate "JSON mode" toggle, Gemini uses
`response_mime_type='application/json'` inside `GenerateContentConfig`. You can also pass a
`response_schema` (a Pydantic model or JSON schema) for schema-enforced output — the
strongest option, matching Article 3.2's "strongest technique" tier. This lab's exercises
default to prompt-only JSON instructions (matching the original tutorial exactly) so the
defensive-parsing lesson still applies, but try swapping in `response_mime_type` yourself
as a stretch goal in Exercise 4.

## 5. Safety filters can block a response entirely
This is a real Gemini-specific gotcha that doesn't really come up with OpenAI/Anthropic in
the same way. If Gemini's safety filters flag a prompt or response, `response.text` can
raise an exception instead of returning text, and the actual reason lives in
`response.candidates[0].finish_reason` (e.g., `"SAFETY"`). `llm_client.py` catches this and
returns a readable error string instead of crashing — worth reading that part of the code,
since defending against provider-specific failure modes like this is exactly the kind of
thing an FDE has to handle in production regardless of which model a client has standardized on.

## 6. Free tier / rate limits
Gemini's free tier (via Google AI Studio API keys) has generous but real rate limits
(requests per minute, requests per day) that vary by model and change over time. If you hit
a rate-limit error mid-exercise, that's expected — either wait, or switch to **mock mode**
(see below) to keep working without burning quota.

## 7. Model name
`llm_client.py` defaults to `gemini-2.5-flash` — fast and inexpensive, appropriate for this
whole lab. Check https://ai.google.dev/gemini-api/docs/models for the current model
lineup if you want to try a newer one; just change `_DEFAULT_MODEL` in `llm_client.py`.

## 8. Getting an API key
Get a free key from Google AI Studio: https://aistudio.google.com/app/apikey — no cloud
billing account required for the free tier.

---

## Mock Mode — Practicing Without an API Key or Quota

This lab adds a third `LLM_PROVIDER` option: `mock`. Set `LLM_PROVIDER=mock` in your `.env`
and `call_llm()` returns pre-written, realistic responses from `mock_responses.py` instead
of calling any real API. This is useful for:
- Working through the exercises before your Gemini key is set up
- Practicing the **defensive parsing** logic in Exercise 4 against known-tricky mock
  outputs (including a deliberately malformed one) without needing the model to
  cooperate
- Not burning API quota while you're just debugging your own script logic

Mock mode is *not* a substitute for actually running against live Gemini — the whole point
of Exercise 1 (temperature) and Exercise 2 (few-shot) is observing real model behavior. Use
mock mode to get your code working first, then switch `LLM_PROVIDER=gemini` and re-run
everything for the real exercise.
