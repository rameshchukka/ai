"""
Validate RAG answers using RAGAS (https://docs.ragas.io).

We measure 4 things about an answer the RAG system produced:

  1. Faithfulness       -> Is the answer backed by the retrieved text? (no reference needed)
  2. Answer Relevancy   -> Does the answer actually address the question? (no reference needed)
  3. Context Precision  -> Were the top chunks the most relevant ones?    (needs a reference answer)
  4. Context Recall     -> Did the chunks cover the reference answer?      (needs a reference answer)

All scores are between 0 and 1 (higher is better).

How to use:
    v = RAGValidator(api_key="...")
    scores = v.validate(question="...", answer="...", contexts=["chunk1", "chunk2"])
    print(format_validation_report(scores))
"""

import sys
import types
from typing import Dict, List, Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

# --- Compatibility shim (must run BEFORE importing ragas) -----------------
# ragas 0.4.3 tries to import ChatVertexAI from an old langchain-community
# location that newer versions removed. We never use Vertex AI, so we register
# a tiny stand-in module to satisfy that import. Remove this once ragas no
# longer references the old path.
if "langchain_community.chat_models.vertexai" not in sys.modules:
    try:
        import langchain_community.chat_models.vertexai  # noqa: F401
    except ModuleNotFoundError:
        _shim = types.ModuleType("langchain_community.chat_models.vertexai")
        _shim.ChatVertexAI = type("ChatVertexAI", (), {})  # placeholder, never used
        sys.modules["langchain_community.chat_models.vertexai"] = _shim
# --------------------------------------------------------------------------

from ragas import EvaluationDataset, SingleTurnSample, evaluate
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import AnswerRelevancy, ContextPrecision, ContextRecall, Faithfulness


class RAGValidator:
    """Scores a RAG answer with RAGAS metrics, powered by Gemini."""

    def __init__(
        self,
        api_key: str,
        llm_model: str = "gemini-2.5-flash",
        embedding_model: str = "all-mpnet-base-v2",
    ):
        # RAGAS needs an LLM (to judge the answer) and an embedding model
        # (to compare meanings). The LLM is Gemini; the embeddings run locally
        # with the same HuggingFace model the rest of the app uses (no API call).
        llm = LangchainLLMWrapper(
            ChatGoogleGenerativeAI(model=llm_model, google_api_key=api_key)
        )
        embeddings = LangchainEmbeddingsWrapper(
            HuggingFaceEmbeddings(model_name=embedding_model)
        )

        # These two metrics only need the question, answer and context.
        self.metrics_no_reference = [
            Faithfulness(llm=llm),
            AnswerRelevancy(llm=llm, embeddings=embeddings),
        ]
        # These two extra metrics also need a "correct" reference answer.
        self.metrics_with_reference = [
            ContextPrecision(llm=llm),
            ContextRecall(llm=llm),
        ]

    def validate(
        self,
        question: str,
        answer: str,
        contexts: List[str],
        reference: Optional[str] = None,
    ) -> Dict[str, float]:
        """
        Score one (question, answer, contexts) example.

        Pass `reference` (a correct answer) to also get Context Precision and Recall.
        Returns a dict like {"faithfulness": 0.92, "answer_relevancy": 0.85, ...}.
        """
        # Pick which metrics to run based on whether we have a reference answer.
        metrics = self.metrics_no_reference
        if reference:
            metrics = self.metrics_no_reference + self.metrics_with_reference

        # Build the single example RAGAS expects, then evaluate it.
        sample = SingleTurnSample(
            user_input=question,
            response=answer,
            retrieved_contexts=contexts,
            reference=reference,
        )
        dataset = EvaluationDataset(samples=[sample])
        result_row = evaluate(dataset=dataset, metrics=metrics).to_pandas().iloc[0]

        # The result row also contains the inputs we passed in; keep only the scores.
        input_columns = ["user_input", "response", "retrieved_contexts", "reference"]
        scores = {}
        for name, value in result_row.to_dict().items():
            if name not in input_columns:
                scores[name] = float(value)
        return scores


def format_validation_report(scores: Dict[str, float]) -> str:
    """Turn a scores dict into a readable Markdown report with bars and labels."""
    lines = ["### RAGAS Validation Report", ""]
    for metric, score in scores.items():
        filled = round(score * 10)
        bar = "[" + "#" * filled + "-" * (10 - filled) + "]"
        label = _quality_label(score)
        title = metric.replace("_", " ").title()
        lines.append(f"**{title}**: {score:.3f} {bar} — {label}")
    return "\n".join(lines)


def _quality_label(score: float) -> str:
    """Map a 0-1 score to a plain-English quality label."""
    if score >= 0.8:
        return "Excellent"
    if score >= 0.6:
        return "Good"
    if score >= 0.4:
        return "Fair"
    return "Poor"
