from pathlib import Path
from typing import List, Dict, Any
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions


class PDFProcessor:
    def __init__(self, min_chunk_length: int = 20):
        self.min_chunk_length = min_chunk_length

        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False              # text-only PDFs (faster). Set True to read scanned/image PDFs.
        pipeline_options.do_table_structure = False  # skip tables (faster). See below to turn tables on.

        # --- OPTIONAL: also extract TABLES and IMAGES ---------------------
        # Docling can recognise tables and pull out page/figure images.
        # Turning these on makes processing slower, so they are off by default.
        # To enable, uncomment the lines below (and `import` line at the top
        # is already enough — these options live on PdfPipelineOptions):
        #
        #   pipeline_options.do_table_structure = True        # detect tables
        #   pipeline_options.generate_page_images = True      # render each page as an image
        #   pipeline_options.generate_picture_images = True   # crop out each figure/picture
        #   pipeline_options.images_scale = 2.0               # image resolution (higher = sharper)
        # ------------------------------------------------------------------

        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

    def extract_chunks(self, pdf_path: str) -> List[Dict[str, Any]]:
        result = self.converter.convert(pdf_path)
        stem = Path(pdf_path).stem # from filename.pdf extract "filename" to use in chunk IDs
        source = Path(pdf_path).name # will get the actual filename.pdf to store in the chunk metadata
        chunks = []

        try:
            paragraphs = result.document.export_to_markdown().split("\n\n")
            method = "markdown"
        except Exception:
            paragraphs = []
            for elem in result.document.iterate_items():
                if hasattr(elem, "text"):
                    paragraphs.append(elem.text)
            method = "iterate"

        for i, para in enumerate(paragraphs):
            text = para.strip()
            if len(text) >= self.min_chunk_length:
                chunks.append({
                    "id": f"{stem}_chunk_{i}",
                    "text": text,
                    "source": source,
                    "chunk_index": i,
                    "metadata": {"length": len(text), "method": method},
                })

        # --- OPTIONAL: read TABLES from the document ----------------------
        # (Requires pipeline_options.do_table_structure = True in __init__.)
        # Each table is turned into Markdown text and stored as a normal chunk
        # so it becomes searchable just like a paragraph.
        #
        # for t, table in enumerate(result.document.tables):
        #     table_md = table.export_to_markdown()
        #     if len(table_md.strip()) >= self.min_chunk_length:
        #         chunks.append({
        #             "id": f"{stem}_table_{t}",
        #             "text": table_md,
        #             "source": source,
        #             "chunk_index": f"table_{t}",
        #             "metadata": {"length": len(table_md), "method": "table"},
        #         })
        # ------------------------------------------------------------------

        # --- OPTIONAL: save IMAGES from the document ----------------------
        # (Requires generate_page_images / generate_picture_images = True.)
        # Pictures are images, not text, so we save them to disk instead of
        # adding them as text chunks. `picture.image.pil_image` is a PIL image.
        #
        # from pathlib import Path
        # image_dir = Path("extracted_images")
        # image_dir.mkdir(exist_ok=True)
        # for p, picture in enumerate(result.document.pictures):
        #     if picture.image is not None:
        #         out_path = image_dir / f"{stem}_picture_{p}.png"
        #         picture.image.pil_image.save(out_path)
        # ------------------------------------------------------------------

        return chunks

    def get_chunk_statistics(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not chunks:
            return {"total_chunks": 0, "total_chars": 0, "avg_chunk_size": 0}

        sizes = []
        for c in chunks:
            sizes.append(c["metadata"]["length"])

        return {
            "total_chunks": len(chunks),
            "total_chars": sum(sizes),
            "avg_chunk_size": round(sum(sizes) / len(sizes), 2),
            "min_chunk_size": min(sizes),
            "max_chunk_size": max(sizes),
        }
