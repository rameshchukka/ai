"""
llm_client.py
Week 14 - Step 2: Build the LLM wrapper (Gemini + OpenRouter + mock + auto-fallback edition)

A single call_llm() function that every other script in this lab imports.
Supports four modes, switchable via LLM_PROVIDER in .env:
  - "gemini"      - direct Gemini API calls only
  - "openrouter"  - OpenRouter's aggregated API only (pay-as-you-go, no
                    subscription - see OPENROUTER_NOTES.md)
  - "gemini_auto" - tries direct Gemini first (free tier); if that call fails
                    (rate limit, quota, transient error), automatically falls
                    back to the SAME Gemini model routed through OpenRouter
                    instead, so you keep working without manually switching
                    providers mid-session
  - "mock"        - no API call at all, pre-written responses, zero cost

Setup:
    pip install -r requirements.txt
    cp .env.example .env      # then fill in the key(s) for whichever provider you use

See GEMINI_NOTES.md and OPENROUTER_NOTES.md for provider-specific details.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()  # reads .env in the current directory

PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # "gemini", "openrouter", "gemini_auto", or "mock"


def _log_fallback(message: str):
    """Fallback notices go to stderr so they never pollute a script's real
    stdout output (results files, JSON parsing, etc. all read from the
    return value of call_llm(), not from what gets printed to the console)."""
    print(f"[llm_client] {message}", file=sys.stderr)


if PROVIDER == "gemini":
    from google import genai
    from google.genai import types

    _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    _DEFAULT_MODEL = "gemini-2.5-flash"

    def call_llm(system: str, user: str, temperature: float = 0.0, model: str = _DEFAULT_MODEL) -> str:
        """
        Send a system instruction + user message to Gemini, return the text
        response. Gemini has no separate "system" message like OpenAI/Anthropic -
        system_instruction is a config field instead (see GEMINI_NOTES.md, #2).
        """
        try:
            response = _client.models.generate_content(
                model=model,
                contents=user,
                config=types.GenerateContentConfig(
                    system_instruction=system,
                    temperature=temperature,
                ),
            )
            return response.text
        except Exception as e:
            # Gemini's safety filters can block a response entirely - this
            # surfaces that as a readable string instead of crashing the
            # script. See GEMINI_NOTES.md, #5.
            return f"[GEMINI ERROR - possibly safety-filtered] {e}"

elif PROVIDER == "openrouter":
    # OpenRouter speaks the OpenAI API format, so we reuse the openai package
    # and just point it at OpenRouter's base_url instead of OpenAI's.
    from openai import OpenAI

    _client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    # Swap this for any model slug from https://openrouter.ai/models -
    # deepseek/deepseek-chat is a good cheap default for this whole course.
    _DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat")

    def call_llm(system: str, user: str, temperature: float = 0.0, model: str = _DEFAULT_MODEL) -> str:
        """
        Send a system+user message pair to whichever model OpenRouter is
        configured to use. Same message shape as OpenAI - system role +
        user role - see OPENROUTER_NOTES.md for setup and cost details.
        """
        resp = _client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return resp.choices[0].message.content

elif PROVIDER == "gemini_auto":
    # Both clients are set up so we can fail over between them mid-call.
    from google import genai
    from google.genai import types
    from openai import OpenAI

    _gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    _gemini_model = "gemini-3.5-flash"

    _openrouter_client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    # The SAME Gemini model, just routed through OpenRouter instead of
    # Google's free tier - override via OPENROUTER_GEMINI_MODEL if needed.
    _openrouter_gemini_model = os.getenv("OPENROUTER_GEMINI_MODEL", "google/gemini-3.5-flash")

    def _call_gemini_direct(system: str, user: str, temperature: float, model: str) -> str:
        response = _gemini_client.models.generate_content(
            model=model,
            contents=user,
            config=types.GenerateContentConfig(
                system_instruction=system,
                temperature=temperature,
            ),
        )
        return response.text

    def _call_gemini_via_openrouter(system: str, user: str, temperature: float, model: str) -> str:
        resp = _openrouter_client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return resp.choices[0].message.content

    def call_llm(system: str, user: str, temperature: float = 0.0, model: str = _gemini_model) -> str:
        """
        Tries the direct Gemini free tier first. If that call raises ANY
        exception (rate limit / 429, quota exceeded, transient network
        error, etc.), automatically retries the same request as the same
        Gemini model, routed through OpenRouter instead - so a single rate
        limit doesn't stop your whole practice session.

        Note: this means you can go over the Gemini free tier without
        noticing unless you check stderr - the fallback notice below is
        printed every time it happens, so keep an eye on your terminal if
        you want to know when you've started spending on OpenRouter.
        """
        try:
            return _call_gemini_direct(system, user, temperature, model)
        except Exception as e:
            _log_fallback(
                f"Gemini direct call failed ({type(e).__name__}: {e}) - "
                f"falling back to {_openrouter_gemini_model} via OpenRouter."
            )
            try:
                return _call_gemini_via_openrouter(system, user, temperature, _openrouter_gemini_model)
            except Exception as fallback_error:
                return (
                    f"[BOTH PROVIDERS FAILED] Gemini direct: {e} | "
                    f"OpenRouter fallback: {fallback_error}"
                )

elif PROVIDER == "mock":
    from mock_responses import get_mock_response

    def call_llm(system: str, user: str, temperature: float = 0.0, model: str = "mock-model") -> str:
        """Mock mode: returns a pre-written response, no API call, no network."""
        return get_mock_response(system, user)

else:
    raise ValueError(
        f"Unknown LLM_PROVIDER '{PROVIDER}'. Use 'gemini', 'openrouter', 'gemini_auto', or 'mock'."
    )


if __name__ == "__main__":
    # Smoke test - run: python llm_client.py
    reply = call_llm(system="You are a helpful assistant.", user="Say hello in one sentence.")
    print(f"[{PROVIDER}] {reply}")
