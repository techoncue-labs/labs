#!/usr/bin/env python3
"""Create the made-up "Sunny Bakery" test site used in this guide.

It has three deliberate problems to find with Chrome DevTools MCP:
  1. a script error (the click handler looks for a button id that does not exist),
  2. a missing image (rolls.png is never created, so it returns 404),
  3. an oversized hero image (3200 px wide, shown at 560 px) that slows the page down.

Usage:  pip install pillow && python3 make_site.py [output_dir]   (default: ./site)
Then:   cd site && python3 -m http.server 8080
"""
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

INDEX_HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sunny Bakery</title>
<style>
body{margin:0;font-family:Arial,sans-serif;background:#fffaf2;color:#3b2a1a}
header{background:#f6b73c;padding:22px 40px;font-size:30px;font-weight:bold}
main{padding:30px 40px;display:flex;gap:40px;align-items:flex-start}
.hero{width:560px;height:360px;border-radius:16px;object-fit:cover;background:#eee}
h1{font-size:44px;margin:0 0 12px} p{font-size:21px;line-height:1.5;max-width:520px}
button{font-size:22px;padding:12px 26px;border:0;border-radius:10px;background:#c0392b;color:#fff;cursor:pointer}
.menu{display:flex;gap:18px;margin-top:22px} .menu img{width:120px;height:90px;border-radius:10px;background:#f1e3cf}
</style></head>
<body>
<header>Sunny Bakery</header>
<main>
  <img class="hero" src="hero.jpg" alt="Fresh bread on a table">
  <div>
    <h1>Fresh bread every morning</h1>
    <p>Sourdough, croissants and cinnamon rolls, baked before sunrise. Order online and pick up on your way to work.</p>
    <button id="order">Order now</button>
    <div class="menu"><img src="croissant.png" alt="Croissant"><img src="rolls.png" alt="Cinnamon rolls"></div>
  </div>
</main>
<script>
  // deliberate bug: the script looks for a button id that does not exist
  document.getElementById('order-button').addEventListener('click', () => alert('Thanks!'));
</script>
</body></html>
"""


def hero(width, height, seed=7):
    """A warm, noisy 'photo-like' picture. The noise keeps the JPEG large, like a real photo."""
    rnd = random.Random(seed)
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):  # vertical warm gradient
        t = y / height
        draw.line([(0, y), (width, y)], fill=(int(240 - 90 * t), int(200 - 90 * t), int(140 - 80 * t)))
    for _ in range(60):  # "loaves"
        x, y = rnd.randrange(width), rnd.randrange(height)
        r = rnd.randrange(width // 30, width // 10)
        draw.ellipse([x - r, y - r // 2, x + r, y + r // 2],
                     fill=(rnd.randrange(150, 210), rnd.randrange(90, 140), rnd.randrange(40, 80)))
    noise = Image.effect_noise((width, height), 40).convert("RGB")
    return Image.blend(img.filter(ImageFilter.GaussianBlur(2)), noise, 0.18)


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(INDEX_HTML, encoding="utf-8")
    big = hero(3200, 2080)
    big.save(out / "hero.jpg", quality=92)                                           # the slow, oversized one
    big.resize((1120, 728), Image.LANCZOS).save(out / "hero-small.jpg", quality=85)  # the fix
    Image.new("RGB", (120, 90), (232, 176, 88)).save(out / "croissant.png")
    # rolls.png is intentionally NOT created (the 404 bug)
    print(f"Site written to {out.resolve()}")
    for f in sorted(out.iterdir()):
        print(f"  {f.name:16} {f.stat().st_size / 1024:8.0f} KB")


if __name__ == "__main__":
    main()
