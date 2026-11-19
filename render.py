#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page.

news.json holds the day's stories, researched from Reuters, AP, BBC and
Al Jazeera reporting of 19 November 2026. This script turns that data
into entry.png, a 1024 by 1024 front page. It works fully offline and is
deterministic: the same news.json always produces the same PNG bytes.

Run it with: python3 render.py
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
DEJAVU = "/usr/share/fonts/truetype/dejavu"

PAGE_W, PAGE_H = 1024, 1024
C = {
    "navy": (14, 42, 71),
    "gold": (201, 162, 39),
    "gold_light": (232, 196, 92),
    "paper": (247, 243, 234),
    "card": (255, 255, 255),
    "ink": (26, 32, 40),
    "muted": (84, 94, 106),
    "red": (166, 28, 28),
    "teal": (15, 118, 110),
    "blue": (29, 78, 150),
    "green": (46, 125, 50),
    "purple": (106, 62, 158),
    "line": (214, 206, 190),
    "white": (255, 255, 255),
    "soft": (205, 216, 228),
}


def F(bold, size):
    """DejaVu at the requested weight and size."""
    fname = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(DEJAVU, fname), size)


def wrap_text(d, s, f, width):
    """Split s into lines that fit width when drawn with font f."""
    out, cur = [], ""
    for word in s.split():
        cand = (cur + " " + word).strip()
        if d.textlength(cand, font=f) <= width:
            cur = cand
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def put_lines(d, x, y, lines, f, color, gap):
    """Draw each line, stepping down by gap; return the y below the last."""
    for ln in lines:
        d.text((x, y), ln, font=f, fill=color)
        y += gap
    return y


def card(d, box, fill=None, edge=None):
    d.rounded_rectangle(box, radius=10,
                        fill=fill if fill is not None else C["card"],
                        outline=edge if edge is not None else C["line"],
                        width=2)


def flags_icon(d, x, y, w, h, color):
    """Three flagpoles: the three leaders of the hero story."""
    for k, cx in enumerate((x + int(w * 0.18), x + int(w * 0.5), x + int(w * 0.82))):
        d.line([cx, y + 4, cx, y + h - 4], fill=color, width=5)
        fy = y + 6 + k * 6
        d.polygon([(cx, fy), (cx + 36, fy + 11), (cx, fy + 23)], fill=color)


def bridge_icon(d, x, y, w, h, color):
    """A suspension bridge deck with towers and hangers."""
    deck = y + int(h * 0.6)
    d.line([x, deck, x + w, deck], fill=color, width=6)
    for tx in (x + int(w * 0.16), x + int(w * 0.74)):
        d.line([tx, y + 6, tx, deck], fill=color, width=6)
        d.line([tx - 13, y + 6, tx + 13, y + 6], fill=color, width=6)
    d.arc([x + 4, y + int(h * 0.26), x + w - 4, deck + 36], 180, 360,
          fill=color, width=5)
    for k in range(5):
        hx = x + int(w * (0.08 + 0.21 * k))
        d.line([hx, deck, hx, deck + 26], fill=color, width=4)


def ballot_icon(d, x, y, w, h, color):
    """A ballot box with a tick: the Speaker nomination."""
    bx, by = x + 6, y + int(h * 0.32)
    bw, bh = w - 12, int(h * 0.52)
    d.rectangle([bx, by, bx + bw, by + bh], outline=color, width=5)
    d.line([bx, by, bx + int(bw * 0.45), by - 15], fill=color, width=5)
    d.line([bx + int(bw * 0.45), by - 15, bx + bw, by + 5], fill=color, width=5)
    d.line([bx + int(bw * 0.3), by + int(bh * 0.55),
            bx + int(bw * 0.45), by + int(bh * 0.78)], fill=color, width=6)
    d.line([bx + int(bw * 0.45), by + int(bh * 0.78),
            bx + int(bw * 0.78), by + int(bh * 0.28)], fill=color, width=6)


def bars_icon(d, x, y, w, h, color):
    """Rising bars: the record IPO."""
    base = y + h - 6
    heights = [0.32, 0.52, 0.42, 0.72, 1.0]
    bw = w // 6
    for k, frac in enumerate(heights):
        bx0 = x + k * (bw + 4)
        bh = int((h - 14) * frac)
        d.rectangle([bx0, base - bh, bx0 + bw, base], fill=color)
    d.line([x, base, x + w, base], fill=color, width=4)


