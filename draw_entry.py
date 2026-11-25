#!/usr/bin/env python3
"""Render the news-image-20261125 front page.

One 1024x1024 newspaper front page summing up Wednesday 25 November
2026: a masthead, one lead story, two mid-size stories, three short
stories, an ALSO TODAY ticker and a sources line. Stdlib + Pillow
only, no network. Deterministic: the same run always writes the
same bytes, because nothing here depends on time, randomness or
the environment.

Run: python3 draw_entry.py   -> writes entry.png next to this script.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

SIZE = 1024
MARGIN = 38
CONTENT_W = SIZE - 2 * MARGIN

PAPER = (246, 241, 229)
INK = (24, 24, 24)
NAVY = (16, 38, 66)
RED = (168, 32, 36)
GOLD = (176, 134, 34)
BLUE = (28, 74, 140)
GREEN = (28, 102, 58)
RUST = (178, 74, 28)
PURPLE = (104, 62, 140)
STEEL = (58, 92, 110)
GREY = (112, 106, 94)
TICKER_BG = (14, 30, 62)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


class FrontPage:
    """A 1024x1024 newsprint page, drawn top to bottom."""

    def __init__(self):
        self.image = Image.new("RGB", (SIZE, SIZE), PAPER)
        self.draw = ImageDraw.Draw(self.image)

    # -- small helpers -------------------------------------------------

    def rule(self, y, thick=1, color=NAVY, x0=MARGIN, x1=SIZE - MARGIN):
        self.draw.line([(x0, y), (x1, y)], fill=color, width=thick)

    def centered(self, y, text, font, color=INK, cx=SIZE // 2):
        width = self.draw.textlength(text, font=font)
        self.draw.text((cx - width / 2, y), text, font=font, fill=color)

    def wrap(self, text, font, width):
        """Greedy word wrap; every returned line fits `width`."""
        lines = []
        current = ""
        for word in text.split():
            trial = (current + " " + word).strip()
            if self.draw.textlength(trial, font=font) <= width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def paragraph(self, x, y, text, font, width, leading, color=INK):
        for line in self.wrap(text, font, width):
            self.draw.text((x, y), line, font=font, fill=color)
            y += leading
        return y

    def headline(self, x, y, text, size, width, color=INK):
        font = load(SERIF_BOLD, size)
        for line in self.wrap(text, font, width):
            self.draw.text((x, y), line, font=font, fill=color)
            y += size + 6
        return y

    def kicker(self, x, y, text, size, color):
        font = load(SANS_BOLD, size)
        self.draw.text((x, y), text, font=font, fill=color)
        return y + size + 8

    # -- little line drawings ------------------------------------------

    def ship(self, x, y, w, h, color=RED):
        """A cargo ship: stacked containers, hull, mast, waves."""
        d = self.draw
        # containers, tallest in the middle
        d.rectangle([x + int(w * 0.10), y + int(h * 0.30),
                     x + int(w * 0.38), y + int(h * 0.55)], fill=color)
        d.rectangle([x + int(w * 0.42), y + int(h * 0.14),
                     x + int(w * 0.68), y + int(h * 0.55)], fill=color)
        d.rectangle([x + int(w * 0.72), y + int(h * 0.30),
                     x + int(w * 0.94), y + int(h * 0.55)], fill=color)
        # mast with a small flag
        d.line([(x + int(w * 0.55), y + int(h * 0.14)),
                (x + int(w * 0.55), y - 4)], fill=color, width=3)
        d.polygon([(x + int(w * 0.55), y - 4),
                   (x + int(w * 0.55) + 18, y + 2),
                   (x + int(w * 0.55), y + 8)], fill=color)
        # hull
        d.polygon([(x, y + int(h * 0.55)),
                   (x + w, y + int(h * 0.55)),
                   (x + int(w * 0.88), y + h),
                   (x + int(w * 0.12), y + h)], fill=color)
        # waves
        d.line([(x, y + h + 8), (x + int(w * 0.45), y + h + 8)],
               fill=GREY, width=2)
        d.line([(x + int(w * 0.55), y + h + 8), (x + w, y + h + 8)],
               fill=GREY, width=2)

    def globe(self, x, y, r, color=BLUE):
        """A wireframe globe: circle, meridians, parallels."""
        d = self.draw
        d.ellipse([x, y, x + 2 * r, y + 2 * r], outline=color, width=4)
        d.ellipse([x + r // 2, y, x + 3 * r // 2, y + 2 * r],
                  outline=color, width=3)
        d.line([(x, y + r), (x + 2 * r, y + r)], fill=color, width=3)
        d.arc([x, y + r // 3, x + 2 * r, y + 5 * r // 3],
              start=200, end=340, fill=color, width=3)
        d.arc([x, y + r // 3, x + 2 * r, y + 5 * r // 3],
              start=20, end=160, fill=color, width=3)

    def tower(self, x, y, w, h, color=GREEN):
        """A tall tower with a spire and a few windows."""
        d = self.draw
        d.polygon([(x + w // 2, y),
                   (x + w // 2 + 7, y + 14),
                   (x + w // 2 - 7, y + 14)], fill=color)
        d.rectangle([x + 6, y + 14, x + w - 6, y + h], fill=color)
        for row in range(4):
            wy = y + 24 + row * 12
            d.rectangle([x + 11, wy, x + w - 11, wy + 5],
                        fill=PAPER)

    # -- story blocks ---------------------------------------------------

    def story(self, x, y, w, bar, kick, kick_color, head, head_size,
              body, body_size, body_leading, icon=None):
        """One story: coloured top bar, kicker, headline, body."""
        self.draw.rectangle([x, y, x + w, y + 7], fill=bar)
        y += 16
        y = self.kicker(x, y, kick, 17, kick_color)
        if icon is not None:
            # small icon in the kicker row, clear of the headline below
            icon(x + w - 58, y - 33)
        y = self.headline(x, y, head, head_size, w)
        y += 2
        y = self.paragraph(x, y, body, load(SANS, body_size), w,
                           body_leading)
        return y

    def ticker(self, y, height, label, text):
        self.draw.rounded_rectangle(
            [MARGIN, y, SIZE - MARGIN, y + height], radius=10,
            fill=TICKER_BG)
        label_font = load(SANS_BOLD, 20)
        label_w = self.draw.textlength(label, font=label_font)
        text_x = MARGIN + 18 + label_w + 22
        text_w = SIZE - MARGIN - 18 - text_x
        body_font = load(SANS, 18)
        lines = self.wrap(text, body_font, text_w)
        block = len(lines) * 23
        ly = y + max(6, (height - block) // 2)
        self.draw.text((MARGIN + 18, ly), label, font=label_font,
                       fill=GOLD)
        for line in lines:
            self.draw.text((text_x, ly), line, font=body_font,
                           fill=(240, 238, 230))
            ly += 23

    # -- the page ---------------------------------------------------------

    def build(self):
        # Masthead
        self.rule(26, thick=4)
        self.centered(36, "THE WORLD IN ONE DAY",
                      load(SERIF_BOLD, 58), color=NAVY)
        self.centered(
            110,
            "WEDNESDAY  \u00b7  25 NOVEMBER 2026  \u00b7  "
            "THE DAY'S WORLD NEWS IN ONE PICTURE",
            load(SANS_BOLD, 20), color=GOLD)
        self.rule(140, thick=2)
        self.rule(145, thick=1)

        # Lead story: Ukraine hits Russian ships
        y = 150
        y = self.kicker(MARGIN, y, "UKRAINE  \u00b7  WAR AT SEA", 19, RED)
        y = self.headline(MARGIN, y, "UKRAINE HITS RUSSIAN SHIPS",
                          48, 720)
        y += 4
        y = self.paragraph(
            MARGIN, y,
            "President Zelenskiy confirms Ukraine's drone strike on a "
            "Russian cargo ship in the Gulf of Finland \u2014 and a "
            "Russian warship sunk off Benghazi, Libya. Moscow calls "
            "the attacks \u2018terrorist acts\u2019 and warns of severe "
            "consequences.",
            load(SANS, 21), 720, 28)
        lead_end = y
        # ship drawing on the right of the lead
        self.ship(816, 186, 150, 108)
        self.centered(308, "2 SHIPS HIT", load(SANS_BOLD, 18),
                      color=RED, cx=891)
        self.centered(330, "KYIV CONFIRMS", load(SANS_BOLD, 14),
                      color=GREY, cx=891)
        self.rule(lead_end + 8, thick=1, color=GREY)

        # Two mid-size stories
        mid_y = lead_end + 22
        mid_w = 462
        mid_end = max(
            self.story(MARGIN, mid_y, mid_w, BLUE,
                       "CLIMATE  \u00b7  COP31", BLUE,
                       "CLIMATE SUMMIT COLLAPSES", 34,
                       "COP31 in Antalya ends with no deal \u2014 the first "
                       "climate summit to collapse since 2009 \u2014 as oil "
                       "states block any mention of fossil fuels. The UN "
                       "chief calls it deeply disappointing.",
                       18, 24,
                       icon=lambda ix, iy: self.globe(ix, iy, 16)),
            self.story(MARGIN + mid_w + 24, mid_y, mid_w, GREEN,
                       "MIDDLE EAST  \u00b7  YEMEN WAR", GREEN,
                       "HOUTHI DRONE HITS RIYADH TOWER", 34,
                       "A Houthi drone attack hits Riyadh's tallest tower, "
                       "wounding 11 people, Saudi civil defence says \u2014 "
                       "a rare strike deep inside the Saudi capital.",
                       18, 24,
                       icon=lambda ix, iy: self.tower(ix, iy, 32, 32)))
        self.rule(mid_end + 10, thick=1, color=GREY)

        # Three short stories
        short_y = mid_end + 24
        short_w = 296
        gap = 20
        short_end = max(
            self.story(MARGIN, short_y, short_w, RUST,
                       "USA  \u00b7  INTELLIGENCE", RUST,
                       "CIA AND SPY CHIEF'S OFFICE HACKED", 25,
                       "The CIA and the director of national intelligence's "
                       "office suffer a breach of some unclassified "
                       "information, a source tells Reuters.",
                       16, 21),
            self.story(MARGIN + short_w + gap, short_y, short_w, PURPLE,
                       "TECH  \u00b7  COURTS", PURPLE,
                       "HUAWEI GUILTY OF STEALING SECRETS", 25,
                       "A US jury finds China's Huawei guilty of stealing "
                       "trade secrets in a criminal trial \u2014 but acquits "
                       "it of racketeering.",
                       16, 21),
            self.story(MARGIN + 2 * (short_w + gap), short_y, short_w,
                       STEEL, "USA  \u00b7  WHITE HOUSE", STEEL,
                       "TRUMP HONOURS GIULIANI", 25,
                       "Donald Trump awards Rudy Giuliani the Presidential "
                       "Medal of Freedom, the highest US civilian honour.",
                       16, 21))

        # ALSO TODAY ticker
        ticker_y = short_end + 12
        self.ticker(
            ticker_y, 74, "ALSO TODAY",
            "700,000+ Russian soldiers killed (new analysis) "
            "\u00b7 NATO AWACS to Poland \u00b7 3 Iranian tankers mined "
            "in Hormuz \u00b7 Sarkozy corruption case to trial "
            "\u00b7 Nvidia -7%, Dell raises AI forecast.")

        # Sources line
        self.centered(ticker_y + 74 + 10,
                      "Sources: Reuters \u00b7 CNN \u00b7 UN News "
                      "\u00b7 RFE/RL \u2014 25 November 2026",
                      load(SANS, 17), color=GREY)

    def save(self):
        self.image.save(OUT, format="PNG")


def main():
    page = FrontPage()
    page.build()
    page.save()
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
