# Ingestion Process — Manual curl → Bulk Script → Load Test

## Prerequisites
- A Chroma server running and reachable, e.g. `chroma run --path ./chroma_data --port 8000`
- Your in-house Jina embedding endpoint — now known exactly from your real
  `inhouse_llm.py`: `{API_BASE_JINA}/embeddings`, authenticated with
  `Authorization: Bearer {API_KEY}`. No more guessing at the shape.
- `jq` installed for the curl examples (`brew install jq` on Mac) — makes parsing JSON
  responses in a terminal bearable.

## Why this is 4 steps, not 3
Chroma's v2 REST API addresses collections by **UUID**, not by name, in the add/query
paths. So the full pipeline is:

```
1. Resolve collection name -> UUID        (one-time per collection, or cache it)
2. Embed the text                          (call {API_BASE_JINA}/embeddings)
3. POST the embedding + metadata to Chroma  (the actual "add")
4. (later) POST a query embedding to search the same collection
```

## Step-by-step: manual curl (do this first, on 2-3 rows, before scripting anything)
See `ingestion/manual_curl_examples.sh` for the literal commands. Walk through it
top to bottom by hand — copy-paste each curl one at a time and read the actual JSON
response before moving to the next. This is the part that builds real intuition for
what's happening at the protocol level; don't skip straight to the bulk script.

What you're confirming by hand:
- The tenant/database/collection-list call actually returns your collection's UUID
- The embedding endpoint's response shape — confirmed: `{"data": [{"embedding": [...]}, ...]}` (OpenAI-style), per `get_embeddings()` in your real `inhouse_llm.py`. Run the curl yourself anyway — confirming it firsthand beats trusting a doc, and it's the whole point of this step.
- The add call returns `200`/`201` with no error body
- A query call against the same collection returns your just-added row as the top hit

## Step-by-step: bulk load from Excel
Once the manual version works, move to `ingestion/bulk_ingest_from_excel.ipynb`. It:
1. Reads `dataset/practice_dataset.xlsx` with pandas
2. Resolves the collection UUID once (cached for the rest of the run)
3. **Batches** the embedding calls (many texts per HTTP call, if your embedding
   endpoint supports a list input — most do) instead of one call per row
4. **Batches** the Chroma add call (arrays of ids/embeddings/documents/metadatas in
   one POST) in chunks (e.g. 20 rows per request) instead of one row per request
5. Verifies the final collection count matches the row count
6. Runs a few sanity queries (one per cluster) and prints top-k results to eyeball

**Why batch instead of looping curl-style per row:** with 55 rows that's barely a
difference, but on a real corpus of thousands of chunks, one HTTP round-trip per row
is the difference between an ingestion job that takes minutes vs. hours. Get the
batching habit now, while the dataset is small enough to debug easily.

## Step-by-step: load testing with JMeter (do this last, after ingestion is verified correct)
See `ingestion/jmeter_load_test.jmx`. Open it in JMeter (GUI mode is fine for this —
`jmeter` with no args, then File > Open). It has two independent Thread Groups:

- **Ingestion Load** — repeatedly embeds + adds rows from a CSV, with configurable
  thread count and loop count, to see how the embedding endpoint and Chroma's add
  endpoint hold up under concurrent writers.
- **Query Load** — repeatedly queries the collection with a fixed embedding vector
  (reading from a CSV) to isolate **query** throughput/latency from **ingestion**
  throughput/latency — these are different load profiles in a real system (writes
  are bursty/batchy, queries are constant/concurrent), so it's worth measuring them
  separately rather than assuming one number describes both.

Before running: edit the `HOST`/`PORT`/`TENANT`/`DATABASE`/`COLLECTION_ID` User
Defined Variables at the top of the test plan to match your actual server, and
replace the placeholder vector in `jmeter_query_vector.csv` with a real embedding
(generate one from the conceptual intuition notebook and paste it in — the placeholder
is structurally correct but not a real semantic vector).

Read the **Summary Report** listener's output after a run: average/p95 latency and
error % per sampler are the numbers worth tracking run over run as you change thread
count, not just "did it finish."
