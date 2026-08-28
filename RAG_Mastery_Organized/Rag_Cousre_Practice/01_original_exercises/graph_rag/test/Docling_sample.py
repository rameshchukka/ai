from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.document_converter import PdfFormatOption
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from docling.datamodel.pipeline_options import PdfPipelineOptions

# 1. Configure converter
pipeline_options = PdfPipelineOptions(do_ocr=False, do_table_structure=True)
format_opts = {
    InputFormat.PDF: PdfFormatOption(
        pipeline_options=pipeline_options,
        # You could choose a custom backend here if needed
    )
}

converter = DocumentConverter(
    allowed_formats=[InputFormat.PDF],
    format_options=format_opts
)

# 2. Convert a document
result = converter.convert(r"H:\01_Training\ContentSlides_AgenticAI\Code\ERP-2008-chapter4.pdf")

# 3. Work with the DoclingDocument
doc = result.document  # This is a DoclingDocument object
doc.print_element_tree()  # (for example) print the structure
for item, level in doc.iterate_items():
    print("Level:", level, "Item:", item)

# 4. Export as Markdown or JSON
markdown = doc.export_to_markdown()
doc_json = doc.model_dump_json()  # or `export_to_dict()` depending on version
