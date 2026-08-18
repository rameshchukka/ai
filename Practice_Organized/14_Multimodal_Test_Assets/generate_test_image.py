"""
generate_test_image.py
Builds test_image.png: a synthetic scene with KNOWN, countable content -
3 colored shapes (red circle, blue square, green triangle) and a text label -
so you can objectively check whether Gemini's description is accurate,
not just plausible-sounding.

Run: python generate_test_image.py
"""

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 600, 400
img = Image.new("RGB", (WIDTH, HEIGHT), color="white")
draw = ImageDraw.Draw(img)

# Red circle, top-left
draw.ellipse([50, 50, 200, 200], fill="red", outline="black", width=3)

# Blue square, top-right
draw.rectangle([400, 50, 550, 200], fill="blue", outline="black", width=3)

# Green triangle, bottom-center
draw.polygon([(300, 380), (220, 250), (380, 250)], fill="green", outline="black", width=3)

# Text label (known ground truth for OCR-style testing)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
except Exception:
    font = ImageFont.load_default()
draw.text((150, 300), "FDE LAB TEST 42", fill="black", font=font)

img.save("test_image.png")
print("Created test_image.png")
print("Ground truth: 1 red circle (top-left), 1 blue square (top-right),")
print("1 green triangle (bottom-center), text reading 'FDE LAB TEST 42'")
