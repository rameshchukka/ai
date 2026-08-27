# Phase 1 — Diagrams

## 1. The extraction pipeline, all formats funnel to the same shape

```
  PDF ──┐
  DOCX ─┤
  PPT ──┤
  HTML ─┼──> [format-specific parser] ──> structured intermediate
  MD ───┤        (preserve headers,            (text + page/slide/section
  JSON ─┤         tables, lists,                 metadata, NOT yet flattened)
  XML ──┤         code blocks)
  YAML ─┤                                              |
  CSV ──┤                                              v
  XLSX ─┤                                    plain text + metadata
  OpenAPI┘                                   (ready for Phase 2 chunking)
```

## 2. Why "extract to plain text early" loses information

```
 GOOD (structure preserved as long as possible):
 PDF -> [page1: {headings:[...], tables:[...], paragraphs:[...]}, page2: {...}]
            |
            v  (flatten ONLY when handing off to chunker)
 chunker receives text + "this came from page 3, under heading 'Error Codes'"


 BAD (flatten immediately):
 PDF -> "Error Codes 404 Not Found 500 Internal Server Error The request..."
            |
            v
 chunker has no idea where one logical section ends and the next begins,
 because the structural signal was discarded before chunking ever saw it
```

## 3. Format → typical chunk boundary (preview of Phase 2's payoff)

```
        Format                      Natural chunk boundary
        ──────                      ───────────────────────
        PDF (prose)            -->  paragraph / section heading
        DOCX                   -->  heading styles (Heading 1/2/3)
        PPT                    -->  one slide = one chunk (usually)
        HTML                   -->  <h1>-<h6> tags, <section>, <article>
        Markdown               -->  # headers
        JSON / XML / OpenAPI   -->  one logical object/endpoint = one chunk
        CSV / Excel            -->  one row, or one logical row-group
        YAML                   -->  one top-level key
```
