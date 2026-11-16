#!/usr/bin/env python3
"""Create the made-up test media used in this guide: four short films and a three-episode show.

Everything is generated: fictional titles, our own posters and backdrops (Pillow), our own NFO info files,
an English subtitle file for "The Lantern Keeper", and colourful ffmpeg test clips (VP9/Opus .webm,
so a normal browser can play them directly, without transcoding).

Needs: Python 3, Pillow (pip install pillow), ffmpeg 6.1 or newer with libvpx, libopus and drawtext,
and the DejaVu fonts (Debian/Ubuntu: sudo apt install ffmpeg fonts-dejavu-core).

Usage:  python3 make_media.py [output_dir]   (default: ./media)
Output: <output_dir>/Movies/<Title (Year)>/..., <output_dir>/Shows/Garden Robots (2025)/Season 01/...
"""
import random
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "media").resolve()
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
for _f in (FB, FR):
    if not Path(_f).exists():
        sys.exit(f"Font not found: {_f}. Install the DejaVu fonts (fonts-dejavu-core) or change FB/FR at the top of this script.")
MOVIES = [  # title, year, rating, genre, plot, colours
 ("Captain Pebble", 2024, "G", "Family", "A small round stone dreams of sailing the sea and builds a raft out of leaves.", ("#ffb347", "#ff6f61")),
 ("The Lantern Keeper", 2024, "PG", "Adventure", "On a windy island, a young keeper must relight the old lantern before the storm arrives.", ("#355c7d", "#f8b195")),
 ("Comet Relay", 2023, "PG-13", "Science Fiction", "Four pilots race a message across the solar system before a comet blocks the signal.", ("#0f2027", "#2c5364")),
 ("Midnight Circuit", 2022, "R", "Thriller", "A night-shift engineer finds a city's traffic lights blinking out a code.", ("#141e30", "#8e2de2")),
]
SHOW = ("Garden Robots", 2025, "TV-Y", "Animation", "Three tiny robots look after a backyard garden, one season at a time.", ("#56ab2f", "#a8e063"),
        [("Seeds Day", "The robots plant their very first row of seeds."), ("The Big Rain", "A storm floods the garden and the robots build tiny canals."),
         ("Harvest Party", "Tomatoes are ready, and everyone in the garden is invited.")])

