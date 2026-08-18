# Phase 1 — Document Processing

## Why this phase matters
Every RAG pipeline starts with "get text out of a file." Getting this step wrong
(losing table structure, missing headers, garbling encoding) silently degrades
every downstream phase — chunking, embedding, and retrieval can't recover
information that extraction already threw away.

## Format-by-format cheat sheet
| Format | Library | What's tricky about it |
|---|---|---|
| PDF | `pypdf`, `pdfplumber` | Text order isn't guaranteed to match visual layout; tables need special handling (`pdfplumber.extract_tables()`); scanned PDFs need OCR (Phase 7) |
| DOCX | `python-docx` | Tables, headers, and styles live in separate object models — paragraph text alone misses structure |
| PPT | `python-pptx` | Text is scattered across shapes/text frames, not a linear document — slide order ≠ reading order within a slide |
| HTML | `BeautifulSoup`, `lxml` | Need to strip nav/ads/boilerplate; semantic tags (`<table>`, `<h1>`) carry structure worth preserving for chunking |
| Markdown | stdlib + simple parsing, or `markdown-it-py` | Headers are the natural chunk boundary — don't throw this away by stripping to plain text first |
| JSON | stdlib `json` | Nested structure needs a flattening strategy before chunking — decide what a "document" even means in a JSON tree |
| XML | `lxml`, `xml.etree` | Similar to JSON but with namespaces/attributes to handle; XPath is the efficient way to extract repeated structures |
| YAML | `PyYAML` | Mostly config files — usually small enough to treat as one chunk per file or per top-level key |
| CSV | stdlib `csv`, `pandas` | Row-based by nature — almost always wants table-aware chunking (Phase 2), never character-split |
| Excel | `openpyxl`, `pandas` | Multiple sheets, merged cells, formulas vs. values — decide whether you want formula text or computed values |
| OpenAPI/Swagger | `PyYAML`/`json` + manual traversal | Deeply nested but highly structured — ideal candidate for structure-aware chunking (Phase 2), one chunk per endpoint |

## The general extraction pipeline
```
raw file -> format-specific parser -> structured intermediate
   (preserve: headers, tables, lists, code blocks, page/slide numbers)
-> plain text + metadata
   (metadata: source file, page/slide number, section path)
-> ready for Phase 2 chunking
```

The single most common mistake: extracting to plain text too early, throwing away
headers/structure that Phase 2's better chunking strategies depend on. Keep
structure as long as possible; only flatten to plain text at the very last step
before chunking, and even then, preserve structural metadata alongside it.

## Where ChromaDB fits in this phase
Nowhere yet — Phase 1 is purely "get text + structure out of a file." Nothing gets
embedded or stored until after Phase 2 (chunking). The worksheet for this phase
still ends with a ChromaDB step so you can see the full thread from raw file to
stored document, even though the chunking logic itself is intentionally minimal
here (full treatment in Phase 2).

## Teaser problem
> You extract a PDF with `pypdf` and get back one giant text blob — paragraphs
> ran together, table rows got mixed into surrounding prose, and you can't tell
> which page anything came from. What's wrong, and what's the fix?

**Solution:** `pypdf` gives you text in *reading order heuristics*, not true
structure — it doesn't know what a table or paragraph boundary is, only character
positions. Fix: use `pdfplumber` instead for anything with tables (it has
`extract_tables()` specifically), and always extract per-page so you retain page
numbers as metadata — losing the page number is the same kind of silent
information loss that makes debugging retrieval failures much harder later. See
the worksheet for both libraries side by side on the same content.
