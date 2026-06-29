"""
inhouse_wrappers.py  (v2 — corrected against your real inhouse_llm.py)
=======================================================================
Changes from the earlier version, and why:

1. Uses LangChain's built-in `ChatOpenAI` directly, per model, instead of a
   custom LLM subclass. Your models are already served via the `openai` SDK
   against custom base_urls -- that IS what ChatOpenAI is for. Less code to
   maintain, and it gets you streaming/tool-calling/etc. for free if your
   serving stack (vLLM or similar) supports those at the HTTP level.

2. Fixes a real bug in inhouse_llm.py: chat()/multimodal_chat() always use
   `client` (bound to the Qwen3-14B endpoint) no matter what `model=` you
   pass. This module routes each model constant to ITS OWN base_url, via
   get_chat_model(model=...), so Mistral/Llama/Devstral/Qwen3-30B/VL actually
   hit their own endpoints.

3. Adds the missing client for the vision model (API_BASE_QWEN2_5_VL_7B had
   no corresponding client object in inhouse_llm.py at all).

4. Fixes the multimodal message format. inhouse_llm.py's multimodal_chat()
   appends the image as a third plain-text message (just the raw base64
   string) -- that is NOT valid OpenAI-compatible vision format and likely
   isn't actually being understood as an image by the serving model. This
   module uses the correct `image_url` content-block format instead.

5. InHouseEmbeddings now calls get_embedding()/get_embeddings() with their
   REAL signature -- no `model=` kwarg, since the embedding endpoint is
   fixed to Jina via API_BASE_JINA. (The earlier version of this wrapper
   incorrectly assumed a `model=` parameter existed on get_embedding().)

Nothing in inhouse_llm.py itself needs to change for this file to work --
this sits alongside it and reuses its config (API_KEY, base_urls, http_client_ssl,
get_embedding/get_embeddings) without modifying it. If you want the underlying
bug actually fixed at the source, see the patch note at the bottom of this file.
"""

from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.embeddings import Embeddings
from langchain_core.messages import SystemMessage, HumanMessage

from inhouse_llm import (
    API_BASE_QWEN3_14B, API_BASE_QWEN3_30B, API_BASE_MISTRAL,
    API_BASE_LLAMA, API_BASE_DEVSTRAL, API_BASE_QWEN2_5_VL_7B,
    MODEL_QWEN3_14B, MODEL_QWEN3_30B, MODEL_MISTRAL,
    MODEL_LLAMA, MODEL_DEVSTRAL, MODEL_QWEN2_5_VL_7B,
    API_KEY, http_client_ssl,
    get_embedding, get_embeddings,
)

# ---------------------------------------------------------------------------
# Model -> its OWN base_url. This is the fix for the routing bug: every
# helper in inhouse_llm.py ignores this and always uses the Qwen3-14B client.
# ---------------------------------------------------------------------------
_BASE_URL_BY_MODEL = {
    MODEL_QWEN3_14B: API_BASE_QWEN3_14B,
    MODEL_QWEN3_30B: API_BASE_QWEN3_30B,
    MODEL_MISTRAL: API_BASE_MISTRAL,
    MODEL_LLAMA: API_BASE_LLAMA,
    MODEL_DEVSTRAL: API_BASE_DEVSTRAL,
    MODEL_QWEN2_5_VL_7B: API_BASE_QWEN2_5_VL_7B,  # no client existed for this one before
}


def get_chat_model(model: str = MODEL_QWEN3_14B, max_tokens: int = 1000, **kwargs) -> ChatOpenAI:
    """
    Returns a LangChain ChatOpenAI instance correctly pointed at the given
    model's own endpoint. Use this instead of inhouse_llm.chat() whenever you
    need a model OTHER than the default Qwen3-14B -- chat()/multimodal_chat()
    in inhouse_llm.py don't route correctly for those.

    Works as a drop-in LangChain chat model: supports .invoke(), .stream(),
    LCEL composition (prompt | get_chat_model(...) | parser), etc.
    """
    base_url = _BASE_URL_BY_MODEL.get(model)
    if base_url is None:
        raise ValueError(f"Unknown model path: {model!r}. Known models: {list(_BASE_URL_BY_MODEL)}")
    return ChatOpenAI(
        base_url=base_url,
        api_key=API_KEY,
        model=model,
        max_tokens=max_tokens,
        http_client=http_client_ssl,  # reuses the same SSL-aware client inhouse_llm.py builds
        **kwargs,
    )


