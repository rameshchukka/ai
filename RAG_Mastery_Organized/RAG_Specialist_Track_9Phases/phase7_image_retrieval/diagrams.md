# Phase 7 — Diagrams

## 1. Two parallel paths to "searchable image"

```
   Image file
       |
   ┌───┴───┐
   v       v
  OCR    CLIP image encoder (HF)
   |       |
   v       v
 text   image vector
   |     (in CLIP's joint
   v      text-image space)
 Jina text
 embedding
   |
   v
 text vector
 (in Jina's space,
  UNRELATED to CLIP's space)
```

## 2. CLIP's actual superpower: shared text-image space

```
  CLIP text encoder("a diagram of a payment flow") ──┐
                                                        ├──> SAME vector space
  CLIP image encoder(payment_flow_diagram.png)  ──────┘

  This is why you can search images with a plain text query — but ONLY
  if both the query and the images go through CLIP's own encoders.
  Mixing CLIP's image vectors with a DIFFERENT model's text vectors
  (e.g. Jina) breaks this property entirely — see concept_notes.md teaser.
```

## 3. Linking images to surrounding text via metadata, not a shared model

```
  Chroma collection "doc_text" (Jina embeddings)        Chroma collection
       chunk: "...see the architecture                  "doc_images" (CLIP)
       diagram below for the full                              |
       request flow..."                                  image: architecture_diagram.png
       metadata: {doc_id: "doc_42",                       metadata: {doc_id: "doc_42",
                  section: "Architecture"}                           section: "Architecture"}

  Query text -> finds the paragraph -> read metadata.doc_id + section
             -> separately query doc_images WHERE doc_id="doc_42" AND
                section="Architecture" -> retrieve the linked image
  (the link is the shared metadata field, not a shared embedding space)
```

## 4. Use-case → approach decision tree

```
        What matters most about this image?
                      |
        ┌─────────────┼─────────────┐
        v                            v
   Exact text content          Visual layout/shape
   (error message,             (architecture diagram,
    error code)                 UI screenshot structure)
        |                            |
        v                            v
   OCR + text embedding         CLIP image embedding
   (in-house Jina, no HF)       (Hugging Face CLIP)

        Need both? -> store both, in SEPARATE collections,
                      linked by shared metadata (diagram 3)
```
