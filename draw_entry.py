#!/usr/bin/env python3
"""Render entry.png for the make.fun news-image-20261125 bounty.

A 1024x1024 newspaper front page summing up Wednesday 25 November
2026: a masthead, one lead story (Ukraine hits Russian ships in the
Gulf of Finland and off Libya), two mid-size stories (COP31 collapses
in Antalya with no climate deal; a Houthi drone hits Riyadh's tallest
tower), three short stories (the CIA and the DNI's office are hacked;
Huawei is found guilty of stealing trade secrets; Trump awards
Giuliani the Medal of Freedom), plus an ALSO TODAY ticker and a
sources line. Every fact below was checked against Reuters / CNN /
UN News / RFE/RL reporting on 25 November 2026.

Run: python3 draw_entry.py  -> writes entry.png next to this script.
Stdlib + Pillow only. No network access.
"""
from PIL import Image, ImageDraw, ImageFont

W = 1024
BG = (247, 243, 232)      # newsprint
CARD_BG = (255, 255, 255)
CARD_EDGE = (210, 203, 185)
INK = (18, 18, 18)
MUTED = (96, 96, 90)
NAVY = (13, 32, 66)
GOLD = (198, 148, 42)
CRIMSON = (164, 30, 30)
OCEAN = (20, 68, 140)
FOREST = (24, 102, 52)
EMBER = (178, 58, 14)
VIOLET = (96, 44, 130)
SLATE = (52, 84, 96)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(drw, text, fnt, width):
    """Greedy word wrap into lines no wider than width pixels."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            test = cur + " " + w
            if drw.textlength(test, font=fnt) <= width:
                cur = test
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text_block(drw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        drw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def fit_headline(drw, text, x, y, width, max_lines, size0, size_min,
                 color):
    """Headline that steps down in size until it fits max_lines."""
    size = size0
    while size > size_min:
        fnt = font(F_SERIF, size)
        if len(wrap(drw, text, fnt, width)) <= max_lines:
            break
        size -= 2
    fnt = font(F_SERIF, size)
    lines = wrap(drw, text, fnt, width)[:max_lines]
    return text_block(drw, lines, x, y, fnt, color, int(size * 1.14))


def body(drw, text, x, y, width, max_lines, size, color=INK):
    fnt = font(F_SANS, size)
    lines = wrap(drw, text, fnt, width)[:max_lines]
    return text_block(drw, lines, x, y, fnt, color, int(size * 1.32))


def tag(drw, text, x, y, color):
    fnt = font(F_SANS_B, 17)
    drw.text((x, y), text, font=fnt, fill=color)
    return y + 24


def panel(drw, x0, y0, x1, y1, accent):
    drw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=CARD_BG,
                          outline=CARD_EDGE, width=2)
    drw.rounded_rectangle([x0, y0, x1, y0 + 14], radius=8, fill=accent)
    drw.rectangle([x0, y0 + 7, x1, y0 + 14], fill=accent)


# ---- small pictograms, drawn with plain shapes ----------------------

def ship(drw, cx, cy, r, color):
    """A cargo ship: hull, stacked containers, bridge, mast."""
    # hull
    drw.polygon([(cx - r, cy + r * 0.25), (cx + r, cy + r * 0.25),
                 (cx + r * 0.78, cy + r * 0.72),
                 (cx - r * 0.78, cy + r * 0.72)], fill=color)
    # containers
    for i, h in enumerate((0.42, 0.58, 0.42)):
        x0 = cx - r * 0.85 + i * r * 0.58
        drw.rectangle([x0, cy - r * h, x0 + r * 0.5, cy + r * 0.22],
                      fill=color)
    # bridge + mast
    drw.rectangle([cx + r * 0.42, cy - r * 0.72, cx + r * 0.82,
                   cy + r * 0.22], fill=color)
    drw.line([cx + r * 0.62, cy - r * 0.72, cx + r * 0.62,
              cy - r * 1.0], fill=color, width=4)
    drw.line([cx - r * 0.95, cy + r * 0.25, cx - r * 0.95,
              cy - r * 0.35], fill=color, width=4)


def globe(drw, cx, cy, r, color):
    """A globe: circle, meridians, equator, with a crack."""
    drw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    drw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                outline=color, width=4)
    drw.line([cx - r, cy, cx + r, cy], fill=color, width=4)
    drw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 200, 340,
            fill=color, width=4)
    # crack: short zigzag across the top right
    pts = [(cx + r * 0.1, cy - r * 0.95), (cx + r * 0.35, cy - r * 0.6),
           (cx + r * 0.15, cy - r * 0.35), (cx + r * 0.45, cy - r * 0.05)]
    drw.line(pts, fill=color, width=4, joint="curve")


def tower(drw, cx, cy, r, color):
    """A skyscraper: tall slab, pointed crown, lit windows."""
    drw.rectangle([cx - r * 0.42, cy - r * 0.55, cx + r * 0.42,
                   cy + r * 0.95], fill=color)
    drw.polygon([(cx - r * 0.42, cy - r * 0.55),
                 (cx + r * 0.42, cy - r * 0.55),
                 (cx, cy - r * 1.0)], fill=color)
    drw.line([cx, cy - r * 1.0, cx, cy - r * 1.25], fill=color, width=4)
    for row in range(4):
        y = cy - r * 0.25 + row * r * 0.3
        for col in (-1, 1):
            drw.rectangle([cx + col * r * 0.22 - 4, y,
                           cx + col * r * 0.22 + 4, y + 8],
                          fill=CARD_BG)


def render():
    img = Image.new("RGB", (W, W), BG)
    drw = ImageDraw.Draw(img)
    m = 34

    # ---- masthead ----------------------------------------------------
    drw.rectangle([m, 26, W - m, 30], fill=NAVY)
    title = "THE WORLD IN ONE DAY"
    tf = font(F_SERIF, 58)
    tw = drw.textlength(title, font=tf)
    drw.text(((W - tw) / 2, 44), title, font=tf, fill=NAVY)
    sub = ("WEDNESDAY  ·  25 NOVEMBER 2026  ·  THE DAY'S WORLD NEWS "
           "IN ONE PICTURE")
    sf = font(F_SANS_B, 19)
    sw = drw.textlength(sub, font=sf)
    drw.text(((W - sw) / 2, 118), sub, font=sf, fill=GOLD)
    drw.line([m, 152, W - m, 152], fill=NAVY, width=3)
    drw.line([m, 158, W - m, 158], fill=NAVY, width=1)

    # ---- lead story: Ukraine hits Russian ships -----------------------
    x0, y0, x1, y1 = m, 176, W - m, 408
    panel(drw, x0, y0, x1, y1, CRIMSON)
    ship(drw, x1 - 108, y0 + 108, 58, CRIMSON)
    drw.text((x1 - 168, y0 + 176), "2 SHIPS HIT", font=font(F_SANS_B, 17),
             fill=CRIMSON)
    drw.text((x1 - 168, y0 + 198), "KYIV CONFIRMS", font=font(F_SANS, 15),
             fill=MUTED)
    y = tag(drw, "UKRAINE  ·  WAR AT SEA", x0 + 22, y0 + 30, CRIMSON)
    y = fit_headline(drw, "UKRAINE HITS RUSSIAN SHIPS", x0 + 22, y,
                     700, 1, 58, 36, INK)
    body(drw, "Zelenskiy confirms Ukraine's drone strike on a Russian "
              "cargo ship in the Gulf of Finland — and a Russian "
              "warship sunk off Benghazi, Libya. Moscow calls them "
              "'terrorist acts'.",
         x0 + 22, y + 8, 700, 3, 22)

    # ---- two mid-size stories -----------------------------------------
    mid_y0, mid_y1 = 424, 636
    mid_w = (W - 2 * m - 18) // 2

    # COP31 collapses
    ax0, ay0, ax1 = m, mid_y0, m + mid_w
    panel(drw, ax0, ay0, ax1, mid_y1, OCEAN)
    globe(drw, ax1 - 58, ay0 + 58, 30, OCEAN)
    y = tag(drw, "CLIMATE  ·  COP31", ax0 + 20, ay0 + 26, OCEAN)
    y = fit_headline(drw, "CLIMATE SUMMIT COLLAPSES", ax0 + 20, y,
                     mid_w - 120, 2, 30, 24, INK)
    body(drw, "COP31 in Antalya ends with no deal — the first climate "
              "summit to collapse since 2009 — as oil states block any "
              "mention of fossil fuels. The UN chief calls it deeply "
              "disappointing.", ax0 + 20, y + 6,
         mid_w - 40, 4, 18)

    # Houthi drone hits Riyadh tower
    bx0, bx1 = m + mid_w + 18, W - m
    panel(drw, bx0, ay0, bx1, mid_y1, FOREST)
    tower(drw, bx1 - 58, ay0 + 58, 28, FOREST)
    y = tag(drw, "MIDDLE EAST  ·  YEMEN WAR", bx0 + 20, ay0 + 26, FOREST)
    y = fit_headline(drw, "HOUTHI DRONE HITS RIYADH TOWER",
                     bx0 + 20, y, mid_w - 120, 2, 30, 24, INK)
    body(drw, "A Houthi drone attack hits Riyadh's tallest tower, "
              "wounding 11 people, Saudi civil defence says — a rare "
              "strike deep inside the Saudi capital.",
         bx0 + 20, y + 6, mid_w - 40, 3, 18)

    # ---- three short stories -------------------------------------------
    sm_y0, sm_y1 = 656, 852
    sm_w = (W - 2 * m - 36) // 3
    shorts = [
        (EMBER, "USA  ·  INTELLIGENCE", "CIA AND SPY CHIEF'S OFFICE HACKED",
         "The CIA and the spy chief's office suffer a breach of some "
         "unclassified information, a source tells Reuters."),
        (VIOLET, "TECH  ·  COURTS", "HUAWEI GUILTY OF STEALING SECRETS",
         "A US jury finds China's Huawei guilty of stealing trade "
         "secrets in a criminal trial — but acquits it of "
         "racketeering."),
        (SLATE, "USA  ·  WHITE HOUSE", "TRUMP HONOURS GIULIANI",
         "Donald Trump awards Rudy Giuliani the Presidential Medal of "
         "Freedom, the highest US civilian honour."),
    ]
    for i, (accent, kick, head, text) in enumerate(shorts):
        sx0 = m + i * (sm_w + 18)
        sx1 = sx0 + sm_w
        panel(drw, sx0, sm_y0, sx1, sm_y1, accent)
        y = tag(drw, kick, sx0 + 18, sm_y0 + 24, accent)
        y = fit_headline(drw, head, sx0 + 18, y, sm_w - 36, 2, 24, 18,
                         INK)
        body(drw, text, sx0 + 18, y + 6, sm_w - 36, 4, 16)

    # ---- ticker ----------------------------------------------------------
    ty0, ty1 = 868, 936
    drw.rounded_rectangle([m, ty0, W - m, ty1], radius=8, fill=NAVY)
    lab_f = font(F_SANS_B, 18)
    label = "ALSO TODAY  "
    drw.text((m + 18, ty0 + 22), label, font=lab_f, fill=GOLD)
    lx = m + 18 + drw.textlength(label, font=lab_f)
    ticker = ("700,000+ Russian soldiers killed in the Ukraine war, new "
              "analysis finds  •  NATO to deploy early-warning aircraft "
              "in Poland  •  Iran says 3 oil tankers hit by mines in "
              "the Strait of Hormuz  •  Sarkozy corruption case sent "
              "to trial  •  Nvidia falls 7% as Dell lifts forecasts on "
              "AI server boom")
    y = ty0 + 8
    for ln in wrap(drw, ticker, font(F_SANS, 16), W - m - lx - 18):
        drw.text((lx, y), ln, font=font(F_SANS, 16),
                 fill=(235, 235, 235))
        y += 20

    # ---- sources footer ---------------------------------------------------
    foot = ("Sources: Reuters · CNN · UN News · RFE/RL  —  "
            "25 November 2026")
    ff = font(F_SANS, 16)
    fw = drw.textlength(foot, font=ff)
    drw.text(((W - fw) / 2, 950), foot, font=ff, fill=MUTED)
    drw.text((m, 984), "THE WORLD IN ONE DAY — 25 NOVEMBER 2026",
             font=font(F_SANS_B, 13), fill=MUTED)
    tail = "ONE PICTURE · SIX STORIES · ALL VERIFIED"
    drw.text((W - m - drw.textlength(tail, font=font(F_SANS_B, 13)), 984),
             tail, font=font(F_SANS_B, 13), fill=MUTED)

    img.save("entry.png")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    render()
