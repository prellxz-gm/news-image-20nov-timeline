#!/usr/bin/env python3
"""Draw entry.png for news-image-20261120 — variant C 'Timeline + Proof'.

Front page, 1024x1024, drawn entirely with PIL: masthead, date-check strip,
3 large drawn lead panels, a UTC timeline rail + spine, a 2-column story
grid (38 stories), and a bottom band with region legend + world-map inset.
All 41 verified stories from the brief's story list. No AI image.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(bold, size):
    return ImageFont.truetype(F_BOLD if bold else F_REG, size)


# ---------------------------------------------------------------- palette
NAVY = (16, 28, 51)
NAVY2 = (24, 44, 78)
PAPER = (250, 248, 242)
INK = (24, 24, 28)
MUTED = (84, 90, 102)
GREEN_BG = (227, 243, 228)
GREEN_TX = (27, 94, 32)
GOLD = (201, 162, 39)
RED = (176, 38, 38)
LINE = (203, 208, 216)
SPINE = (176, 186, 200)

REGIONS = {
    "Europe":       ((31, 78, 156), 9),
    "Asia":         ((192, 57, 43), 14),
    "Oceania":      ((46, 125, 50), 6),
    "Latin America": ((230, 126, 34), 4),
    "North America": ((108, 52, 131), 3),
    "Africa":       ((176, 141, 10), 3),
    "Middle East":  ((0, 131, 143), 2),
}

# (headline, outlet, region) — 38 grid stories; leads are drawn separately.
STORIES = [
    # Europe
    ("Polish jets scramble amid barrage", "CNN", "Europe"),
    ("France seeks UN Council meeting", "Reuters", "Europe"),
    ("UK and EU agree reset deal", "Reuters", "Europe"),
    ("Gen Z strikes sweep 25 nations", "CNN", "Europe"),
    ("ATP approves $350m pay plan", "Reuters", "Europe"),
    ("Pochettino's first Man Utd presser", "NBC", "Europe"),
    ("Macron hosts Harris in Paris", "Le Monde", "Europe"),
    # Middle East
    ("Iraq troops deploy in stronghold", "Reuters", "Middle East"),
    ("Saudi intercepts Houthi missile", "Reuters", "Middle East"),
    # Africa
    ("581 women killed in South Africa", "BBC", "Africa"),
    ("Ruto mocks opposition walkout", "People Daily", "Africa"),
    ("Egypt solar for 7,000 factories", "Salala Times", "Africa"),
    # Asia
    ("Asian shares plunge in AI rout", "Morningstar", "Asia"),
    ("Pakistan seal Test series win", "Reuters", "Asia"),
    ("Sen, Satwik into HK semis", "Indian Witness", "Asia"),
    ("Japan inflation hits year's high", "One Turn", "Asia"),
    ("10,000 rally against Takaichi", "Freedom Press", "Asia"),
    ("Modi opens first SCO Forum", "PIB", "Asia"),
    ("India unveils H5N1 chicken vaccine", "OPEN", "Asia"),
]

STORIES_R = [
    # Asia (continued)
    ("Cheetah gives birth to four cubs", "PIB", "Asia"),
    ("First cholera case in S Korea", "MedicalXpress", "Asia"),
    ("Korea moves to impeach top judge", "SE Daily", "Asia"),
    ("Prabowo, Xi talk S. China Sea", "DevDiscourse", "Asia"),
    ("Google asked over 19,000 cuts", "Reuters", "Asia"),
    ("Marcos returns with P41bn pledges", "PNA", "Asia"),
    # North America
    ("BC Tories end century-long wait", "CanPress", "North America"),
    ("Bitcoin hits lowest since July", "CoinDesk", "North America"),
    ("China hackers exploited VMware", "Help Net", "North America"),
    # Latin America
    ("EU-Mexico trade pact nears OK", "Reuters", "Latin America"),
    ("Colombia seizes 3.9t of cocaine", "Unfiltered", "Latin America"),
    ("Chile Senate passes 2027 budget", "Swipely", "Latin America"),
    ("Brazil marks Black Consciousness", "Particle", "Latin America"),
    # Oceania
    ("Nicholls' 175* powers NZ to 368", "Cricbuzz", "Oceania"),
    ("Norma 'arm' may not be an arm", "phys.org", "Oceania"),
    ("Australia defence bill passes", "TrueNorth", "Oceania"),
    ("NSW rejects $2bn metro claim", "Brief News", "Oceania"),
    ("David Jones axes 1,600 staff", "mikes.news", "Oceania"),
    ("Polymiadis guilty of murder", "People", "Oceania"),
]

assert len(STORIES) == 19 and len(STORIES_R) == 19, (len(STORIES), len(STORIES_R))

LEADS = [
    dict(num=1, kicker="LEAD 1  ·  EUROPE — WAR", color=REGIONS["Europe"][0],
         head="Russia's 110-missile barrage batters Kyiv",
         fact="3 bridges hit · 9 killed, 28 injured", outlet="CNN"),
    dict(num=2, kicker="LEAD 2  ·  ASIA — CLIMATE", color=REGIONS["Asia"][0],
         head="Cyclone Akvan slams India's east coast",
         fact="100,000+ evacuated · 209 mm rain", outlet="BusinessLine"),
    dict(num=3, kicker="LEAD 3  ·  EUROPE — CLIMATE", color=REGIONS["Europe"][0],
         head="COP31 ends in deadlock — no fossil-fuel deal",
         fact="Draft cut 144→80 paras · no deal", outlet="phys.org"),
]


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


TRUNCATED = []


def fit(draw, s, f, max_w):
    """Truncate with ellipsis if a line would overflow; returns the string."""
    if draw.textlength(s, font=f) <= max_w:
        return s
    TRUNCATED.append(s)
    ell = "…"
    while s and draw.textlength(s + ell, font=f) > max_w:
        s = s[:-1]
    return s + ell


def wrap(draw, s, f, max_w):
    """Greedy word wrap, returns list of lines (max 2 expected)."""
    words = s.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- pictograms
def draw_kyiv(d, x, y, w, h):
    """Night skyline, river + 3 bridges, missile streaks, explosions."""
    d.rectangle([x, y, x + w, y + h], fill=(11, 30, 58))
    # stars
    for sx, sy in [(18, 10), (70, 6), (130, 14), (200, 8), (260, 16),
                   (40, 26), (150, 30), (230, 28), (290, 12)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(220, 225, 240))
    # missile streaks (top right -> down left)
    for mx, my, ln in [(250, 4, 46), (210, 2, 52), (285, 10, 38)]:
        d.line([x + mx, y + my, x + mx - ln, y + my + ln // 2], fill=(255, 140, 40), width=3)
        d.ellipse([x + mx - 3, y + my - 3, x + mx + 3, y + my + 3], fill=(255, 220, 120))
    # explosion bursts
    for ex, ey, r in [(96, 34, 12), (196, 40, 10)]:
        for k in range(8):
            a = k * math.pi / 4
            d.line([x + ex, y + ey,
                    x + ex + int(r * math.cos(a)), y + ey + int(r * math.sin(a))],
                   fill=(255, 176, 32), width=3)
        d.ellipse([x + ex - 5, y + ey - 5, x + ex + 5, y + ey + 5], fill=(255, 220, 90))
    # skyline
    base = y + h - 16
    heights = [22, 30, 18, 34, 26, 38, 20, 30, 24]
    bx = x + 6
    bw = (w - 12) // len(heights)
    for hh in heights:
        d.rectangle([bx, base - hh, bx + bw - 3, base], fill=(6, 12, 24))
        for wy in range(base - hh + 4, base - 3, 7):
            d.rectangle([bx + 3, wy, bx + 5, wy + 3], fill=(255, 214, 90))
        bx += bw
    # river + bridges
    d.rectangle([x, base, x + w, y + h], fill=(18, 58, 96))
    for cx in (60, 152, 244):
        d.arc([x + cx - 26, base - 2, x + cx + 26, base + 22], 180, 360,
              fill=(214, 222, 235), width=3)
        d.line([x + cx - 26, base + 8, x + cx + 26, base + 8], fill=(214, 222, 235), width=2)


def draw_akvan(d, x, y, w, h):
    """Cyclone spiral over sea, rain, coastline with houses."""
    d.rectangle([x, y, x + w, y + h], fill=(178, 219, 238))
    cx, cy = x + 118, y + 36
    # spiral: concentric broken arcs, teal
    for r, start in [(34, 20), (26, 140), (18, 260), (10, 60)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 300,
              fill=(18, 92, 122), width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(12, 66, 92))
    # rain streaks
    for rx, ry in [(20, 8), (48, 20), (250, 12), (278, 26), (90, 6), (220, 30)]:
        d.line([x + rx, y + ry, x + rx - 5, y + ry + 12], fill=(120, 170, 205), width=2)
    # coast + sea
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(46, 127, 168))
    d.polygon([(x, y + h - 20), (x + 120, y + h - 20), (x + 90, y + h),
               (x, y + h)], fill=(196, 164, 110))
    # waves
    for wx in (150, 185, 220, 255):
        d.arc([x + wx - 12, y + h - 16, x + wx + 12, y + h - 2], 180, 360,
              fill=(235, 245, 250), width=2)
    # houses on the coast
    for hx in (18, 44, 72):
        d.rectangle([x + hx, y + h - 32, x + hx + 16, y + h - 20], fill=(240, 240, 235))
        d.polygon([(x + hx - 2, y + h - 32), (x + hx + 8, y + h - 40),
                   (x + hx + 18, y + h - 32)], fill=(176, 60, 40))


def draw_cop31(d, x, y, w, h):
    """Conference hall: banner, flags, delegates, document, NO DEAL stamp."""
    d.rectangle([x, y, x + w, y + h], fill=(245, 238, 220))
    # banner
    d.rectangle([x + 60, y + 4, x + w - 60, y + 22], fill=(31, 78, 156))
    d.text((x + w // 2, y + 13), "COP31  ·  ANTALYA",
           font=font(True, 13), fill=(255, 255, 255), anchor="mm")
    # flags row
    flag_cols = [(31, 78, 156), (192, 57, 43), (46, 125, 50), (230, 126, 34),
                 (108, 52, 131), (0, 131, 143)]
    for i, c in enumerate(flag_cols):
        fx = x + 22 + i * 46
        d.line([fx, y + 26, fx, y + 46], fill=(90, 90, 90), width=2)
        d.rectangle([fx, y + 26, fx + 26, y + 38], fill=c)
    # table + delegates
    d.rectangle([x + 14, y + 52, x + w - 14, y + h - 6], fill=(146, 104, 62))
    d.rectangle([x + 14, y + 52, x + w - 14, y + 57], fill=(120, 82, 46))
    for i in range(5):
        px = x + 34 + i * 54
        d.ellipse([px - 8, y + 30, px + 8, y + 46], fill=(222, 184, 150))
        d.polygon([(px - 12, y + 52), (px + 12, y + 52), (px + 8, y + 38),
                   (px - 8, y + 38)],
                  fill=[(52, 84, 120), (120, 52, 52), (52, 110, 70),
                        (120, 100, 40), (90, 60, 110)][i])
    # document on the table
    d.rectangle([x + w - 108, y + 52, x + w - 24, y + h - 10], fill=(255, 255, 255),
                outline=(150, 150, 150))
    for ly in range(y + 58, y + h - 14, 7):
        d.line([x + w - 100, ly, x + w - 32, ly], fill=(190, 190, 190), width=1)
    # NO DEAL stamp
    sx, sy = x + w - 66, y + 52
    d.ellipse([sx - 26, sy - 14, sx + 26, sy + 14], outline=RED, width=3)
    d.text((sx, sy), "NO DEAL", font=font(True, 13), fill=RED, anchor="mm")


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead (0–64)
    d.rectangle([0, 0, W, 64], fill=NAVY)
    d.text((16, 12), "THE WORLD IN ONE DAY", font=font(True, 40), fill=(255, 255, 255))
    dt = "FRIDAY 20 NOVEMBER 2026"
    d.text((W - 16, 12), dt, font=font(True, 20), fill=(255, 255, 255), anchor="ra")
    d.text((W - 16, 40), "41 STORIES  ·  7 REGIONS", font=font(True, 13),
           fill=(255, 214, 90), anchor="ra")
    d.rectangle([0, 60, W, 64], fill=GOLD)

    # ---- date-check strip (64–98)
    d.rectangle([0, 64, W, 98], fill=GREEN_BG)
    d.rectangle([0, 64, W, 98], outline=(120, 190, 125), width=1)
    d.text((16, 81), "✓  EVERY EVENT VERIFIED — FRIDAY 20 NOVEMBER 2026",
           font=font(True, 20), fill=GREEN_TX, anchor="lm")
    d.text((W - 16, 81), "SOURCES CHECKED 20 NOV 2026", font=font(True, 13),
           fill=GREEN_TX, anchor="rm")

    # ---- lead panels (98–292)
    panel_w, gap = 328, 8
    px0 = 12
    for i, lead in enumerate(LEADS):
        x = px0 + i * (panel_w + gap)
        y, ph = 98, 194
        d.rectangle([x, y, x + panel_w, y + ph], fill=(255, 255, 255),
                    outline=LINE, width=1)
        # kicker bar
        d.rectangle([x, y, x + panel_w, y + 26], fill=lead["color"])
        d.text((x + 10, y + 13), lead["kicker"], font=font(True, 13),
               fill=(255, 255, 255), anchor="lm")
        # pictogram
        pic = [draw_kyiv, draw_akvan, draw_cop31][i]
        pic(d, x + 12, y + 32, panel_w - 24, 64)
        # headline (2 lines, 22px)
        lines = wrap(d, lead["head"], font(True, 22), panel_w - 24)
        hy = y + 100
        for ln in lines[:2]:
            d.text((x + 12, hy), ln, font=font(True, 22), fill=INK)
            hy += 26
        # fact line
        fy = y + 156
        d.text((x + 12, fy), fit(d, lead["fact"], font(False, 14), panel_w - 24),
               font=font(False, 14), fill=MUTED)
        # outlet (own line at panel bottom-right)
        d.text((x + panel_w - 12, y + ph - 6), lead["outlet"], font=font(True, 13),
               fill=lead["color"], anchor="rb")

    # ---- timeline rail (292–322)
    d.text((16, 307), "THE DAY IN STORIES — UTC", font=font(True, 16), fill=NAVY, anchor="lm")
    rx0, rx1, ry = 300, 1000, 312
    d.line([rx0, ry, rx1, ry], fill=SPINE, width=3)
    for h in range(0, 25, 4):
        tx = rx0 + (rx1 - rx0) * h // 24
        d.ellipse([tx - 4, ry - 4, tx + 4, ry + 4], fill=NAVY)
        lab = "%02d" % h
        d.text((tx, ry - 12), lab, font=font(False, 13), fill=MUTED, anchor="mb")

    # ---- story grid (322–858): 19 rows x 28px, 2 columns, centre spine
    gy0, row_h = 322, 28
    col_l, col_r, col_w = 12, 524, 488
    d.line([512, gy0 + 4, 512, gy0 + 19 * row_h - 4], fill=SPINE, width=3)
    f_head = font(True, 20)
    f_out = font(False, 13)
    for row in range(19):
        cy = gy0 + row * row_h
        # spine dot (left story's region colour)
        c = REGIONS[STORIES[row][2]][0]
        d.ellipse([512 - 5, cy + 14 - 5, 512 + 5, cy + 14 + 5], fill=c,
                  outline=(255, 255, 255), width=1)
        for col_x, story in ((col_l, STORIES[row]), (col_r, STORIES_R[row])):
            head, outlet, region = story
            rc = REGIONS[region][0]
            d.ellipse([col_x, cy + 9, col_x + 10, cy + 19], fill=rc)
            out_txt = " · " + outlet
            ow = d.textlength(out_txt, font=f_out)
            hw = col_w - 14 - ow - 4
            head_fit = fit(d, head, f_head, hw)
            d.text((col_x + 14, cy + 14), head_fit, font=f_head, fill=INK, anchor="lm")
            d.text((col_x + 14 + d.textlength(head_fit, font=f_head) + 4, cy + 14),
                   out_txt, font=f_out, fill=MUTED, anchor="lm")

    # ---- bottom band (858–1024)
    by = 858
    d.line([0, by, W, by], fill=LINE, width=1)
    d.text((16, by + 16), "REGIONS", font=font(True, 14), fill=NAVY)
    # legend: 7 chips in two rows
    lx, ly = 16, by + 36
    order = ["Asia", "Europe", "Oceania", "Latin America", "North America",
             "Africa", "Middle East"]
    chip_w = [190, 150, 150, 190, 210, 130, 190]
    cx, cy = lx, ly
    for j, name in enumerate(order):
        c, n = REGIONS[name]
        d.rectangle([cx, cy, cx + 12, cy + 12], fill=c)
        d.text((cx + 18, cy + 6), "%s · %d" % (name, n), font=font(False, 14),
               fill=INK, anchor="lm")
        cx += chip_w[j]
        if j == 3:
            cx, cy = lx, ly + 26
    # fields line
    d.text((16, by + 92),
           "FIELDS:  War & politics 14  ·  Markets & tech 9  ·  Society & culture 6  ·  "
           "Sport 5  ·  Science 4  ·  Climate 3",
           font=font(False, 13), fill=MUTED)
    d.text((16, by + 114),
           "Drawn from verified reporting — every story first reported on Friday 20 November 2026.",
           font=font(False, 13), fill=MUTED)
    d.text((16, by + 134),
           "Lead stories: Kyiv barrage · Cyclone Akvan · COP31 deadlock.",
           font=font(False, 13), fill=MUTED)

    # world-map inset (bottom-right, 200 x 118)
    mx, my, mw, mh = 808, by + 14, 200, 118
    d.rectangle([mx, my, mx + mw, my + mh], fill=(226, 238, 245),
                outline=LINE, width=1)
    d.text((mx + 6, my + 12), "MAP — DOTS = REGIONS",
           font=font(True, 13), fill=NAVY, anchor="lm")
    map_top = my + 20
    # rough continent blobs (x, y in map box, map area below the caption)
    polys = [
        [(8, 32), (28, 20), (52, 22), (68, 32), (60, 48), (46, 58), (28, 54), (14, 44)],
        [(48, 62), (62, 60), (72, 72), (66, 94), (56, 92), (48, 74)],
        [(96, 30), (112, 20), (126, 26), (122, 40), (108, 44), (98, 38)],
        [(100, 48), (118, 46), (132, 55), (128, 78), (112, 88), (102, 70)],
        [(126, 26), (160, 18), (190, 28), (188, 50), (165, 62), (140, 58), (128, 42)],
        [(160, 88), (185, 86), (190, 100), (172, 108), (160, 100)],
    ]
    land = (196, 206, 198)
    for p in polys:
        d.polygon([(mx + a, map_top + int(b * 0.88)) for a, b in p], fill=land)
    dots = [("North America", 40, 35), ("Latin America", 60, 75),
            ("Europe", 112, 32), ("Africa", 115, 65), ("Middle East", 128, 48),
            ("Asia", 152, 40), ("Oceania", 175, 95)]
    for name, dx, dy in dots:
        c = REGIONS[name][0]
        myy = map_top + int(dy * 0.88)
        d.ellipse([mx + dx - 5, myy - 5, mx + dx + 5, myy + 5],
                  fill=c, outline=(255, 255, 255), width=1)

    img.save(OUT, "PNG")
    if TRUNCATED:
        print("TRUNCATED LINES:", TRUNCATED)
    else:
        print("no truncations")
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
