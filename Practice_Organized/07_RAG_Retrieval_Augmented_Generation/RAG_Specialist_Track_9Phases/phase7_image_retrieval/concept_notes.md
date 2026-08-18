# Phase 7 — Image Retrieval (no video)

## Scope
Image *understanding and retrieval*, not image generation. Four sub-skills:
1. OCR — extract text from images
2. Image embeddings — represent image content as vectors for similarity search
3. Searching diagrams/screenshots
4. Linking images with surrounding documentation

## OCR
| Tool | Notes |
|---|---|
| Tesseract (`pytesseract`) | Open-source, no HF dependency, good for clean screenshots/scanned text |
| Cloud OCR APIs | Better accuracy on messy/handwritten content, but external dependency |

## Image embeddings — CLIP family (Hugging Face, per your go-ahead)
CLIP-family models (`openai/clip-vit-base-patch32` and similar, via
`transformers`/`open_clip` from Hugging Face) embed images and text **into the
same vector space**, so you can search images using a text query directly — no
in-house equivalent exists for this, which is why this is the one sub-skill in
the whole RAG-Specialist track where HF is the primary path rather than an
alternative.

| Approach | How | Trade-off |
|---|---|---|
| CLIP image embedding (HF) | Embed the image directly with CLIP's image encoder | True visual similarity (layout, colors, shapes) — captures things OCR+text-embedding would miss entirely (a screenshot's visual layout, an architecture diagram's shape) |
| OCR + text embedding (in-house, no HF) | OCR the image to text, embed that text with Jina | Works well when the image's *content* is mostly text (error screenshots, text-heavy diagrams); misses pure visual similarity |

Both are legitimate and often used together: CLIP for "find visually similar
diagrams," OCR+text for "find the screenshot that contains this exact error
message."

## Typical enterprise use cases
- Architecture diagrams — CLIP for visual layout similarity
- UI screenshots — both: OCR for text-in-screenshot, CLIP for visual similarity
- API flowcharts — CLIP, since the structure/shape is the meaningful signal
- Error screenshots — OCR is usually sufficient and more precise (exact error text matters more than visual layout)

## Linking images with surrounding documentation
In practice: store the image's embedding (CLIP and/or OCR-derived text
embedding) in Chroma with metadata pointing to the source document and the
surrounding paragraph/section it appeared in — so a text query can retrieve the
image, and an image query can retrieve the surrounding text, via the shared
metadata link rather than needing one model to understand both perfectly.

## Where ChromaDB fits in this phase
Same collection-per-embedding-space rule as Phase 3 applies here too: CLIP
image embeddings and OCR-derived Jina text embeddings are different vector
spaces and belong in separate collections, joined by shared metadata (e.g. a
`source_doc_id`), not mixed into one collection.

## Teaser problem
> You embed both a screenshot's CLIP image-embedding and its OCR'd text's Jina
> embedding into the SAME Chroma collection, hoping a text query will find
> visually similar matches too. Querying with text returns garbage matches
> against the CLIP-embedded images. Why?

**Solution:** same root cause as Phase 3's teaser — two incompatible vector
spaces in one collection. A text query embedded with Jina is being compared
against CLIP image vectors it has no learned relationship to. The fix: two
collections (`screenshots_clip`, `screenshots_ocr_text`), or — better — embed
your *text query* with CLIP's text encoder when you want to search the CLIP
collection (CLIP's whole point is that text and images share one space when
both are encoded by CLIP itself, not by mixing CLIP images with a different
model's text vectors). See the worksheet for the corrected version.
