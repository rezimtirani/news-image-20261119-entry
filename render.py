#!/usr/bin/env python3
"""Render the 19 November 2026 world-news infographic.

Reads news.json (researched from Reuters/AP/BBC/Al Jazeera reporting of
19 November 2026) and draws a 1024x1024 PNG to entry.png. Deterministic:
no network, no clock, no randomness -- the same input always yields the
same bytes. Run: python3 render.py
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1024, 1024
NAVY = (14, 42, 71)
GOLD = (201, 162, 39)
GOLD_LIGHT = (232, 196, 92)
PAPER = (247, 243, 234)
CARD = (255, 255, 255)
INK = (26, 32, 40)
MUTED = (84, 94, 106)
RED = (166, 28, 28)
TEAL = (15, 118, 110)
BLUE = (29, 78, 150)
GREEN = (46, 125, 50)
PURPLE = (106, 62, 158)
LINE = (214, 206, 190)


def font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rounded_card(draw, box, fill=CARD, outline=LINE, radius=10):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=2)


def icon_flags(draw, x, y, w, h, color):
    for i, cx in enumerate((x + int(w * 0.2), x + int(w * 0.5), x + int(w * 0.8))):
        draw.line([cx, y + 6, cx, y + h - 6], fill=color, width=5)
        fy = y + 8 + i * 6
        draw.polygon([(cx, fy), (cx + 34, fy + 10), (cx, fy + 22)], fill=color)


def icon_bridge(draw, x, y, w, h, color):
    deck_y = y + int(h * 0.62)
    draw.line([x, deck_y, x + w, deck_y], fill=color, width=6)
    for tx in (x + int(w * 0.18), x + int(w * 0.72)):
        draw.line([tx, y + 8, tx, deck_y], fill=color, width=6)
        draw.line([tx - 12, y + 8, tx + 12, y + 8], fill=color, width=6)
    draw.arc([x + 6, y + int(h * 0.28), x + w - 6, deck_y + 34], 180, 360, fill=color, width=5)
    for fx in range(5):
        fx0 = x + int(w * (0.1 + 0.2 * fx))
        draw.line([fx0, deck_y, fx0, deck_y + 26], fill=color, width=4)


def icon_ballot(draw, x, y, w, h, color):
    bx, by = x + 8, y + int(h * 0.3)
    bw, bh = w - 16, int(h * 0.55)
    draw.rectangle([bx, by, bx + bw, by + bh], outline=color, width=5)
    draw.line([bx, by, bx + int(bw * 0.45), by - 14], fill=color, width=5)
    draw.line([bx + int(bw * 0.45), by - 14, bx + bw, by + 6], fill=color, width=5)
    draw.line([bx + int(bw * 0.3), by + int(bh * 0.55), bx + int(bw * 0.45),
               by + int(bh * 0.75)], fill=color, width=6)
    draw.line([bx + int(bw * 0.45), by + int(bh * 0.75), bx + int(bw * 0.75),
               by + int(bh * 0.3)], fill=color, width=6)


def icon_chart(draw, x, y, w, h, color):
    # rising bars: the record IPO
    base_y = y + h - 8
    bars = [0.35, 0.55, 0.45, 0.75, 1.0]
    bw = w // 6
    for i, frac in enumerate(bars):
        bx0 = x + i * (bw + 4)
        bh = int((h - 16) * frac)
        draw.rectangle([bx0, base_y - bh, bx0 + bw, base_y], fill=color)
    draw.line([x, base_y, x + w, base_y], fill=color, width=4)


def icon_crossing(draw, x, y, w, h, color):
    # a dashed ceasefire line crossed by an arrow
    mid_y = y + h // 2
    for dx in range(0, w, 18):
        draw.line([x + dx, mid_y, x + dx + 10, mid_y], fill=color, width=4)
    ax0, ay0 = x + 8, y + h - 14
    ax1, ay1 = x + w - 14, y + 12
    draw.line([ax0, ay0, ax1, ay1], fill=color, width=6)
    draw.polygon([(ax1, ay1), (ax1 - 18, ay1 + 2), (ax1 - 4, ay1 + 18)], fill=color)


def main():
    with open(os.path.join(HERE, "news.json"), encoding="utf-8") as fh:
        news = json.load(fh)

    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- header ----
    draw.rectangle([0, 0, W, 140], fill=NAVY)
    draw.rectangle([0, 140, W, 146], fill=GOLD)
    draw.text((28, 22), news["title"], font=font(True, 64), fill=(255, 255, 255))
    draw.text((30, 100), news["subtitle"], font=font(False, 23), fill=(205, 216, 228))
    draw.text((996, 24), news["date_lines"][0], font=font(True, 28), fill=GOLD_LIGHT, anchor="ra")
    draw.text((996, 58), news["date_lines"][1], font=font(True, 40), fill=(255, 255, 255), anchor="ra")

    # ---- hero story ----
    hero = news["hero"]
    rounded_card(draw, [24, 158, 1000, 424])
    draw.rounded_rectangle([24, 158, 244, 424], radius=10, fill=RED)
    draw.rectangle([200, 158, 244, 424], fill=RED)  # square off the right edge
    icon_flags(draw, 42, 200, 184, 150, (255, 255, 255))
    draw.text((268, 178), hero["kicker"], font=font(True, 21), fill=RED)
    y = draw_text_block(draw, 268, 206,
                        wrap(draw, hero["headline"], font(True, 42), 700),
                        font(True, 42), NAVY, 50)
    draw_text_block(draw, 268, y + 10,
                    wrap(draw, hero["body"], font(False, 25), 700),
                    font(False, 25), MUTED, 33)

    # ---- four-story grid ----
    colors = [BLUE, TEAL, GREEN, PURPLE]
    icons = [icon_bridge, icon_ballot, icon_chart, icon_crossing]
    for i, story in enumerate(news["stories"]):
        col, row = i % 2, i // 2
        x0 = 24 + col * 504
        y0 = 434 + row * 194
        x1, y1 = x0 + 472, y0 + 180
        rounded_card(draw, [x0, y0, x1, y1])
        draw.rectangle([x0 + 10, y0, x1 - 10, y0 + 8], fill=colors[i])
        ix, iy = x0 + 16, y0 + 30
        icons[i](draw, ix, iy + 10, 88, 92, colors[i])
        tx = x0 + 116
        draw.text((tx, y0 + 24), story["kicker"], font=font(True, 19), fill=colors[i])
        y = draw_text_block(draw, tx, y0 + 50,
                            wrap(draw, story["headline"], font(True, 28), 340)[:2],
                            font(True, 28), INK, 34)
        draw_text_block(draw, tx, y + 6,
                        wrap(draw, story["body"], font(False, 19), 340)[:2],
                        font(False, 19), MUTED, 25)

    # ---- also today: four briefs ----
    draw.text((28, 816), "ALSO TODAY", font=font(True, 22), fill=NAVY)
    draw.line([170, 830, 996, 830], fill=LINE, width=2)
    for i, brief in enumerate(news["briefs"]):
        bx = 28 + i * 247
        draw.rectangle([bx, 858, bx + 14, 872], fill=NAVY)
        draw_text_block(draw, bx + 24, 852,
                        wrap(draw, brief["headline"], font(True, 20), 210)[:2],
                        font(True, 20), INK, 25)
        draw_text_block(draw, bx + 24, 906,
                        wrap(draw, brief["body"], font(False, 17), 210)[:2],
                        font(False, 17), MUTED, 22)

    # ---- banner + sources ----
    draw.rectangle([0, 956, W, 994], fill=RED)
    draw.text((512, 964), news["footer"], font=font(True, 22), fill=(255, 255, 255),
              anchor="ma")
    draw.text((512, 1000), news["sources"], font=font(False, 14), fill=MUTED, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
