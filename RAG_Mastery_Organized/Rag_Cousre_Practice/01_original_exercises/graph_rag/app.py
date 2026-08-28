import os
import gradio as gr
from rag_orchestrator import RAGOrchestrator
from validator import RAGValidator, format_validation_report

rag = RAGOrchestrator()
validator = RAGValidator(
    api_key=rag.config.gemini_api_key,
    llm_model=rag.config.generation_model,
    embedding_model=rag.config.embedding_model,
)


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

def upload_and_process_pdf(pdf_file):
    if pdf_file is None:
        return "Please upload a PDF file.", _db_status()
    try:
        result = rag.process_and_store_pdf(pdf_file)
        if result["success"]:
            s = result["statistics"]
            msg = (
                f"**PDF processed successfully.**\n\n"
                f"- Chunks created: {result['chunks_processed']}\n"
                f"- Avg chunk size: {s['avg_chunk_size']} chars\n"
                f"- Total chars: {s['total_chars']}"
            )
        else:
            msg = f"Processing failed: {result['message']}"
        return msg, _db_status()
    except Exception as e:
        return f"Error: {e}", _db_status()


def query_rag(question, top_k):
    if not question.strip():
        return "Please enter a question.", ""
    try:
        result = rag.query(question, top_k=int(top_k))
        answer_md = f"**Answer:**\n\n{result['answer']}"

        sources_md = "**Sources:**\n\n"
        for i, s in enumerate(result["sources"], 1):
            sources_md += (
                f"**{i}. {s['source']}** (chunk {s['chunk_index']}) — "
                f"similarity {s['similarity']:.4f}\n> {s['text'][:200]}...\n\n"
            )
        return answer_md, sources_md
    except Exception as e:
        return f"Error: {e}", ""


def validate_query(question, reference, top_k):
    """Run a full RAG query then evaluate it with RAGAS."""
    if not question.strip():
        return "Please enter a question.", "", ""
    try:
        result = rag.query(question, top_k=int(top_k))
        answer = result["answer"]

        contexts = []
        for s in result["sources"]:
            contexts.append(s["text"])

        ref = reference.strip() or None

        scores = validator.validate(
            question=question, answer=answer, contexts=contexts, reference=ref
        )
        report = format_validation_report(scores)

        answer_md = f"**Answer:**\n\n{answer}"
        return answer_md, report, _db_status()
    except Exception as e:
        return f"Error: {e}", "", _db_status()


def _db_status():
    try:
        info = rag.get_database_info()

        if info["documents"]:
            doc_lines = []
            for d in info["documents"]:
                doc_lines.append(f"  - {d}")
            docs = "\n".join(doc_lines)
        else:
            docs = "  (none)"

        return (
            f"**Database Status**\n\n"
            f"- Documents: {info['total_documents']}\n"
            f"- Chunks: {info['total_chunks']}\n\n"
            f"**Indexed files:**\n{docs}"
        )
    except Exception as e:
        return f"Error: {e}"


def delete_doc(name):
    if not name.strip():
        return "Please enter a document name.", _db_status()
    try:
        rag.delete_document(name.strip())
        return f"Deleted: {name}", _db_status()
    except Exception as e:
        return f"Error: {e}", _db_status()


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

with gr.Blocks(title="GraphRAG — PDF Knowledge Base") as demo:

    gr.Markdown("# GraphRAG — PDF Knowledge Base\nPowered by Gemini + Neo4j + RAGAS")

    with gr.Tabs():

        # ── Tab 1: Upload ──────────────────────────────────────────────
        with gr.Tab("Upload Documents"):
            with gr.Row():
                with gr.Column(scale=2):
                    pdf_input = gr.File(label="PDF File", file_types=[".pdf"], type="filepath")
                    upload_btn = gr.Button("Process PDF", variant="primary")
                with gr.Column(scale=1):
                    db_status_upload = gr.Markdown(_db_status())
            upload_status = gr.Markdown()
            upload_btn.click(
                upload_and_process_pdf,
                inputs=[pdf_input],
                outputs=[upload_status, db_status_upload],
            )

        # ── Tab 2: Query ───────────────────────────────────────────────
        with gr.Tab("Query Knowledge Base"):
            question_q = gr.Textbox(label="Question", lines=2,
                                    placeholder="Ask anything about your documents…")
            top_k_q = gr.Slider(1, 10, value=5, step=1, label="Top-K chunks")
            query_btn = gr.Button("Search", variant="primary")
            answer_out = gr.Markdown(label="Answer")
            sources_out = gr.Markdown(label="Sources")
            query_btn.click(query_rag, [question_q, top_k_q], [answer_out, sources_out])
            gr.Examples(
                [["What are the main topics?"], ["Summarise the key findings."]],
                inputs=question_q,
            )

        # ── Tab 3: Validate (RAGAS) ────────────────────────────────────
        with gr.Tab("Validate (RAGAS)"):
            gr.Markdown(
                "Run a query and automatically evaluate it with **RAGAS** metrics.\n\n"
                "| Metric | Needs reference? | Meaning |\n"
                "|---|---|---|\n"
                "| Faithfulness | No | Answer grounded in context? |\n"
                "| Answer Relevancy | No | Answer addresses the question? |\n"
                "| Context Precision | Yes | Top chunks most relevant? |\n"
                "| Context Recall | Yes | Context covers the ground truth? |"
            )
            question_v = gr.Textbox(label="Question", lines=2)
            reference_v = gr.Textbox(
                label="Reference answer (optional — enables Precision & Recall)",
                lines=2,
                placeholder="Leave blank to skip Precision / Recall metrics.",
            )
            top_k_v = gr.Slider(1, 10, value=5, step=1, label="Top-K chunks")
            validate_btn = gr.Button("Run & Validate", variant="primary")
            val_answer = gr.Markdown(label="Generated Answer")
            val_report = gr.Markdown(label="RAGAS Scores")
            val_db = gr.Markdown()
            validate_btn.click(
                validate_query,
                inputs=[question_v, reference_v, top_k_v],
                outputs=[val_answer, val_report, val_db],
            )

        # ── Tab 4: Manage DB ───────────────────────────────────────────
        with gr.Tab("Manage Database"):
            with gr.Row():
                with gr.Column():
                    db_status_mgmt = gr.Markdown(_db_status())
                    refresh_btn = gr.Button("Refresh")
                with gr.Column():
                    delete_input = gr.Textbox(label="Document name to delete")
                    delete_btn = gr.Button("Delete", variant="stop")
                    delete_status = gr.Markdown()
            refresh_btn.click(_db_status, outputs=[db_status_mgmt])
            delete_btn.click(delete_doc, [delete_input], [delete_status, db_status_mgmt])

        # ── Tab 5: System Info ─────────────────────────────────────────
        with gr.Tab("System Info"):
            gr.Markdown(f"""
### Configuration

| Setting | Value |
|---|---|
| Embedding model | `{rag.config.embedding_model}` |
| Generation model | `{rag.config.generation_model}` |
| Neo4j URI | `{rag.config.neo4j_uri}` |
| Database | `{rag.config.neo4j_database}` |
| Min chunk length | {rag.config.chunk_min_length} chars |
| Default top-K | {rag.config.top_k_results} |
| Max retries | {rag.config.max_retries} |

### RAGAS Validation
- **Faithfulness** and **Answer Relevancy** run on every validation (no ground truth needed).
- Add a **Reference answer** to also compute **Context Precision** and **Context Recall**.
- All metrics are scored 0–1 (higher is better).
""")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, show_error=True)
