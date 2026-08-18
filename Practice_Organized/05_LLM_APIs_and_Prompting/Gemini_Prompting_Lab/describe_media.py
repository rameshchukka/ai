"""
describe_media.py
Point this at ANY of your own image, audio, or video files and get Gemini's
description - no need to rename your files or match the synthetic test set.

Usage:
    python describe_media.py path/to/your/file.jpg
    python describe_media.py path/to/your/file.mp3 --prompt "Transcribe this exactly"
    python describe_media.py path/to/your/file.mp4 --prompt "List every scene change with a timestamp"

Setup:
    pip install google-genai python-dotenv
    export GEMINI_API_KEY=your-key-here     (or use a .env file)

Notes:
- Files under ~20MB are sent inline (fast, simple). Larger files automatically
  use Gemini's File API instead (upload once, reference by handle) - this
  script handles that switch for you, see USE_FILE_API_ABOVE_MB below.
- Supported formats are broad but not unlimited. Common ones:
    Images: .png .jpg .jpeg .webp .heic .heif
    Audio:  .wav .mp3 .aac .flac .ogg .m4a
    Video:  .mp4 .mov .avi .webm .mpeg .3gp
  If your file's extension isn't in MIME_TYPES below, add it - Gemini just
  needs the correct mime_type string, which is usually easy to look up.
"""

import os
import sys
import argparse
import mimetypes
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

MODEL = "gemini-2.5-flash"
USE_FILE_API_ABOVE_MB = 20  # Gemini's inline-bytes limit is around here

# Explicit overrides for formats Python's built-in mimetypes module sometimes
# gets wrong or doesn't know about. Add to this dict if you hit an unsupported
# format error.
MIME_TYPES = {
    ".heic": "image/heic",
    ".heif": "image/heif",
    ".m4a": "audio/mp4",
    ".3gp": "video/3gpp",
    ".wav": "audio/wav",  # Python's mimetypes returns "audio/x-wav" - Gemini wants "audio/wav"
}

DEFAULT_PROMPTS = {
    "image": (
        "Describe everything visible in this image in detail: objects, people, "
        "colors, positions, and any visible text (transcribe text exactly)."
    ),
    "audio": (
        "Transcribe this audio exactly. Then separately summarize what it's about "
        "and note the speaker's apparent tone/intent."
    ),
    "video": (
        "Describe what happens in this video over time - list each significant "
        "visual change or event in order, with approximate timestamps if you can. "
        "Then separately transcribe or summarize any audio/narration."
    ),
}


def guess_mime_type(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()
    if ext in MIME_TYPES:
        return MIME_TYPES[ext]
    mime_type, _ = mimetypes.guess_type(filepath)
    if mime_type is None:
        raise ValueError(
            f"Couldn't guess a MIME type for '{filepath}'. Add an entry for '{ext}' "
            f"to the MIME_TYPES dict at the top of this script."
        )
    return mime_type


def get_media_category(mime_type: str) -> str:
    if mime_type.startswith("image/"):
        return "image"
    if mime_type.startswith("audio/"):
        return "audio"
    if mime_type.startswith("video/"):
        return "video"
    raise ValueError(f"Unsupported media category for mime type '{mime_type}'")


def describe_media(filepath: str, prompt: str = None) -> str:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No such file: {filepath}")

    mime_type = guess_mime_type(filepath)
    category = get_media_category(mime_type)
    final_prompt = prompt or DEFAULT_PROMPTS[category]

    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    print(f"File: {filepath}")
    print(f"Detected type: {mime_type} ({category}), {size_mb:.2f} MB")
    print(f"Prompt: {final_prompt}\n")

    if size_mb <= USE_FILE_API_ABOVE_MB:
        with open(filepath, "rb") as f:
            data = f.read()
        response = client.models.generate_content(
            model=MODEL,
            contents=[
                types.Part.from_bytes(data=data, mime_type=mime_type),
                final_prompt,
            ],
        )
    else:
        # File API: upload once, then reference the handle - required above
        # the inline size limit, and also more efficient if you plan to ask
        # multiple questions about the same file.
        print(f"File is over {USE_FILE_API_ABOVE_MB}MB - uploading via File API...")
        uploaded = client.files.upload(file=filepath)
        response = client.models.generate_content(
            model=MODEL,
            contents=[uploaded, final_prompt],
        )

    return response.text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Describe an image, audio, or video file using Gemini.")
    parser.add_argument("filepath", help="Path to your image/audio/video file")
    parser.add_argument(
        "--prompt",
        help="Custom prompt to send along with the file (default: a general description prompt)",
        default=None,
    )
    args = parser.parse_args()

    try:
        result = describe_media(args.filepath, args.prompt)
        print("=" * 60)
        print("GEMINI'S RESPONSE")
        print("=" * 60)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