def art(path, w, h, title, sub, cols, big):
    im = Image.new("RGB", (w, h), cols[0]); d = ImageDraw.Draw(im)
    c0, c1 = [tuple(int(c[i:i+2], 16) for i in (1, 3, 5)) for c in cols]
    for y in range(h):
        t = y / h; d.line([(0, y), (w, y)], fill=tuple(int(c0[k] + (c1[k] - c0[k]) * t) for k in range(3)))
    random.seed(title)
    for _ in range(14):
        x, y, r = random.randint(0, w), random.randint(0, h), random.randint(w // 30, w // 7)
        d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 255, 255), width=max(2, w // 200))
    f = ImageFont.truetype(FB, big); fs = ImageFont.truetype(FR, max(18, big // 3))
    words, lines, cur = title.split(), [], ""
    for wd in words:
        if d.textlength((cur + " " + wd).strip(), font=f) > w * 0.86: lines.append(cur); cur = wd
        else: cur = (cur + " " + wd).strip()
    lines.append(cur); y = h * 0.62 - len(lines) * big * 0.6
    for ln in lines:
        d.text(((w - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill="white", stroke_width=max(2, big // 18), stroke_fill=(0, 0, 0)); y += big * 1.15
    d.text(((w - d.textlength(sub, font=fs)) / 2, y + big * 0.2), sub, font=fs, fill="white", stroke_width=2, stroke_fill=(0, 0, 0))
    im.save(path, quality=90)

def film(path, title, sub, cols, secs, seed):
    c0, c1 = cols
    vf = (f"drawtext=fontfile={FB}:text='{title}':fontsize=84:fontcolor=white:borderw=5:bordercolor=black:x=(w-tw)/2:y=(h-th)/2-40,"
          f"drawtext=fontfile={FR}:text='{sub}':fontsize=34:fontcolor=white:borderw=3:bordercolor=black:x=(w-tw)/2:y=(h/2)+60,"
          f"drawtext=fontfile={FR}:text='%{{pts\\:hms}}':fontsize=26:fontcolor=white@0.8:x=w-tw-30:y=h-th-24")
    a = f"aevalsrc='0.06*sin(2*PI*220*t)+0.04*sin(2*PI*330*t)+0.03*sin(2*PI*(440+{seed}*20)*t)':s=48000:d={secs}"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"gradients=s=1280x720:c0={c0}:c1={c1}:c2=#ffffff:n=3:speed=0.02:seed={seed}:d={secs}:r=25",
                    "-f", "lavfi", "-i", a, "-vf", vf, "-c:v", "libvpx-vp9", "-b:v", "900k", "-deadline", "realtime", "-cpu-used", "8", "-row-mt", "1",
                    "-c:a", "libopus", "-b:a", "64k", "-shortest", str(path)], check=True)

def srt(path, lines, step=6):
    out = []
    for i, ln in enumerate(lines):
        a, b = 2 + i * step, 2 + i * step + step - 1
        out.append(f"{i+1}\n00:00:{a:02},000 --> 00:00:{b:02},000\n{ln}\n")
    path.write_text("\n".join(out))

for i, (t, y, r, g, p, cols) in enumerate(MOVIES):
    d = OUT / "Movies" / f"{t} ({y})"; d.mkdir(parents=True, exist_ok=True)
    film(d / f"{t} ({y}).webm", t, "A Tech On Cue test film", cols, 45, i + 1)
    art(d / "poster.jpg", 600, 900, t, f"{y}  ·  {g}", cols, 64); art(d / "backdrop.jpg", 1280, 720, t, "", cols[::-1], 90)
    (d / "movie.nfo").write_text(f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<movie>\n  <title>{t}</title>\n  <year>{y}</year>\n  <plot>{p}</plot>\n  <mpaa>{r}</mpaa>\n  <genre>{g}</genre>\n  <runtime>1</runtime>\n  <lockdata>true</lockdata>\n</movie>\n")
    if t == "The Lantern Keeper":
        srt(d / f"{t} ({y}).en.srt", ["The wind is rising again.", "We have until sunset to light it.", "Hand me the matches, quickly!",
                                      "Look, the ships can see us now.", "The storm is turning away.", "Well done, keeper."])
t, y, r, g, p, cols, eps = SHOW
d = OUT / "Shows" / f"{t} ({y})"; (d / "Season 01").mkdir(parents=True, exist_ok=True)
art(d / "poster.jpg", 600, 900, t, f"{y}  ·  {g}", cols, 64); art(d / "backdrop.jpg", 1280, 720, t, "", cols[::-1], 90)
(d / "tvshow.nfo").write_text(f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<tvshow>\n  <title>{t}</title>\n  <year>{y}</year>\n  <plot>{p}</plot>\n  <mpaa>{r}</mpaa>\n  <genre>{g}</genre>\n  <lockdata>true</lockdata>\n</tvshow>\n")
for k, (et, ep) in enumerate(eps, 1):
    base = d / "Season 01" / f"{t} S01E{k:02}"
    film(base.with_suffix(".webm"), et, f"{t}  ·  Episode {k}", cols, 30, 10 + k)
    art(Path(str(base) + "-thumb.jpg"), 1280, 720, et, f"Episode {k}", cols, 80)
    base.with_suffix(".nfo").write_text(f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<episodedetails>\n  <title>{et}</title>\n  <season>1</season>\n  <episode>{k}</episode>\n  <plot>{ep}</plot>\n  <mpaa>{r}</mpaa>\n  <lockdata>true</lockdata>\n</episodedetails>\n")
print("done", sum(1 for _ in OUT.rglob("*")), "files")