def cross_icon(d, x, y, w, h, color):
    """An arrow crossing a dashed line: the Gaza ceasefire line."""
    mid = y + h // 2
    for dx in range(0, w, 18):
        d.line([x + dx, mid, x + dx + 10, mid], fill=color, width=4)
    x0, y0 = x + 6, y + h - 12
    x1, y1 = x + w - 12, y + 10
    d.line([x0, y0, x1, y1], fill=color, width=6)
    d.polygon([(x1, y1), (x1 - 18, y1 + 2), (x1 - 4, y1 + 18)], fill=color)


ICONS = [bridge_icon, ballot_icon, bars_icon, cross_icon]
ACCENTS = [C["blue"], C["teal"], C["green"], C["purple"]]


def draw_masthead(d, news):
    d.rectangle([0, 0, PAGE_W, 140], fill=C["navy"])
    d.rectangle([0, 140, PAGE_W, 146], fill=C["gold"])
    d.text((28, 22), news["title"], font=F(True, 64), fill=C["white"])
    d.text((30, 100), news["subtitle"], font=F(False, 23), fill=C["soft"])
    d.text((996, 24), news["date_lines"][0], font=F(True, 28),
           fill=C["gold_light"], anchor="ra")
    d.text((996, 58), news["date_lines"][1], font=F(True, 40),
           fill=C["white"], anchor="ra")


def draw_hero(d, news):
    hero = news["hero"]
    card(d, [24, 158, 1000, 424])
    d.rounded_rectangle([24, 158, 244, 424], radius=10, fill=C["red"])
    d.rectangle([200, 158, 244, 424], fill=C["red"])
    flags_icon(d, 42, 200, 184, 150, C["white"])
    d.text((268, 178), hero["kicker"], font=F(True, 21), fill=C["red"])
    y = put_lines(d, 268, 206,
                  wrap_text(d, hero["headline"], F(True, 42), 700),
                  F(True, 42), C["navy"], 50)
    put_lines(d, 268, y + 10,
              wrap_text(d, hero["body"], F(False, 25), 700),
              F(False, 25), C["muted"], 33)


def draw_grid(d, news):
    for i, story in enumerate(news["stories"]):
        col, row = i % 2, i // 2
        x0 = 24 + col * 504
        y0 = 434 + row * 194
        x1, y1 = x0 + 472, y0 + 180
        card(d, [x0, y0, x1, y1])
        d.rectangle([x0 + 10, y0, x1 - 10, y0 + 8], fill=ACCENTS[i])
        ICONS[i](d, x0 + 16, y0 + 40, 88, 92, ACCENTS[i])
        tx = x0 + 116
        d.text((tx, y0 + 24), story["kicker"], font=F(True, 19),
               fill=ACCENTS[i])
        y = put_lines(d, tx, y0 + 50,
                      wrap_text(d, story["headline"], F(True, 28), 340)[:2],
                      F(True, 28), C["ink"], 34)
        put_lines(d, tx, y + 6,
                  wrap_text(d, story["body"], F(False, 19), 340)[:2],
                  F(False, 19), C["muted"], 25)


def draw_briefs(d, news):
    d.text((28, 816), "ALSO TODAY", font=F(True, 22), fill=C["navy"])
    d.line([170, 830, 996, 830], fill=C["line"], width=2)
    for i, brief in enumerate(news["briefs"]):
        bx = 28 + i * 247
        d.rectangle([bx, 858, bx + 14, 872], fill=C["navy"])
        put_lines(d, bx + 24, 852,
                  wrap_text(d, brief["headline"], F(True, 20), 210)[:2],
                  F(True, 20), C["ink"], 25)
        put_lines(d, bx + 24, 906,
                  wrap_text(d, brief["body"], F(False, 17), 210)[:2],
                  F(False, 17), C["muted"], 22)


def draw_footer(d, news):
    d.rectangle([0, 956, PAGE_W, 994], fill=C["red"])
    d.text((512, 964), news["footer"], font=F(True, 22),
           fill=C["white"], anchor="ma")
    d.text((512, 1000), news["sources"], font=F(False, 14),
           fill=C["muted"], anchor="ma")


def main():
    with open(os.path.join(BASE, "news.json"), encoding="utf-8") as fh:
        news = json.load(fh)
    img = Image.new("RGB", (PAGE_W, PAGE_H), C["paper"])
    d = ImageDraw.Draw(img)
    draw_masthead(d, news)
    draw_hero(d, news)
    draw_grid(d, news)
    draw_briefs(d, news)
    draw_footer(d, news)
    out = os.path.join(BASE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
