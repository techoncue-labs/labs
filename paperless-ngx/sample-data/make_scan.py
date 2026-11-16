#!/usr/bin/env python3
"""A made-up 'scanned' paper document (image only, no text layer), so you can watch Paperless-ngx run OCR on it.

Needs Pillow:  pip install pillow
Usage:         python3 make_scan.py   ->  samples/oakridge-boiler-service-scan.pdf
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parent / "samples"
FONT_FILES = {False: ["DejaVuSerif.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", "Georgia.ttf", "times.ttf"],
              True: ["DejaVuSerif-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", "Georgia Bold.ttf", "timesbd.ttf"]}


def font(size, bold=False):
    for f in FONT_FILES[bold]:
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            continue
    return ImageFont.load_default(size)  # Pillow 10.1 or newer


def main():
    random.seed(7)
    W, H = 1654, 2339  # A4 at 200 dpi
    img = Image.new("L", (W, H), 246)
    d = ImageDraw.Draw(img)
    y = 150
    d.text((140, y), "OAKRIDGE HEATING", font=font(64, True), fill=40); y += 90
    d.text((140, y), "Boiler service and repairs  -  Springfield", font=font(30), fill=70); y += 70
    d.line((140, y, W - 140, y), fill=60, width=4); y += 60
    d.text((140, y), "BOILER SERVICE REPORT", font=font(46, True), fill=30); y += 90
    for line in ["Customer: Alex Sample, 12 Example Road, Springfield", "Visit date: 9 October 2026", "Engineer: J. Moreno",
                 "Appliance: gas combi boiler, installed 2019", "", "Work done:", "  - Annual safety check and service",
                 "  - Cleaned the burner and replaced the seal", "  - Pressure topped up to 1.2 bar", "  - Carbon monoxide test: passed",
                 "", "Result: boiler is safe to use.", "Next service due: October 2027", "", "Amount paid: $95.00 (cash)"]:
        d.text((140, y), line, font=font(36), fill=35); y += 62
    y += 60
    d.text((140, y), "Signed:", font=font(36), fill=35)
    d.line([(330 + i * 9, y + 30 + int(18 * math.sin(i / 3.0))) for i in range(40)], fill=50, width=4)
    d.text((140, H - 200), "Made-up sample document for a tutorial. All names and amounts are fictional.", font=font(26), fill=90)
    # scanner look: noise, slight blur, small rotation
    px = img.load()
    for _ in range(60000):
        x, yy = random.randrange(W), random.randrange(H)
        px[x, yy] = max(0, px[x, yy] - random.randrange(40, 120))
    img = img.filter(ImageFilter.GaussianBlur(0.8)).rotate(-1.3, expand=False, fillcolor=210)
    OUT.mkdir(exist_ok=True)
    out = OUT / "oakridge-boiler-service-scan.pdf"
    img.convert("RGB").save(out, resolution=200)
    print("wrote", out)


if __name__ == "__main__":
    main()
