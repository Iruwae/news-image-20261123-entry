#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - Monday 23 November 2026.
Draws a 1024x1024 broadsheet PNG with PIL. Deterministic: no network,
no randomness, no timestamps in output."""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 248, 239)
INK = (17, 17, 17)
GREY = (90, 88, 80)
RULE = (40, 40, 40)
RED = (178, 34, 34)
BLUE = (24, 64, 120)
TAN = (214, 200, 160)
OCEAN = (205, 222, 232)
LAND = (232, 222, 188)
LAND_EDGE = (150, 135, 100)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
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


def draw_wrapped(draw, text, fnt, x, y, max_w, fill=INK, leading=None, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def hline(draw, x0, x1, y, wdt=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=wdt)


# ---------------------------------------------------------------- scenes
def scene_capitol(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(176, 205, 228))
    draw.rectangle([x0, y0 + h - 26, x0 + w, y0 + h], fill=(96, 120, 84))
    cx = x0 + w // 2
    # columns
    for i in range(-4, 5):
        px = cx + i * 26
        draw.rectangle([px - 5, y0 + h - 78, px + 5, y0 + h - 26], fill=(245, 240, 225))
    # base + entablature
    draw.rectangle([x0 + 18, y0 + h - 88, x0 + w - 18, y0 + h - 76], fill=(245, 240, 225))
    draw.rectangle([x0 + 8, y0 + h - 34, x0 + w - 8, y0 + h - 26], fill=(235, 228, 208))
    # dome
    draw.pieslice([cx - 52, y0 + 8, cx + 52, y0 + 96], 180, 360, fill=(245, 240, 225))
    draw.rectangle([cx - 52, y0 + 52, cx + 52, y0 + 62], fill=(245, 240, 225))
    draw.rectangle([cx - 4, y0 + 2, cx + 4, y0 + 12], fill=(245, 240, 225))
    # flag
    draw.line([(cx, y0 + 2), (cx, y0 - 12)], fill=INK, width=2)
    draw.polygon([(cx, y0 - 12), (cx + 16, y0 - 8), (cx, y0 - 4)], fill=RED)
    # windows
    for i in range(-3, 4):
        px = cx + i * 26
        draw.rectangle([px - 3, y0 + h - 66, px + 3, y0 + h - 52], fill=(60, 70, 80))
    draw.ellipse([cx - 8, y0 + 34, cx + 8, y0 + 50], fill=(60, 70, 80))


def scene_nato(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(38, 58, 92))
    # flags row
    flags = [(24, 64, 120), (178, 34, 34), (0, 90, 60), (200, 160, 30),
             (120, 40, 120), (30, 120, 160), (200, 90, 30), (90, 90, 90)]
    fw, fh = 30, 20
    gap = (w - len(flags) * fw) / (len(flags) + 1)
    for i, c in enumerate(flags):
        fx = x0 + gap + i * (fw + gap)
        fy = y0 + 14
        draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(245, 240, 225))
        draw.rectangle([fx, fy, fx + fw, fy + fh // 2], fill=c)
        draw.line([(fx + fw / 2, fy + fh), (fx + fw / 2, fy + fh + 26)], fill=(200, 200, 200), width=2)
    # table
    draw.ellipse([x0 + 20, y0 + h - 52, x0 + w - 20, y0 + h - 6], fill=(120, 80, 50))
    draw.ellipse([x0 + 34, y0 + h - 58, x0 + w - 34, y0 + h - 18], fill=(160, 112, 66))
    # name plates
    for i in range(5):
        px = x0 + 40 + i * 52
        draw.rectangle([px, y0 + h - 44, px + 34, y0 + h - 34], fill=(245, 240, 225))
    # seats
    for i in range(5):
        px = x0 + 44 + i * 52
        draw.rectangle([px, y0 + h - 78, px + 26, y0 + h - 60], fill=(30, 30, 40))


def scene_rescue(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(70, 70, 76))
    # floodlight glow
    draw.ellipse([x0 + w - 78, y0 + 4, x0 + w - 8, y0 + 60], fill=(240, 220, 140))
    draw.line([(x0 + w - 43, y0 + 60), (x0 + w - 90, y0 + h - 30)], fill=(200, 190, 120), width=2)
    # standing wall fragment
    draw.rectangle([x0 + 12, y0 + 22, x0 + 58, y0 + h - 30], fill=(120, 112, 100))
    for r in range(3):
        for c in range(2):
            draw.rectangle([x0 + 18 + c * 20, y0 + 30 + r * 22,
                            x0 + 34 + c * 20, y0 + 46 + r * 22], fill=(60, 60, 70))
    # rubble mound
    draw.polygon([(x0 + 40, y0 + h - 26), (x0 + 130, y0 + 40),
                  (x0 + 230, y0 + 62), (x0 + w - 10, y0 + h - 26)],
                 fill=(150, 142, 128))
    draw.polygon([(x0 + 90, y0 + h - 26), (x0 + 150, y0 + 66),
                  (x0 + 210, y0 + h - 26)], fill=(130, 122, 108))
    draw.polygon([(x0 + 160, y0 + h - 26), (x0 + 200, y0 + 78),
                  (x0 + 250, y0 + h - 26)], fill=(110, 102, 90))
    # crane arm
    draw.line([(x0 + 250, y0 + 10), (x0 + 150, y0 + 70)], fill=(220, 180, 60), width=5)
    draw.line([(x0 + 150, y0 + 70), (x0 + 150, y0 + 92)], fill=(220, 180, 60), width=3)
    # rescue workers (orange helmets)
    for px, py in [(x0 + 96, y0 + h - 52), (x0 + 176, y0 + h - 48), (x0 + 226, y0 + h - 50)]:
        draw.rectangle([px - 5, py, px + 5, py + 22], fill=(230, 120, 30))
        draw.ellipse([px - 6, py - 10, px + 6, py + 2], fill=(240, 200, 40))
        draw.rectangle([px - 8, py + 4, px + 8, py + 10], fill=(240, 240, 230))


# ---------------------------------------------------------------- map
CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
           (-80, 73), (-65, 60), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
           (-80, 32), (-85, 30), (-90, 29), (-97, 26), (-105, 22), (-110, 24),
           (-115, 30), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    "SA": [(-80, 10), (-75, 11), (-70, 12), (-60, 8), (-52, 5), (-50, 0),
           (-40, -5), (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -40),
           (-70, -52), (-73, -50), (-73, -40), (-72, -20), (-78, -5), (-80, 5)],
    "EU": [(-10, 36), (-9, 43), (-2, 48), (0, 50), (3, 52), (8, 55), (10, 57),
           (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 70),
           (15, 70), (5, 60), (-5, 58), (-10, 52), (-10, 43), (-6, 36)],
    "AF": [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (40, 15), (43, 11),
           (48, 10), (51, 12), (44, 0), (40, -10), (35, -20), (32, -28),
           (26, -34), (20, -35), (15, -27), (12, -18), (9, -1), (9, 4),
           (-8, 5), (-15, 11), (-17, 15), (-16, 20), (-15, 27), (-10, 31)],
    "AS": [(30, 62), (40, 68), (50, 70), (60, 70), (70, 72), (80, 73), (90, 75),
           (110, 76), (130, 72), (150, 70), (170, 67), (178, 65), (170, 60),
           (162, 56), (158, 52), (142, 50), (140, 45), (135, 43), (130, 38),
           (127, 35), (122, 32), (120, 28), (110, 20), (105, 10), (100, 8),
           (95, 15), (90, 22), (85, 20), (80, 15), (75, 10), (70, 20),
           (65, 25), (60, 25), (55, 26), (50, 29), (48, 30), (42, 35),
           (38, 36), (35, 36), (30, 36), (28, 40), (30, 45), (32, 55)],
    "OC": [(113, -22), (114, -30), (115, -35), (120, -34), (130, -32), (135, -35),
           (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
           (146, -19), (142, -15), (142, -11), (137, -12), (135, -15), (132, -12),
           (130, -13), (126, -14), (122, -17), (118, -20)],
}
# display lon/lat for pins 1..30 (slightly offset where stories cluster)
PINS = {
    1: (-77, 39), 2: (9, 47.5), 3: (30.5, 50.4), 4: (167, -17),
    5: (132, 41), 6: (33, 36), 7: (18, 30), 8: (24, 62),
    9: (106.3, -6.2), 10: (28.7, 7.3), 11: (120, 23), 12: (-108.5, 25.6),
    13: (80, 14), 14: (-86, 50), 15: (2, 57.5), 16: (-1, 48),
    17: (113, 42), 18: (126, 34), 19: (-60, 33), 20: (-122.4, 37.8),
    21: (24, 23), 22: (-70, 38), 23: (41, 30), 24: (-10, 58),
    25: (22, 45), 26: (75, 30), 27: (-47.9, -15.8), 28: (-74, 4.7),
    29: (103, 50), 30: (152.3, -4.3),
}


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "out"
    os.makedirs(out_dir, exist_ok=True)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 18  # margin

    # ---- masthead
    hline(d, MX, W - MX, 8, 3)
    hline(d, MX, W - MX, 13, 1)
    f_mast = SERIF_B(46)
    d.text(((W - d.textlength("THE WORLD IN ONE DAY", font=f_mast)) / 2, 18),
           "THE WORLD IN ONE DAY", font=f_mast, fill=INK)
    hline(d, MX, W - MX, 70, 2)
    f_date = SANS_B(23)
    dtxt = "MONDAY 23 NOVEMBER 2026"
    d.text(((W - d.textlength(dtxt, font=f_date)) / 2, 78), dtxt, font=f_date, fill=INK)
    f_kick = SANS(12)
    ktxt = "ONE IMAGE  ·  THIRTY STORIES  ·  ALL REPORTED TODAY"
    d.text(((W - d.textlength(ktxt, font=f_kick)) / 2, 106), ktxt, font=f_kick, fill=GREY)

    # ---- giant headline + sub-head
    f_hl = SERIF_B(33)
    d.text(((W - d.textlength("DEMOCRATS TAKE THE HOUSE", font=f_hl)) / 2, 126),
           "DEMOCRATS TAKE THE HOUSE", font=f_hl, fill=INK)
    d.text(((W - d.textlength("NATO MEETS AS MISSILES FALL IN POLAND", font=f_hl)) / 2, 162),
           "NATO MEETS AS MISSILES FALL IN POLAND", font=f_hl, fill=INK)
    f_sub = SANS(15)
    stxt = "A blue wave not seen since 1992, an alliance on alert, and rescuers still digging in Dymer."
    d.text(((W - d.textlength(stxt, font=f_sub)) / 2, 202), stxt, font=f_sub, fill=GREY)
    hline(d, MX, W - MX, 224, 1)

    # ---- number strip: 6 boxes
    strip = [
        ("258", "Democrats win at least 258 House seats, largest majority since 1992", "BBC"),
        ("3", "Russian Kh-101 missiles confirmed fallen in SE Poland", "Polish govt"),
        ("12", "Killed in Kyiv region in overnight strikes; toll rose Monday", "Tkachenko, Telegram"),
        ("6.5", "Magnitude of Vanuatu quake, 02:40 UTC Monday, 601 km deep", "USGS"),
        ("5.8%", "Kospi fall on Monday as the AI sell-off grips Asia", "AP"),
        ("90+", "Countries sign COP31 electrification pledge after talks fail", "Reuters"),
    ]
    sy, sh = 228, 92
    bw, gap = 160, 6
    x = MX
    for num, cap, src in strip:
        d.rectangle([x, sy, x + bw, sy + sh], outline=INK, width=2)
        fn = SANS_B(36)
        d.text((x + (bw - d.textlength(num, font=fn)) / 2, sy + 4), num, font=fn, fill=RED)
        fc = SANS(9.5)
        y = sy + 44
        for ln in wrap(d, cap, fc, bw - 12)[:3]:
            d.text((x + 6, y), ln, font=fc, fill=INK)
            y += 11
        fs = SANS_B(9)
        d.text((x + 6, sy + sh - 13), "Source: " + src, font=fs, fill=GREY)
        x += bw + gap

    # ---- heroes: 3 columns
    heroes = [
        ("WASHINGTON", "DEMOCRATS TAKE THE HOUSE",
         "Democrats have won at least 258 seats, their largest House majority since 1992, "
         "after Chuck Hubbard beat Virginia Foxx in North Carolina. The party gained 44 seats; "
         "four races remain uncalled.", "BBC", scene_capitol),
        ("BRUSSELS", "NATO MEETS AS MISSILES FALL IN POLAND",
         "The North Atlantic Council meets today after Poland confirmed three Russian Kh-101 "
         "cruise missiles fell in its south-east on Friday. PM Tusk calls it an \u201cintentional "
         "provocation\u201d; NATO chief Rutte vows to \u201cdefend every inch of Polish territory\u201d.",
         "Polish govt / NATO", scene_nato),
        ("KYIV REGION", "RESCUERS DIG AS TOLL RISES TO 12",
         "Overnight Russian strikes killed at least 12 across the Kyiv region. In Dymer a "
         "five-storey block was hit; the toll there rose to nine on Monday. A boy aged seven "
         "was pulled alive from the rubble; 11 are still missing, incl. two children.",
         "Tkachenko, Telegram / AFP", scene_rescue),
    ]
    hy, hh = 328, 252
    hw, hgap = 322, 8
    x = MX
    for city, head, body, src, scene in heroes:
        d.rectangle([x, hy, x + hw, hy + hh], outline=INK, width=2)
        scene(d, x + 2, hy + 2, hw - 4, 108)
        # dateline banner
        d.rectangle([x + 2, hy + 110, x + hw - 2, hy + 128], fill=INK)
        fb = SANS_B(12)
        d.text((x + 8, hy + 113), city, font=fb, fill=(255, 255, 255))
        fh = SANS_B(15)
        y = hy + 134
        for ln in wrap(d, head, fh, hw - 14):
            d.text((x + 7, y), ln, font=fh, fill=INK)
            y += 18
        fbod = SANS(11)
        y = draw_wrapped(d, body, fbod, x + 7, y + 3, hw - 14, leading=12.5, max_lines=5)
        fs = SANS_B(9)
        d.text((x + 7, hy + hh - 13), "Source: " + src, font=fs, fill=GREY)
        x += hw + hgap

    # ---- world map + legend
    my = 588
    f_sec = SANS_B(13)
    d.text((MX, my), "THE WORLD TODAY \u2014 WHERE IT HAPPENED", font=f_sec, fill=INK)
    d.text((716, my), "REGION KEY", font=f_sec, fill=INK)
    map_x0, map_y0, map_w, map_h = MX, my + 20, 684, 140
    d.rectangle([map_x0, map_y0, map_x0 + map_w, map_y0 + map_h], fill=OCEAN, outline=INK, width=1)

    def to_xy(lon, lat):
        return (map_x0 + (lon + 180) / 360 * map_w,
                map_y0 + (90 - lat) / 150 * map_h)

    for pts in CONTINENTS.values():
        d.polygon([to_xy(lo, la) for lo, la in pts], fill=LAND, outline=LAND_EDGE)
    # graticule
    for lon in range(-150, 181, 30):
        gx, _ = to_xy(lon, 0)
        d.line([(gx, map_y0), (gx, map_y0 + map_h)], fill=(190, 205, 215), width=1)
    # pins
    f_pin = SANS_B(8)
    for n in range(1, 31):
        px, py = to_xy(*PINS[n])
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=(255, 255, 255), width=1)
        t = str(n)
        d.text((px - d.textlength(t, font=f_pin) / 2, py - 5), t, font=f_pin, fill=(255, 255, 255))
    d.text((map_x0, map_y0 + map_h + 4), "Pins numbered to match the 30 stories below. Positions approximate.",
           font=SANS(9), fill=GREY)

    # legend
    lx, ly = 716, my + 20
    legend = [("North America", (24, 64, 120)), ("Europe", (178, 34, 34)),
              ("Middle East / Asia", (0, 90, 60)), ("Africa", (200, 160, 30)),
              ("Oceania / Pacific", (120, 40, 120)), ("Latin America", (30, 120, 160))]
    for name, col in legend:
        d.rectangle([lx, ly, lx + 14, ly + 14], fill=col)
        d.text((lx + 20, ly + 1), name, font=SANS(11), fill=INK)
        ly += 21
    d.text((lx, ly + 2), "Red pins = the day's stories.", font=SANS(10), fill=GREY)
    d.text((lx, ly + 17), "1\u20133 are the three heroes above;", font=SANS(10), fill=GREY)
    d.text((lx, ly + 32), "4\u201330 are the stories listed below.", font=SANS(10), fill=GREY)

    # ---- numbered list: 30 stories, 3 columns x 10 rows
    ly0 = 766
    d.text((MX, ly0), "THE DAY IN 30 STORIES", font=f_sec, fill=INK)
    hline(d, MX, W - MX, ly0 + 18, 1)
    stories = [
        "Democrats win 258 House seats, best since 1992 (BBC)",
        "NATO meets in Brussels over Poland missile fall (NATO)",
        "Kyiv region toll 12 as rescuers dig in Dymer (AFP)",
        "M6.5 quake strikes deep under Vanuatu region (USGS)",
        "Kospi falls 5.8% as AI rout grips Seoul (AP)",
        "COP31: 90+ states back electrification pledge (Reuters)",
        "Russian corvette Merkury sunk off Benghazi (AP)",
        "Sparta II towed away after Baltic drone hit (Yle)",
        "Indonesia factory fire: 24 dead, 30 missing (Reuters)",
        "South Sudan raid kills 24 civilians (AFP)",
        "Taiwan short-selling ban takes effect (FSC)",
        "Mexico seizes FBI-wanted \u2018Chapo Isidro\u2019 (WSJ)",
        "Youth Congress protests Meta, gives ultimatum (Guardian)",
        "UK, France, China block Nusseibeh UN bid (Guardian)",
        "NHS launches huge AI breast-screening trial (BBC)",
        "FIFA to confirm UK as 2035 World Cup host (BBC Sport)",
        "China cuts margin ratio to 80% to steady stocks (Reuters)",
        "Seoul vows to stabilise market after Kospi dive (Reuters)",
        "Nasdaq 100 enters bear market after Friday rout (Reuters)",
        "Anthropic slides 8.5% as AI trade unwinds (Bloomberg)",
        "Four nations urge Israel to let Gaza aid in (Joint stmt)",
        "US futures bounce as Monday trade steadies (Reuters)",
        "Netanyahu\u2013Eisenkot coalition talks collapse (One Turn)",
        "Burnham: EU deal could lift next decade (One Turn)",
        "Thousands rally in Istanbul over media takeover (One Turn)",
        "Nepal PM Balen Shah visits India on first trip (One Turn)",
        "Bolsonaro in intensive care, bowel blocked (One Turn)",
        "Colombia asks X to suspend Petro\u2019s account (One Turn)",
        "Mongolia parliament accepts president\u2019s exit (One Turn)",
        "M5.0 quake off Papua New Guinea (USGS)",
    ]
    assert len(stories) == 30
    f_item = SANS(10)
    f_num = SANS_B(10)
    col_w = 322
    row_h = 18
    y0 = ly0 + 26
    for i, s in enumerate(stories):
        col = i // 10
        row = i % 10
        cx = MX + col * (col_w + 8)
        cy = y0 + row * row_h
        num = str(i + 1) + "."
        d.text((cx, cy), num, font=f_num, fill=RED)
        nx = cx + d.textlength("30. ", font=f_num)
        d.text((nx, cy), s, font=f_item, fill=INK)

    # ---- date check (small, max 3 lines)
    dy = 968
    hline(d, MX, W - MX, dy, 1)
    f_dc = SANS_B(10)
    d.text((MX, dy + 6), "DATE CHECK \u2014 left out as stale:", font=f_dc, fill=INK)
    f_dcb = SANS(10)
    dc = ("Hormuz tanker strikes (Sat 22 Nov)  ·  Trump friendship photos with Putin and Xi (22 Nov)  ·  "
          "the COP31 collapse itself (Sun 22 Nov). Only Monday reporting \u2014 and Monday fallout \u2014 made this page.")
    draw_wrapped(d, dc, f_dcb, MX, dy + 20, W - 2 * MX, leading=12, max_lines=2)
    f_ft = SANS(8.5)
    ftxt = "Drawn from Monday\u2019s reporting. Sources named throughout. Still developing where marked."
    d.text(((W - d.textlength(ftxt, font=f_ft)) / 2, 1014), ftxt, font=f_ft, fill=GREY)

    out = os.path.join(out_dir, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
