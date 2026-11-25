#!/usr/bin/env python3
"""Compose the 25 November 2026 front-page image (1024x1024 PNG).

Written fresh in this session. Layout: dark navy front page, gold masthead,
lead story with a drawn globe, four stories in a 2x2 grid, an "also today"
strip and a sources footer. Output: entry.png next to this file.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (11, 24, 42)
NAVY2 = (17, 34, 58)
NAVY3 = (23, 45, 72)
GOLD = (214, 166, 58)
GOLD_DIM = (150, 118, 48)
WHITE = (246, 243, 236)
MUTED = (172, 186, 200)
RULE = (96, 116, 136)
CARD = (15, 31, 52)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

LEAD = (
    "UKRAINE",
    (96, 165, 220),
    "Zelenskyy confirms Ukraine hit Russian ships",
    "Drones struck a cargo vessel in the Gulf of Finland; "
    "a warship was sunk off Libya.",
)

GRID = [
    ("RIYADH", (231, 76, 60),
     "Houthi drone hits Riyadh's tallest tower",
     "Eleven people wounded, Saudi civil defence says."),
    ("WASHINGTON", (243, 156, 18),
     "CIA and spy chief's office hit by cyber breach",
     "Unclassified data affected, sources tell CNN."),
    ("NEW YORK", (39, 174, 96),
     "Huawei convicted in US trial over Iran business",
     "Jury finds the firm guilty on 10 of 12 counts."),
    ("CONGO", (142, 68, 173),
     "WHO pulls staff out of Ebola hospital",
     "Workers sheltered three days amid fighting in Ituri."),
]

ALSO = [
    "Trump gives Giuliani the Medal of Freedom",
    "NATO to send early-warning jets to Poland",
    "Sydney CBD locked down by gas leak",
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to lines that fit max_w (measured with textlength)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_globe(draw, cx, cy, r):
    """Gold wireframe globe: circle, meridians, parallels."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=4)
    for k in (0.55, 1.0):
        w = int(r * k)
        draw.ellipse([cx - w, cy - r, cx + w, cy + r], outline=GOLD, width=2)
    for dy in (-int(r * 0.5), 0, int(r * 0.5)):
        half = int((r * r - dy * dy) ** 0.5)
        draw.line([cx - half, cy + dy, cx + half, cy + dy], fill=GOLD, width=2)
    # small gold dot marking the Gulf of Finland strike
    draw.ellipse([cx + int(r * 0.42) - 7, cy - int(r * 0.55) - 7,
                  cx + int(r * 0.42) + 7, cy - int(r * 0.55) + 7],
                 fill=(231, 76, 60), outline=WHITE, width=2)


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY2)
    d.text((512, 22), "THE WORLD TODAY", font=font(SERIF_B, 58),
           fill=WHITE, anchor="ma")
    d.text((512, 88), "WEDNESDAY  \u00b7  25 NOVEMBER 2026  \u00b7  ONE IMAGE, THE DAY'S NEWS",
           font=font(SANS_B, 19), fill=GOLD, anchor="ma")
    d.line([48, 118, W - 48, 118], fill=GOLD, width=3)

    # --- lead story ----------------------------------------------------
    lx, ly, lw = 48, 148, 928
    d.rounded_rectangle([lx, ly, lx + lw, ly + 252], radius=14, fill=CARD,
                        outline=RULE, width=2)
    # globe on the right
    draw_globe(d, lx + lw - 118, ly + 126, 92)
    # kicker
    d.text((lx + 28, ly + 22), LEAD[0], font=font(SANS_B, 22), fill=LEAD[1])
    d.line([lx + 28, ly + 56, lx + 28 + 210, ly + 56], fill=LEAD[1], width=3)
    # headline (two lines max)
    head_f = font(SERIF_B, 44)
    lines = wrap(d, LEAD[2], head_f, 640)
    y = ly + 74
    for ln in lines[:2]:
        d.text((lx + 28, y), ln, font=head_f, fill=WHITE)
        y += 54
    deck_f = font(SANS, 24)
    for ln in wrap(d, LEAD[3], deck_f, 640):
        d.text((lx + 28, y + 8), ln, font=deck_f, fill=MUTED)
        y += 32

    # --- 2x2 grid ------------------------------------------------------
    gx, gy = 48, 420
    cw, ch, gap = 452, 200, 20
    for i, (kick, color, head, deck) in enumerate(GRID):
        x = gx + (i % 2) * (cw + gap)
        y = gy + (i // 2) * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=12, fill=CARD,
                            outline=RULE, width=2)
        d.rectangle([x, y, x + 8, y + ch], fill=color)
        d.text((x + 28, y + 18), kick, font=font(SANS_B, 19), fill=color)
        hf = font(SERIF_B, 27)
        yy = y + 50
        for ln in wrap(d, head, hf, cw - 56)[:2]:
            d.text((x + 28, yy), ln, font=hf, fill=WHITE)
            yy += 35
        df = font(SANS, 20)
        for ln in wrap(d, deck, df, cw - 56)[:2]:
            d.text((x + 28, yy + 6), ln, font=df, fill=MUTED)
            yy += 27

    # --- also today ----------------------------------------------------
    ay = 420 + 2 * ch + gap + 6  # 846
    d.line([48, ay, W - 48, ay], fill=RULE, width=2)
    d.text((48, ay + 12), "ALSO TODAY", font=font(SANS_B, 20), fill=GOLD)
    yy = ay + 44
    af = font(SANS, 21)
    for item in ALSO:
        d.text((48, yy), "\u2022", font=af, fill=GOLD)
        d.text((72, yy), item, font=af, fill=WHITE)
        yy += 28

    # --- footer --------------------------------------------------------
    d.line([48, 984, W - 48, 984], fill=RULE, width=1)
    d.text((48, 990), "Sources: Reuters \u00b7 CNN \u00b7 AFP \u00b7 RFE/RL",
           font=font(SANS, 16), fill=MUTED)
    d.text((W - 48, 990), "25 NOV 2026", font=font(SANS_B, 16),
           fill=GOLD, anchor="ra")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
