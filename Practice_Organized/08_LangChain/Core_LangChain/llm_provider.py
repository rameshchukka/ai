"""
llm_provider.py  (v2 -- self-contained, no inhouse_llm.py / inhouse_wrappers.py needed)
=========================================================================================
Everything from inhouse_llm.py + inhouse_wrappers.py + the security patch is merged
into this ONE file. Your notebooks/scripts only ever need:

    llm_provider.py  +  .env  (copied from .env.personal.example or .env.office.example)

Usage -- identical on both machines:

    from llm_provider import get_chat_model, get_embeddings_model, CURRENT_ENV

    llm = get_chat_model("chat")              # task preset...
    llm = get_chat_model(model=MODEL_MISTRAL)  # ...or any specific office model by name
    embeddings = get_embeddings_model()

    llm.invoke("hello")
    embeddings.embed_query("some text")

Fixes carried over from the earlier wrapper/patch work (kept, not re-broken here):
  - Office API_KEY has NO hardcoded fallback -- raises clearly if MODEL_1_APIKEY is
    missing from .env, instead of silently using a credential embedded in source.
  - Cert path comes from IDFC_CERT_PATH in .env, not a hardcoded personal machine path.
  - Every office model gets ITS OWN base_url (the original inhouse_llm.py bug routed
    every model through the Qwen3-14B endpoint regardless of which model= was passed).
  - Vision messages use proper OpenAI-compatible image_url content blocks, not raw
    base64 appended as a third plain-text message.
  - HF_HUB_OFFLINE / TRANSFORMERS_OFFLINE / HF_DATASETS_OFFLINE are set at import
    time, before any HF-adjacent import can happen.

What's new in this version:
  - ALL SEVEN office models are named constants AND individually reachable, not just
    the five that had a task preset. Mistral (previously unreachable -- your own
    learning_guide.md calls for it as a "cross-check vs Qwen family" model) now has
    both a direct MODEL_MISTRAL route and a "cross_check" task preset.
  - get_chat_model() accepts an explicit model= override so you're never limited to
    the 5 task presets -- request any of the 7 by name directly.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# 1. WHICH ENVIRONMENT AM I ON?
# ---------------------------------------------------------------------------
# Explicit env var wins. Set once per machine in that machine's .env:
#   personal laptop:  LLM_ENV=personal
#   office laptop:     LLM_ENV=office

CURRENT_ENV = os.getenv("LLM_ENV", "").strip().lower()

if CURRENT_ENV not in ("personal", "office"):
    if os.getenv("OPENAI_API_KEY"):
        CURRENT_ENV = "personal"
    elif os.getenv("MODEL_1_APIKEY"):
        CURRENT_ENV = "office"
    else:
        CURRENT_ENV = "personal"
    print(f"[llm_provider] LLM_ENV not set -- auto-detected '{CURRENT_ENV}'. "
          f"Set LLM_ENV explicitly in .env to avoid relying on this guess.",
          file=sys.stderr)

# ---------------------------------------------------------------------------
# 2. OFFICE BRANCH -- force HF offline BEFORE any HF-adjacent import can run,
#    regardless of whether get_chat_model()/get_embeddings_model() is called
#    yet. Cheap and side-effect-free on the personal branch, so always safe.
# ---------------------------------------------------------------------------
if CURRENT_ENV == "office":
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    os.environ.setdefault("HF_DATASETS_OFFLINE", "1")


# ===========================================================================
# 3. OFFICE MODELS -- all seven, named and individually reachable.
# ===========================================================================
# Endpoints are IDFC infra, not secrets -- kept as defaults, overridable via
# env if the endpoints ever change without a code update.

API_BASE_QWEN3_14B     = os.getenv("API_BASE_QWEN3_14B",     "https://llm-api.iservebetter.idfcfirstbank.com/qwen3-14b/v1")
API_BASE_QWEN3_30B     = os.getenv("API_BASE_QWEN3_30B",     "https://llm-api.iservebetter.idfcfirstbank.com/qwen3-30b/v1")
API_BASE_MISTRAL       = os.getenv("API_BASE_MISTRAL",       "https://llm-api.iservebetter.idfcfirstbank.com/mistral-24b/v1")
API_BASE_LLAMA         = os.getenv("API_BASE_LLAMA",         "https://llm-api.iservebetter.idfcfirstbank.com/llama-70b/v1")
API_BASE_DEVSTRAL      = os.getenv("API_BASE_DEVSTRAL",      "https://llm-api.iservebetter.idfcfirstbank.com/devstral-25b/v1")
API_BASE_QWEN2_5_VL_7B = os.getenv("API_BASE_QWEN2_5_VL_7B", "https://llm-api.iservebetter.idfcfirstbank.com/qwen-vl-7b/v1")
API_BASE_JINA          = os.getenv("API_BASE_JINA",          "https://llm-api.iservebetter.idfcfirstbank.com/jina-embeddings-v3/v1")

MODEL_QWEN3_14B     = "/app/models/Qwen3-14B-FP8"
MODEL_QWEN3_30B     = "/app/models/Qwen3-32B"
MODEL_MISTRAL       = "/app/models/Mistral-Small-3.1-24B"
MODEL_LLAMA         = "/app/models/Meta-Llama-3-70B-Instruct-FP8-Dynamic"
MODEL_DEVSTRAL      = "/app/models/Devstral-Small-2505"
MODEL_QWEN2_5_VL_7B = "/app/models/Qwen2.5-VL-7B-Instruct"
MODEL_JINA          = "/app/models/jina_embeddings-v3"

# Every chat-capable model -> its OWN base_url. This is what makes each model
# actually reachable (the original bug routed all of them through Qwen3-14B).
_OFFICE_BASE_URL_BY_MODEL = {
    MODEL_QWEN3_14B:     API_BASE_QWEN3_14B,
    MODEL_QWEN3_30B:     API_BASE_QWEN3_30B,
    MODEL_MISTRAL:       API_BASE_MISTRAL,
    MODEL_LLAMA:         API_BASE_LLAMA,
    MODEL_DEVSTRAL:      API_BASE_DEVSTRAL,
    MODEL_QWEN2_5_VL_7B: API_BASE_QWEN2_5_VL_7B,
}

# Task presets. "cross_check" added so Mistral -- previously unreachable via
# any task preset -- has a named route in, matching your learning_guide.md's
# stated use ("cross-checking prompt behavior vs Qwen family").
OFFICE_TASK_MAP = {
    "chat":        MODEL_QWEN3_14B,
    "reasoning":   MODEL_QWEN3_30B,
    "code":        MODEL_DEVSTRAL,
    "vision":      MODEL_QWEN2_5_VL_7B,
    "judge":       MODEL_LLAMA,
    "cross_check": MODEL_MISTRAL,
}


def _office_api_key() -> str:
    key = os.getenv("MODEL_1_APIKEY")
    if not key:
        raise RuntimeError(
            "MODEL_1_APIKEY not set. Add it to your .env file -- "
            "never hardcode a fallback credential in source."
        )
    return key


def _office_cert_path():
    cert_path = os.getenv("IDFC_CERT_PATH", "")
    return cert_path if cert_path and os.path.exists(cert_path) else False


_office_http_client_cache = None
_office_http_client_built = False


def _office_http_client():
    """Lazily builds (and caches) the SSL-aware httpx client. Only touched
    when an office chat/embeddings call actually happens -- never at import,
    so this file stays side-effect-free on the personal branch."""
    global _office_http_client_cache, _office_http_client_built
    if _office_http_client_built:
        return _office_http_client_cache

    _office_http_client_built = True
    cert_path = _office_cert_path()
    if not cert_path:
        print(f"[llm_provider] IDFC_CERT_PATH not set or file not found -- "
              f"SSL verification disabled for office endpoints.", file=sys.stderr)
        return None

    import httpx
    try:
        _office_http_client_cache = httpx.Client(verify=cert_path, timeout=httpx.Timeout(60.0))
        print(f"[llm_provider] SSL HTTP client created with certificate: {cert_path}", file=sys.stderr)
    except Exception as e:
        print(f"[llm_provider] Warning: could not create SSL HTTP client: {e}", file=sys.stderr)
        _office_http_client_cache = None
    return _office_http_client_cache


def _get_chat_model_office(task: str = "chat", model: str = None, max_tokens: int = 1000, **kwargs):
    """
    Pass task="..." for a preset (chat/reasoning/code/vision/judge/cross_check),
    OR pass model=MODEL_XXX directly for full control over which of the seven
    office models you get -- both are supported, model= takes priority.
    """
    from langchain_openai import ChatOpenAI

    if model is None:
        if task not in OFFICE_TASK_MAP:
            raise ValueError(f"Unknown task '{task}'. Choose from {list(OFFICE_TASK_MAP)}, "
                              f"or pass model=<one of {list(_OFFICE_BASE_URL_BY_MODEL)}> directly.")
        model = OFFICE_TASK_MAP[task]

    base_url = _OFFICE_BASE_URL_BY_MODEL.get(model)
    if base_url is None:
        raise ValueError(f"Unknown model path: {model!r}. Known models: {list(_OFFICE_BASE_URL_BY_MODEL)}")

    return ChatOpenAI(
        base_url=base_url,
        api_key=_office_api_key(),
        model=model,
        max_tokens=max_tokens,
        http_client=_office_http_client(),
        **kwargs,
    )


def _resize_or_compress_image(image_base64: str, max_dimension: int = 512,
                               size_threshold: int = 500_000) -> str:
    """
    Carried over from the original inhouse_llm.py multimodal_chat() -- this is
    the actual fix for the "image/embedding issue": full-resolution images
    sent as base64 can push a request well past the model's token budget and
    the call fails outright. This shrinks large images BEFORE they're ever
    sent, in the same order of preference as the original:
        1. Resize via PIL to max_dimension on the long edge (best quality/size tradeoff)
        2. If PIL is unavailable or resize fails, crudely truncate the base64 string instead
        3. Hard ceiling: never send more than ~1MB of base64 no matter what
        4. Extra squeeze for very tight max_tokens budgets (handled by the caller,
           see build_vision_messages()'s max_tokens param)
    """
    if len(image_base64) <= size_threshold:
        return image_base64

    print(f"[llm_provider] Large image detected ({len(image_base64)} base64 chars) -- "
          f"resizing to keep the request within the model's token budget.", file=sys.stderr)

    try:
        import base64 as _b64
        import io
        from PIL import Image

        image_data = _b64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        resized = _b64.b64encode(buffer.getvalue()).decode("utf-8")
        print(f"[llm_provider] Resized image: {len(image_base64)} -> {len(resized)} base64 chars", file=sys.stderr)
        image_base64 = resized
    except ImportError:
        print("[llm_provider] Pillow not installed -- falling back to crude base64 "
              "truncation instead of a real resize (pip install pillow to fix properly).",
              file=sys.stderr)
        image_base64 = image_base64[:50_000]
    except Exception as e:
        print(f"[llm_provider] Image resize failed ({e}) -- falling back to truncation.", file=sys.stderr)
        image_base64 = image_base64[:50_000]

    # Hard ceiling regardless of how we got here
    if len(image_base64) > 1_000_000:
        print("[llm_provider] Still over 1MB after resize -- hard-truncating.", file=sys.stderr)
        image_base64 = image_base64[:100_000]

    return image_base64


def build_vision_messages(system_prompt: str, user_prompt: str, image_base64: str,
                           image_format: str = "png", max_tokens: int = 1000):
    """Correctly-formatted multimodal messages (proper image_url content block),
    AND automatically resizes/compresses oversized images first -- see
    _resize_or_compress_image() docstring for why this matters.
    Use with get_chat_model(model=MODEL_QWEN2_5_VL_7B) or task='vision'."""
    from langchain_core.messages import SystemMessage, HumanMessage

    image_base64 = _resize_or_compress_image(image_base64)

    # Extra squeeze when the token budget is especially tight, same threshold
    # the original code used.
    if max_tokens < 500 and len(image_base64) > 100_000:
        print(f"[llm_provider] Low max_tokens ({max_tokens}) with a still-large image -- "
              f"compressing further.", file=sys.stderr)
        image_base64 = image_base64[:20_000]

    return [
        SystemMessage(content=system_prompt),
        HumanMessage(content=[
            {"type": "text", "text": user_prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/{image_format};base64,{image_base64}"}},
        ]),
    ]


def _office_get_embeddings(texts, dimension: int = 1024):
    import requests

    if isinstance(texts, str):
        texts = [texts]

    url = f"{API_BASE_JINA}/embeddings"
    headers = {"Authorization": f"Bearer {_office_api_key()}", "Content-Type": "application/json"}
    payload = {"input": texts, "dimension": dimension, "embedding_type": "float"}
    verify_param = _office_cert_path()

    response = requests.post(url, json=payload, headers=headers, verify=verify_param, timeout=60)
    if response.status_code != 200:
        raise RuntimeError(f"Jina embeddings API error: {response.status_code} - {response.text}")
    return [item["embedding"] for item in response.json()["data"]]


class _OfficeEmbeddings:
    """LangChain-standard Embeddings interface wrapping the Jina endpoint."""
    def embed_documents(self, texts):
        return _office_get_embeddings(texts)

    def embed_query(self, text: str):
        return _office_get_embeddings([text])[0]


def _get_embeddings_model_office():
    return _OfficeEmbeddings()


# ===========================================================================
# 4. PERSONAL BRANCH -- real OpenAI / API-router.
# ===========================================================================

PERSONAL_MODEL_MAP = {
    "chat":      os.getenv("PERSONAL_MODEL_CHAT", "gpt-4o-mini"),
    "reasoning": os.getenv("PERSONAL_MODEL_REASONING", "gpt-4o"),
    "code":      os.getenv("PERSONAL_MODEL_CODE", "gpt-4o-mini"),
    "vision":    os.getenv("PERSONAL_MODEL_VISION", "gpt-4o"),
    "judge":     os.getenv("PERSONAL_MODEL_JUDGE", "gpt-4o"),
}
PERSONAL_API_BASE = os.getenv("PERSONAL_API_BASE")  # None -> OpenAI SDK default
PERSONAL_API_KEY = os.getenv("OPENAI_API_KEY")


def _get_chat_model_personal(task: str = "chat", model: str = None, max_tokens: int = 1000, **kwargs):
    from langchain_openai import ChatOpenAI

    if not PERSONAL_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set. Add it to .env on this (personal) machine.")
    if model is None:
        if task not in PERSONAL_MODEL_MAP:
            raise ValueError(f"Unknown task '{task}'. Choose from {list(PERSONAL_MODEL_MAP)}, "
                              f"or pass model='gpt-4o' (etc.) directly.")
        model = PERSONAL_MODEL_MAP[task]

    return ChatOpenAI(base_url=PERSONAL_API_BASE, api_key=PERSONAL_API_KEY, model=model,
                       max_tokens=max_tokens, **kwargs)


def _get_embeddings_model_personal():
    from langchain_openai import OpenAIEmbeddings

    if not PERSONAL_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set. Add it to .env on this (personal) machine.")
    model_name = os.getenv("PERSONAL_MODEL_EMBEDDING", "text-embedding-3-small")
    return OpenAIEmbeddings(base_url=PERSONAL_API_BASE, api_key=PERSONAL_API_KEY, model=model_name)


# ===========================================================================
# 5. PUBLIC INTERFACE -- the only thing your notebooks import.
# ===========================================================================

def get_chat_model(task: str = "chat", model: str = None, max_tokens: int = 1000, **kwargs):
    """
    task:  "chat" | "reasoning" | "code" | "vision" | "judge"
           (office also has "cross_check" -> Mistral)
    model: optional override -- pass a MODEL_XXX constant directly to bypass
           task presets entirely and get any specific model.
    Returns a LangChain-standard ChatOpenAI, either branch.
    """
    if CURRENT_ENV == "office":
        return _get_chat_model_office(task, model=model, max_tokens=max_tokens, **kwargs)
    return _get_chat_model_personal(task, model=model, max_tokens=max_tokens, **kwargs)


def get_embeddings_model():
    """Returns a LangChain-standard Embeddings object for whichever environment."""
    if CURRENT_ENV == "office":
        return _get_embeddings_model_office()
    return _get_embeddings_model_personal()


# ===========================================================================
# 6. TOKEN COUNTING -- same "installed locally but still phones home" bug
#    class as Hugging Face. tiktoken.get_encoding() downloads its BPE rank
#    file from openaipublic.blob.core.windows.net on first use if it isn't
#    already cached -- this can hang/fail on the office network exactly like
#    HF did, even though the tiktoken PACKAGE itself installed fine via JFrog.
# ===========================================================================
# Two-part fix:
#   1. Point TIKTOKEN_CACHE_DIR at a local folder. Run this ONCE from your
#      personal laptop (which has internet) to populate the cache, then copy
#      that folder to the office laptop -- after that, tiktoken never needs
#      the network again on either machine.
#   2. If the cache is missing AND the network call fails, fall back to a
#      simple chars/4 estimate -- honestly approximate rather than a fake
#      precise-looking number, with a loud warning so you know it happened.
#
# IMPORTANT ACCURACY CAVEAT: cl100k_base is OpenAI's tokenizer. It is only an
# APPROXIMATION for Qwen3/Mistral/Llama/Devstral -- each of those model
# families has its own tokenizer, which will count differently (sometimes by
# a wide margin, especially for non-English text or code). For anything where
# an exact count actually matters (hard context-limit enforcement, precise
# cost accounting), prefer the token counts the API itself returns in
# response.usage.prompt_tokens / response.usage.completion_tokens over any
# client-side estimate -- that reflects what the serving model actually did,
# not an approximation of it.

os.environ.setdefault("TIKTOKEN_CACHE_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), ".tiktoken_cache"))

_tiktoken_encoding_cache = None
_tiktoken_warned = False


def count_tokens_approx(text: str) -> int:
    """
    Best-effort token count for budgeting/chunking decisions. NOT authoritative
    for any model other than OpenAI's -- see the accuracy caveat above. Falls
    back to a chars/4 heuristic (clearly approximate, not a fake-precise
    number) if tiktoken's encoding file isn't cached and can't be fetched.
    """
    global _tiktoken_encoding_cache, _tiktoken_warned

    if _tiktoken_encoding_cache is None:
        try:
            import tiktoken
            _tiktoken_encoding_cache = tiktoken.get_encoding("cl100k_base")
        except Exception as e:
            if not _tiktoken_warned:
                print(f"[llm_provider] tiktoken encoding unavailable ({e}) -- falling back to "
                      f"a chars/4 estimate. Populate TIKTOKEN_CACHE_DIR from a machine with "
                      f"internet access to fix this properly. This estimate is rough regardless "
                      f"-- prefer response.usage from the API for anything that must be exact.",
                      file=sys.stderr)
                _tiktoken_warned = True
            _tiktoken_encoding_cache = False  # cache the failure, don't retry every call

    if _tiktoken_encoding_cache is False:
        return max(1, len(text) // 4)
    return len(_tiktoken_encoding_cache.encode(text))


def print_env_info():
    print(f"[llm_provider] CURRENT_ENV = {CURRENT_ENV!r}")
    if CURRENT_ENV == "office":
        print("[llm_provider] Office models available:", list(_OFFICE_BASE_URL_BY_MODEL))
        print("[llm_provider] Task presets:", OFFICE_TASK_MAP)
        print("[llm_provider] HF_HUB_OFFLINE =", os.environ.get("HF_HUB_OFFLINE"))
    else:
        print("[llm_provider] base_url =", PERSONAL_API_BASE or "(OpenAI default)")
        print("[llm_provider] Task presets:", PERSONAL_MODEL_MAP)


if __name__ == "__main__":
    print_env_info()
