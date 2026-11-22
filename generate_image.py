#!/usr/bin/env python3
"""Draw the front-page image for Sunday 22 November 2026 world news.

Writes entry.png (1024x1024, PNG) beside this file. Pure Pillow drawing:
a newspaper front page with a masthead, one lead story and six more
stories across regions and beats, plus a ticker of further headlines.
No network, no downloaded assets; every shape and letter is drawn here.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
NAVY = (18, 32, 62)
RED = (178, 34, 34)
RULE = (120, 110, 95)
CARD = (255, 255, 255)
MUTED = (90, 86, 76)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, width, fill, leading=None):
    x, y = xy
    lines = wrap(draw, text, fnt, width)
    step = leading or int(fnt.size * 1.25)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y, len(lines)


def tag(draw, xy, label, bg):
    x, y = xy
    fnt = F_SANS_B(20)
    w = draw.textlength(label, font=fnt) + 18
    h = 32
    draw.rounded_rectangle([x, y, x + w, y + h], radius=5, fill=bg)
    draw.text((x + 9, y + 4), label, font=fnt, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- stories
LEAD = {
    "tag": "SUMMIT",
    "headline": "Trump, Xi and Putin meet in Shenzhen",
    "body": "The leaders of the US, China and Russia hold a rare trilateral "
            "summit and agree to open talks on reducing nuclear risk.",
}

STORIES = [
    {
        "tag": "CLIMATE",
        "color": (34, 120, 74),
        "headline": "COP31 deadlocked on fossil fuels",
        "body": "Antalya talks enter a 2nd day of overtime as nations split "
                "on fossil fuels.",
    },
    {
        "tag": "MEXICO",
        "color": (146, 64, 14),
        "headline": "\u2018El Chapo Isidro\u2019 captured; 11 killed",
        "body": "Mexican forces arrest Fausto Isidro Meza Flores in Sinaloa; "
                "7 gunmen, 4 soldiers die.",
    },
    {
        "tag": "MIDDLE EAST",
        "color": (154, 32, 32),
        "headline": "Iran hits Bahrain; Hormuz tankers struck",
        "body": "Bahrain says Iran hit a civilian site; tankers "
                "struck near Hormuz.",
    },
    {
        "tag": "DISASTER",
        "color": (90, 60, 140),
        "headline": "Magnitude 6.7 quake in Peru",
        "body": "A strong quake rattles the Andes in central Peru, felt "
                "across the region.",
    },
    {
        "tag": "MARKETS",
        "color": (20, 90, 110),
        "headline": "US stocks in correction; AI sell-off",
        "body": "Wall Street falls as investors dump AI and chip shares; "
                "Dow, S&P in correction.",
    },
    {
        "tag": "ENTERTAINMENT",
        "color": (120, 30, 90),
        "headline": "GTA 6: record $3.79bn launch day",
        "body": "Grand Theft Auto VI posts the biggest games launch day "
                "ever: $3.79bn.",
    },
]

TICKER = ("ALSO:  FBI confirms its NCIC crime database was breached  "
          "\u2022  Leeds stun Chelsea 4\u20131 at Stamford Bridge  \u2022  "
          "Nigeria boat capsizes, 24 dead  \u2022  Snow strands 1,500 in "
          "Fukushima")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((36, 16), "THE WORLD IN ONE PAGE", font=F_SERIF_B(52),
           fill=(255, 255, 255))
    d.text((36, 76), "SUNDAY, 22 NOVEMBER 2026",
           font=F_SANS_B(30), fill=(232, 196, 90))
    d.text((W - 36, 76), "WORLD NEWS", font=F_SANS_B(26),
           fill=(200, 205, 220), anchor="ra")
    d.rectangle([0, 118, W, 124], fill=RED)

    # ---- lead story ----------------------------------------------------
    y = 140
    tag(d, (36, y), LEAD["tag"], RED)
    d.text((36 + 148, y + 3), "THE DAY'S TOP STORY", font=F_SANS_B(22),
           fill=MUTED)
    y += 44
    y, _ = draw_wrapped(d, (36, y), LEAD["headline"], F_SERIF_B(52),
                        W - 72, INK, leading=62)
    y += 6
    y, _ = draw_wrapped(d, (36, y), LEAD["body"], F_SANS(26), W - 72,
                        (50, 48, 42), leading=34)
    y += 12
    d.line([0, y, W, y], fill=RULE, width=2)
    grid_top = y + 16

    # ---- story grid: 3 columns x 2 rows -------------------------------
    gap = 16
    col_w = (W - 72 - 2 * gap) // 3
    card_h = 226
    for i, s in enumerate(STORIES):
        col = i % 3
        row = i // 3
        x0 = 36 + col * (col_w + gap)
        y0 = grid_top + row * (card_h + gap)
        d.rounded_rectangle([x0, y0, x0 + col_w, y0 + card_h], radius=10,
                            fill=CARD, outline=(205, 198, 182), width=2)
        d.rectangle([x0, y0, x0 + 8, y0 + card_h], fill=s["color"])
        tx = x0 + 24
        ty = y0 + 12
        tag(d, (tx, ty), s["tag"], s["color"])
        hy = ty + 42
        hy, _ = draw_wrapped(d, (tx, hy), s["headline"], F_SERIF_B(26),
                             col_w - 40, INK, leading=31)
        draw_wrapped(d, (tx, hy + 6), s["body"], F_SANS(18),
                     col_w - 40, (60, 58, 52), leading=23)

    y = grid_top + 2 * card_h + gap

    # ---- ticker --------------------------------------------------------
    y += 10
    d.rectangle([0, y, W, y + 2], fill=RULE)
    y += 10
    d.text((36, y), "ALSO TODAY", font=F_SANS_B(21), fill=RED)
    ty = y + 28
    for line in wrap(d, TICKER, F_SANS(20), W - 72):
        d.text((36, ty), line, font=F_SANS(20), fill=(50, 48, 42))
        ty += 26

    # ---- footer --------------------------------------------------------
    fy = H - 38
    d.rectangle([0, fy - 10, W, fy - 8], fill=RULE)
    d.text((36, fy), "Sources: wire reports of 22 November 2026  \u00b7  "
                     "Image sums up the day's world news",
           font=F_SANS(19), fill=MUTED)
    d.text((W - 36, fy), "make.fun", font=F_SANS_B(19), fill=MUTED,
           anchor="ra")

    img.save("entry.png", "PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