def build_vision_messages(system_prompt: str, user_prompt: str, image_base64: str, image_format: str = "png"):
    """
    Builds correctly-formatted multimodal messages (proper image_url content
    block), unlike inhouse_llm.py's multimodal_chat() which appends raw
    base64 as a third plain-text message. Use with get_chat_model(model=MODEL_QWEN2_5_VL_7B).
    """
    return [
        SystemMessage(content=system_prompt),
        HumanMessage(content=[
            {"type": "text", "text": user_prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/{image_format};base64,{image_base64}"}},
        ]),
    ]


class InHouseEmbeddings(Embeddings):
    """
    Wraps get_embeddings()/get_embedding() from inhouse_llm.py AS-IS --
    these were already correct. No `model=` kwarg here, matching the real
    function signatures (the embedding endpoint is fixed to Jina).
    """
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        result = get_embeddings(texts)
        if result is None:
            raise RuntimeError("get_embeddings() returned None -- check the Jina endpoint/API key.")
        return result

    def embed_query(self, text: str) -> List[float]:
        result = get_embedding(text)
        if result is None:
            raise RuntimeError("get_embedding() returned None -- check the Jina endpoint/API key.")
        return result


# Convenience presets, same intent as before, now returning ChatOpenAI directly
def llm_for(task: str, **kwargs) -> ChatOpenAI:
    """
    task: "chat" | "reasoning" | "code" | "vision" | "judge"
    """
    presets = {
        "chat": MODEL_QWEN3_14B,
        "reasoning": MODEL_QWEN3_30B,
        "code": MODEL_DEVSTRAL,
        "vision": MODEL_QWEN2_5_VL_7B,
        "judge": MODEL_LLAMA,
    }
    if task not in presets:
        raise ValueError(f"Unknown task '{task}'. Choose from {list(presets)}")
    return get_chat_model(model=presets[task], **kwargs)


# ---------------------------------------------------------------------------
# OPTIONAL: a minimal patch to inhouse_llm.py itself, if you'd rather fix it
# at the source than work around it from here. NOT applied automatically --
# shown for reference / to hand to whoever owns that file.
# ---------------------------------------------------------------------------
PATCH_NOTE = """
# Fix for inhouse_llm.py's chat()/multimodal_chat() routing bug:
# add a model -> client lookup, and use it instead of the single `client`.

_CLIENT_BY_MODEL = {
    MODEL_QWEN3_14B: client,
    MODEL_QWEN3_30B: client_qwen3_30b,
    MODEL_MISTRAL: client_mistral,
    MODEL_LLAMA: client_llama,
    MODEL_DEVSTRAL: client_devstral,
    # MODEL_QWEN2_5_VL_7B: client_qwen_vl,  # <- also need to CREATE this client,
    #   it doesn't exist in the current file:
    #   client_qwen_vl = OpenAI(base_url=API_BASE_QWEN2_5_VL_7B, api_key=API_KEY, http_client=http_client_ssl)

def chat(prompt, system_prompt=None, model=CHAT_MODEL, **kwargs):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    target_client = _CLIENT_BY_MODEL.get(model, client)  # falls back to default if unknown
    response = target_client.chat.completions.create(model=model, messages=messages, **kwargs)
    return response.choices[0].message.content

# And for multimodal_chat(), replace the 3-message construction with proper
# image_url content blocks (see build_vision_messages() above for the shape),
# and use _CLIENT_BY_MODEL[model] instead of the hardcoded `client`.
"""
