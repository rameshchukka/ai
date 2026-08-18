# Ground Truth — Multimodal Test Files

Use this to actually **grade** Gemini's descriptions, rather than just eyeballing whether
they sound plausible. This is the same "known answer" testing principle from Week 14's
few-shot exercise and Week 17's eval sets — applied here to multimodal input.

## `test_image.png`
- **1 red circle**, top-left area, black outline
- **1 blue square**, top-right area, black outline
- **1 green triangle**, bottom-center area, black outline
- **Text reading exactly:** `FDE LAB TEST 42`
- White background, 600×400 pixels

**Grading checklist for Gemini's response:**
- [ ] Correctly identifies all 3 shapes
- [ ] Correctly identifies all 3 colors
- [ ] Correctly identifies relative positions (top-left / top-right / bottom-center)
- [ ] Correctly reads the text verbatim (this is the OCR-accuracy check — a common failure
      point is getting the numbers wrong, e.g. "24" instead of "42")

## `test_audio.wav`
- **Duration:** ~9 seconds
- **Exact spoken transcript:** *"This is a test recording for the FDE course. The order
  number is 4 2 7 7. Please confirm the shipment has arrived."*
- Synthesized speech (espeak-ng), mono, 22050 Hz — note this is a robotic TTS voice, not a
  natural human voice, so treat it as a baseline test, not a realistic customer-call
  simulation

**Grading checklist for Gemini's response:**
- [ ] Correctly transcribes the core sentence content
- [ ] Correctly extracts the order number as **4277** (digit-extraction accuracy — a good
      test of whether the model handles spoken-digit sequences correctly)
- [ ] Correctly identifies the intent/purpose (requesting shipment confirmation)

## `test_video.mp4`
- **Duration:** ~14.5 seconds, 4 visual frames (H.264 video + AAC audio)
- **Visual sequence (known ground truth):**
  1. Frame 1 (~0-3.6s): empty white scene with caption text
  2. Frame 2 (~3.6-7.3s): a red circle appears
  3. Frame 3 (~7.3-10.9s): a blue square is added (red circle still present)
  4. Frame 4 (~10.9-14.5s): a green triangle is added (all 3 shapes now present)
- **Exact spoken narration:** *"Frame one. Empty scene. Frame two. A red circle appears.
  Frame three. A blue square is added. Frame four. A green triangle completes the set.
  This is the FDE video test."*

**Grading checklist for Gemini's response:**
- [ ] Correctly identifies the temporal sequence (shapes appearing progressively, not just
      "there are 3 shapes" as a static description)
- [ ] Correctly reports the final state (all 3 shapes present at the end)
- [ ] Correctly transcribes/summarizes the narration content
- [ ] Correctly connects the visual sequence to the narration (i.e., understands both
      modalities describe the *same* progression, not two unrelated things)

---

## Why this matters for FDE work
This is the same discipline from Week 17 (Evaluation & Guardrails) applied to multimodal
input: you can't tell if a model's description is *good* just by reading it — it has to be
checked against a known answer. When you eventually build a real multimodal feature for a
client (e.g., extracting data from scanned documents, transcribing support call audio),
this is exactly the kind of test-case-with-known-ground-truth you'd build into your eval
suite before calling anything production-ready.
