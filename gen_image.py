#!/usr/bin/env python3
"""Draw the entry image for news-image-20261121: one-day world news front page.
All artwork is drawn from scratch with PIL shapes and DejaVu fonts.
Output: entry.png, 1024x1024, deterministic (no timestamps, no randomness)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (20, 38, 76)
GOLD = (232, 193, 90)
WHITE = (255, 255, 255)
RED = (178, 34, 34)
DARKRED = (139, 0, 0)
GREEN = (31, 122, 74)
TEAL = (14, 110, 110)
PURPLE = (94, 53, 130)
ORANGE = (214, 106, 24)
GREY = (90, 90, 90)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(d, x, y, lines, fnt, fill, spacing=4):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def card(d, box, accent):
    d.rounded_rectangle(box, radius=10, fill=WHITE, outline=INK, width=2)
    d.rounded_rectangle([box[0], box[1], box[2], box[1] + 10], radius=10, fill=accent)
    d.rectangle([box[0], box[1] + 5, box[2], box[1] + 10], fill=accent)


def panel(d, box, accent, kicker, headline, body, icon_fn, head_size=27):
    card(d, box, accent)
    x0, y0, x1, y1 = box
    pad = 16
    y = y0 + 22
    d.text((x0 + pad, y), kicker, font=font(FB, 17), fill=accent)
    y += 26
    hl = wrap(d, headline, font(FB, head_size), x1 - x0 - 2 * pad)
    y = draw_text_block(d, x0 + pad, y, hl, font(FB, head_size), INK, spacing=2)
    y += 6
    bl = wrap(d, body, font(FR, 19), x1 - x0 - 2 * pad)
    y = draw_text_block(d, x0 + pad, y, bl, font(FR, 19), (60, 60, 60), spacing=3)
    icon_fn(d, x0, y, x1, y1)


# ---- icons (simple geometric scenes) ----
def icon_chart(d, x0, y, x1, y1):
    # falling market line, red
    ix0, iy0, ix1, iy1 = x0 + 16, y + 4, x1 - 16, y1 - 14
    d.rectangle([ix0, iy0, ix1, iy1], outline=(200, 200, 200), width=1)
    pts = [(ix0 + 8, iy0 + 12), (ix0 + 60, iy0 + 28), (ix0 + 110, iy0 + 22),
           (ix0 + 165, iy0 + 48), (ix0 + 220, iy0 + 44), (ix0 + 272, iy0 + 68)]
    d.line(pts, fill=RED, width=5)
    d.polygon([(ix0 + 272, iy0 + 68), (ix0 + 258, iy0 + 62), (ix0 + 262, iy0 + 76)],
              fill=RED)
    d.text((ix1 - 92, iy0 + 4), "-5.3%", font=font(FB, 22), fill=RED)


def icon_barrier(d, x0, y, x1, y1):
    ix0, iy0 = x0 + 16, y + 2
    # Estonian flag stripes
    d.rectangle([ix0, iy0, ix0 + 70, iy0 + 12], fill=(0, 114, 206))
    d.rectangle([ix0, iy0 + 12, ix0 + 70, iy0 + 24], fill=(20, 20, 20))
    d.rectangle([ix0, iy0 + 24, ix0 + 70, iy0 + 36], fill=WHITE, outline=INK, width=1)
    # barrier stripes
    bx = ix0 + 90
    for i in range(5):
        col = RED if i % 2 == 0 else WHITE
        d.polygon([(bx + i * 34, iy0 + 36), (bx + i * 34 + 24, iy0 + 36),
                   (bx + i * 34 + 10, iy0), (bx + i * 34 - 14, iy0)], fill=col)
    d.rectangle([bx - 4, iy0, bx + 176, iy0 + 36], outline=INK, width=2)
    d.text((ix0, iy0 + 44), "ALL CROSSINGS SHUT", font=font(FB, 17), fill=INK)


def icon_shield(d, x0, y, x1, y1):
    cx, cy = x0 + 60, y + 42
    d.polygon([(cx - 34, cy - 30), (cx + 34, cy - 30), (cx + 34, cy + 2),
               (cx, cy + 36), (cx - 34, cy + 2)], outline=NAVY, width=4)
    d.line([(cx - 16, cy), (cx - 4, cy + 12), (cx + 18, cy - 14)],
           fill=GREEN, width=6)
    d.text((x0 + 112, y + 22), "PLOT FOILED", font=font(FB, 21), fill=NAVY)


def icon_pill(d, x0, y, x1, y1):
    cx, cy = x0 + 70, y + 40
    d.rounded_rectangle([cx - 55, cy - 20, cx + 55, cy + 20], radius=20,
                        fill=(240, 240, 240), outline=INK, width=3)
    d.rounded_rectangle([cx - 55, cy - 20, cx, cy + 20], radius=20, fill=TEAL)
    d.rectangle([cx - 8, cy - 20, cx, cy + 20], fill=TEAL)
    d.text((x0 + 150, y + 12), "1 in 12: tumours", font=font(FB, 21), fill=TEAL)
    d.text((x0 + 150, y + 40), "gone on scans", font=font(FB, 21), fill=TEAL)


def icon_gta(d, x0, y, x1, y1):
    ix0, iy0, ix1, iy1 = x0 + 16, y + 2, x1 - 16, y1 - 12
    # sunset gradient bands
    bands = [(255, 122, 89), (255, 159, 67), (255, 205, 92), (124, 58, 237)]
    bh = (iy1 - iy0) // 4
    for i, c in enumerate(bands):
        d.rectangle([ix0, iy0 + i * bh, ix1, iy0 + (i + 1) * bh], fill=c)
    # sun
    d.ellipse([ix0 + 150, iy0 + 8, ix0 + 210, iy0 + 68], fill=(255, 236, 160))
    # palm silhouette
    px, py = ix0 + 60, iy1 - 6
    d.line([(px, py), (px + 8, py - 62)], fill=(30, 20, 40), width=7)
    for dx, dy in [(-38, -58), (-30, -72), (30, -70), (42, -56), (0, -78)]:
        d.line([(px + 8, py - 62), (px + 8 + dx, py - 62 + dy)],
               fill=(30, 20, 40), width=5)
    d.text((ix0 + 228, iy0 + 14), "$3.79 BILLION", font=font(FB, 24), fill=WHITE)
    d.text((ix0 + 228, iy0 + 48), "DAY-ONE RECORD", font=font(FB, 20), fill=WHITE)


def icon_missile(d, x0, y, x1, y1):
    # right side of the lead panel: missile streak + burst + NATO star
    cx, cy = 880, 270
    d.line([(700, 330), (850, 235)], fill=(150, 150, 150), width=4)
    d.line([(700, 345), (840, 255)], fill=(200, 200, 200), width=3)
    # missile body
    d.polygon([(852, 218), (892, 252), (872, 272), (838, 240)], fill=(90, 90, 90))
    d.polygon([(892, 252), (912, 246), (898, 268)], fill=(90, 90, 90))
    # burst star
    bx, by = 950, 330
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 34, 14
        a1 = math.radians(ang)
        a2 = math.radians(ang + 15)
        d.polygon([(bx + r1 * math.cos(a1), by + r1 * math.sin(a1)),
                   (bx + r2 * math.cos(a2), by + r2 * math.sin(a2)),
                   (bx + r1 * math.cos(math.radians(ang + 30)),
                    by + r1 * math.sin(math.radians(ang + 30)))], fill=ORANGE)
    d.ellipse([bx - 16, by - 16, bx + 16, by + 16], fill=RED)
    d.text((700, 380), "NO INJURIES REPORTED", font=font(FB, 18), fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=4)

    # Masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((W // 2, 12), "THE WORLD IN ONE DAY", font=font(FB, 56),
           fill=WHITE, anchor="ma")
    d.text((W // 2, 76), "SATURDAY, 21 NOVEMBER 2026", font=font(FB, 30),
           fill=GOLD, anchor="ma")

    # Lead story: Poland
    box = (12, 130, 1012, 408)
    card(d, box, RED)
    d.text((30, 150), "CONFLICT  ·  POLAND  —  LEAD STORY",
           font=font(FB, 19), fill=RED)
    d.text((30, 178), "RUSSIAN MISSILES LAND", font=font(FB, 46), fill=INK)
    d.text((30, 228), "ON NATO SOIL", font=font(FB, 46), fill=INK)
    body = ("Two Russian missiles and a drone came down in Poland "
            "during a huge strike on Ukraine. PM Tusk calls it a "
            "deliberate provocation; NATO chief Rutte calls it a "
            "\u201cgrave violation\u201d of allied airspace.")
    bl = wrap(d, body, font(FR, 21), 640)
    draw_text_block(d, 30, 292, bl, font(FR, 21), (60, 60, 60), spacing=4)
    icon_missile(d, 0, 0, 0, 0)

    # Row A: three panels
    yA0, yA1 = 420, 692
    xw = (1012 - 12 - 2 * 12) // 3
    panel(d, (12, yA0, 12 + xw, yA1), DARKRED, "MARKETS  ·  NEW YORK",
          "WALL STREET PLUNGES", "S&P 500 slides into correction as AI shares sell off. Nasdaq falls 5.3%; Nvidia drops about 14%.",
          icon_chart, head_size=25)
    panel(d, (12 + xw + 12, yA0, 12 + 2 * xw + 12, yA1), NAVY, "EUROPE  ·  ESTONIA",
          "ESTONIA SHUTS BORDER WITH RUSSIA", "Tallinn closes every crossing after a suspected arson sabotage near the frontier.",
          icon_barrier, head_size=25)
    panel(d, (12 + 2 * xw + 24, yA0, 1012, yA1), PURPLE, "EUROPE  ·  DENMARK",
          "RUSSIAN PLOT TO KILL RAPPER FOILED", "Danish police say they stopped a Russian plan to assassinate US-Ukrainian rapper Kyivstoner.",
          icon_shield, head_size=25)

    # Row B: two wide panels
    yB0, yB1 = 704, 1004
    bw = (1012 - 12 - 12) // 2
    panel(d, (12, yB0, 12 + bw, yB1), TEAL, "HEALTH  ·  BARCELONA",
          "PANCREATIC CANCER PILL HAILED AS BREAKTHROUGH",
          "Daraxonrasib plus chemotherapy shrank or cleared tumours in 60.7% of patients in a trial of 61 people with advanced disease.",
          icon_pill, head_size=26)
    panel(d, (12 + bw + 12, yB0, 1012, yB1), ORANGE, "CULTURE  ·  GAMING",
          "GTA VI SMASHES SALES RECORD",
          "Rockstar reports $3.79 billion in first-day retail sales — the biggest entertainment launch ever.",
          icon_gta, head_size=26)

    img.save("entry.png", "PNG")
    print("saved entry.png")


if __name__ == "__main__":
    main()
