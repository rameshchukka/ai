"""
test_gemini_multimodal.py
Sends test_image.png, test_audio.wav, and test_video.mp4 to Gemini and asks it
to describe each one. Compare the output against GROUND_TRUTH.md to actually
grade accuracy, not just check that something came back.

Setup:
    pip install google-genai python-dotenv
    export GEMINI_API_KEY=your-key-here     (or use a .env file, see Lab 1)

Run: python test_gemini_multimodal.py

Note: all 3 files here are small enough to send inline. If you swap in your
own larger files (a real photo, a longer recording), files over ~20MB need
Gemini's File API (client.files.upload()) instead of inline bytes - see the
commented alternative at the bottom of this script.
"""

import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash"


def describe_image():
    print("=" * 60)
    print("IMAGE TEST: test_image.png")
    print("=" * 60)
    with open("test_image.png", "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
            "Describe every shape in this image, its color, and its approximate "
            "position. Also transcribe any text you see exactly as written.",
        ],
    )
    print(response.text)
    print()


def describe_audio():
    print("=" * 60)
    print("AUDIO TEST: test_audio.wav")
    print("=" * 60)
    with open("test_audio.wav", "rb") as f:
        audio_bytes = f.read()

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"),
            "Transcribe this audio exactly. Then separately state: what number "
            "is mentioned, and what is the speaker asking for?",
        ],
    )
    print(response.text)
    print()


def describe_video():
    print("=" * 60)
    print("VIDEO TEST: test_video.mp4")
    print("=" * 60)
    with open("test_video.mp4", "rb") as f:
        video_bytes = f.read()

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=video_bytes, mime_type="video/mp4"),
            "Describe what happens in this video over time - list each visual "
            "change in order. Then separately transcribe the narration audio.",
        ],
    )
    print(response.text)
    print()


if __name__ == "__main__":
    describe_image()
    describe_audio()
    describe_video()
    print("Now compare each response against GROUND_TRUTH.md and check off the "
          "grading checklist items for each file.")


# --- For larger files (>20MB), use the File API instead of inline bytes: ---
#
# uploaded = client.files.upload(file="your_large_video.mp4")
# response = client.models.generate_content(
#     model=MODEL,
#     contents=[uploaded, "Describe this video."],
# )
