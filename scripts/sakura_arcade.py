#!/usr/bin/env python3
"""Sakura Arcade: builds every SVG used by the fattsowavy profile README.

Run from the repository root:  python scripts/sakura_arcade.py
Static screens are always rebuilt. Daily screens (sakura-season, high-scores)
use the GitHub GraphQL API when GITHUB_TOKEN is set; FAKE_DATA=1 renders sample data.
Pure standard library, no pip install needed.
"""
import datetime as dt
import json
import os
import random
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
USER = os.environ.get("GH_USER", "fattsowavy")

# ── palette: taken from the sakura mochi cat ──────────────────────────────
BG, PANEL, DIM, LINE = "#14101F", "#1C1630", "#2A2140", "#4A3A66"
P1, P2, P3, P4, P5 = "#FFD6E5", "#F7B6CF", "#F49AB8", "#E9799C", "#B8476F"
CREAM, OUTL, WHITE, MUTED = "#FFF3D6", "#3F1F33", "#FFF6FA", "#A895B8"

# ── 5x7 pixel font ─────────────────────────────────────────────────────────
F = {
'A':[" ### ","#   #","#   #","#####","#   #","#   #","#   #"],
'B':["#### ","#   #","#   #","#### ","#   #","#   #","#### "],
'C':[" ### ","#   #","#    ","#    ","#    ","#   #"," ### "],
'D':["#### ","#   #","#   #","#   #","#   #","#   #","#### "],
'E':["#####","#    ","#    ","#### ","#    ","#    ","#####"],
'F':["#####","#    ","#    ","#### ","#    ","#    ","#    "],
'G':[" ### ","#   #","#    ","# ###","#   #","#   #"," ####"],
'H':["#   #","#   #","#   #","#####","#   #","#   #","#   #"],
'I':[" ### ","  #  ","  #  ","  #  ","  #  ","  #  "," ### "],
'J':["  ###","   # ","   # ","   # ","   # ","#  # "," ##  "],
'K':["#   #","#  # ","# #  ","##   ","# #  ","#  # ","#   #"],
'L':["#    ","#    ","#    ","#    ","#    ","#    ","#####"],
'M':["#   #","## ##","# # #","# # #","#   #","#   #","#   #"],
'N':["#   #","##  #","# # #","#  ##","#   #","#   #","#   #"],
'O':[" ### ","#   #","#   #","#   #","#   #","#   #"," ### "],
'P':["#### ","#   #","#   #","#### ","#    ","#    ","#    "],
'Q':[" ### ","#   #","#   #","#   #","# # #","#  # "," ## #"],
'R':["#### ","#   #","#   #","#### ","# #  ","#  # ","#   #"],
'S':[" ####","#    ","#    "," ### ","    #","    #","#### "],
'T':["#####","  #  ","  #  ","  #  ","  #  ","  #  ","  #  "],
'U':["#   #","#   #","#   #","#   #","#   #","#   #"," ### "],
'V':["#   #","#   #","#   #","#   #","#   #"," # # ","  #  "],
'W':["#   #","#   #","#   #","# # #","# # #","## ##","#   #"],
'X':["#   #","#   #"," # # ","  #  "," # # ","#   #","#   #"],
'Y':["#   #","#   #"," # # ","  #  ","  #  ","  #  ","  #  "],
'Z':["#####","    #","   # ","  #  "," #   ","#    ","#####"],
'0':[" ### ","#   #","#  ##","# # #","##  #","#   #"," ### "],
'1':["  #  "," ##  ","  #  ","  #  ","  #  ","  #  "," ### "],
'2':[" ### ","#   #","    #","   # ","  #  "," #   ","#####"],
'3':["#####","   # ","  #  ","   # ","    #","#   #"," ### "],
'4':["   # ","  ## "," # # ","#  # ","#####","   # ","   # "],
'5':["#####","#    ","#### ","    #","    #","#   #"," ### "],
'6':["  ## "," #   ","#    ","#### ","#   #","#   #"," ### "],
'7':["#####","    #","   # ","  #  "," #   "," #   "," #   "],
'8':[" ### ","#   #","#   #"," ### ","#   #","#   #"," ### "],
'9':[" ### ","#   #","#   #"," ####","    #","   # "," ##  "],
' ':["     "]*7,
'.':["     ","     ","     ","     ","     ","     ","  #  "],
'·':["     ","     ","     ","  #  ","     ","     ","     "],
',':["     ","     ","     ","     ","     ","  #  "," #   "],
':':["     ","  #  ","     ","     ","     ","  #  ","     "],
'!':["  #  ","  #  ","  #  ","  #  ","  #  ","     ","  #  "],
'?':[" ### ","#   #","    #","   # ","  #  ","     ","  #  "],
"'":["  #  ","  #  ","     ","     ","     ","     ","     "],
'-':["     ","     ","     ","#####","     ","     ","     "],
'+':["     ","  #  ","  #  ","#####","  #  ","  #  ","     "],
'/':["    #","    #","   # ","  #  "," #   ","#    ","#    "],
'&':[" ##  ","#  # ","# #  "," #   ","# # #","#  # "," ## #"],
'%':["##   ","##  #","   # ","  #  "," #   ","#  ##","   ##"],
'>':["#    "," #   ","  #  ","   # ","  #  "," #   ","#    "],
'<':["    #","   # ","  #  "," #   ","  #  ","   # ","    #"],
'(':["   # ","  #  "," #   "," #   "," #   ","  #  ","   # "],
')':[" #   ","  #  ","   # ","   # ","   # ","  #  "," #   "],
'#':[" # # ","#####"," # # "," # # "," # # ","#####"," # # "],
'=':["     ","     ","#####","     ","#####","     ","     "],
'*':["     "," # # ","  #  ","#####","  #  "," # # ","     "],
'▶':["#    ","##   ","###  ","#### ","###  ","##   ","#    "],
'▼':["     ","     ","#####"," ### ","  #  ","     ","     "],
}


def tw(s, px):
    """Pixel width of a string."""
    return len(s) * 6 * px - px


def text(s, x, y, px, fill, extra=""):
    d = []
    cx = x
    for ch in str(s).upper():
        for r, row in enumerate(F.get(ch, F['?'])):
            c = 0
            while c < 5:
                if row[c] == '#':
                    st = c
                    while c < 5 and row[c] == '#':
                        c += 1
                    d.append(f"M{cx+st*px} {y+r*px}h{(c-st)*px}v{px}h-{(c-st)*px}z")
                else:
                    c += 1
        cx += 6 * px
    return f'<path fill="{fill}" d="{"".join(d)}"{extra}/>'


def ctext(s, cx, y, px, fill, extra=""):
    return text(s, round(cx - tw(s, px) / 2), y, px, fill, extra)


def sprite(rows, pal, x, y, px):
    paths = {}
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            k = row[c]
            if k in pal:
                st = c
                while c < len(row) and row[c] == k:
                    c += 1
                paths.setdefault(pal[k], []).append(f"M{x+st*px} {y+r*px}h{(c-st)*px}v{px}h-{(c-st)*px}z")
            else:
                c += 1
    return "".join(f'<path fill="{col}" d="{"".join(d)}"/>' for col, d in paths.items())


# ── sprites ────────────────────────────────────────────────────────────────
CAT_BODY = [
    "...kk.........kk...",
    "..kpk.........kpk..",
    "..kppkkkkkkkkkppk..",
    ".kgggggggggssgggggk",
    "kgggggggggggggggggk",
    "kggEEgggggggggEEggk",
    "kggEEgggggggggEEggk",
    "kgcccgggkgkgggcccgk",
    "kggggggggkggggggggk",
    "kgggggggggggggggggk",
    "kgggggggggggggggggk",
    ".kgggggggggggggggk.",
    "..kgggggggggggggk..",
    "...kkkkkkkkkkkkk...",
]
CAT_TAIL_A = [".kk", "kpk", "kgk", "kgk", "kk."]
CAT_TAIL_B = ["...", "kk.", "kpk", "kgk", "kk."]
CAT_PAL = {'k': OUTL, 'g': WHITE, 'p': P2, 'c': P3, 's': P4}


def cat_rows(tail, eyes="open"):
    g = [['.'] * 23 for _ in range(14)]
    for y, row in enumerate(CAT_BODY):
        for x, ch in enumerate(row):
            if ch != '.':
                g[y][x] = ch
    for y, row in enumerate(tail):
        for x, ch in enumerate(row):
            if ch != '.':
                g[5 + y][19 + x] = ch
    for y in range(14):
        for x in range(23):
            if g[y][x] == 'E':
                g[y][x] = 'k' if eyes == "open" else 'g'
    if eyes != "open":
        for x in (3, 4, 14, 15):
            g[6][x] = 'k'
    return [''.join(r) for r in g]


def mochi_cat(x, y, px, sleeping=False):
    """Animated sakura mochi cat: tail wag, blink (or asleep), gentle bounce."""
    parts = []
    for cls, tail in (("fa", CAT_TAIL_A), ("fb", CAT_TAIL_B)):
        if sleeping:
            parts.append(f'<g class="{cls}">{sprite(cat_rows(tail, "closed"), CAT_PAL, x, y, px)}</g>')
        else:
            parts.append(f'<g class="{cls}"><g class="eo">{sprite(cat_rows(tail), CAT_PAL, x, y, px)}</g>'
                         f'<g class="ec">{sprite(cat_rows(tail, "closed"), CAT_PAL, x, y, px)}</g></g>')
    return f'<g class="{"breathe" if sleeping else "bounce"}">{"".join(parts)}</g>'


HERO = [
    "   K KK K   ",
    " KKKKKKKKK  ",
    "KKKKKKKKKKK ",
    "KKSKSSKSSKK ",
    " KSSSSSSSK  ",
    " SSESSSESS  ",
    " SSSSSSSSS  ",
    "  SSSMMSS   ",
    "   SSSSS    ",
    " JJJWWWJJJ  ",
    "JJJJWRWJJJJ ",
    "SJJJJWJJJJS ",
    "S JJJJJJJ S ",
    "  PPP PPP   ",
    "  PPP PPP   ",
    " BBBB BBBB  ",
]
HERO_PAL = {'K': '#1A1A22', 'S': '#C68B59', 'E': '#1A1A22', 'M': '#8A4B2A', 'W': '#F0F0F0',
            'R': P4, 'J': '#2E3A5C', 'P': '#1F2740', 'B': '#0A0A10'}
COIN = ["  OOOO  ", " OYYYYO ", "OYLYYYYO", "OYLYYYYO", "OYLYYYYO", "OYYYYYDO", " OYYYDO ", "  OOOO  "]
COIN_PAL = {'O': P5, 'Y': P3, 'L': P1, 'D': P4}
BLOSSOM = ["..p..", ".ppp.", "ppspp", ".ppp.", ".p.p."]
PETAL = ["pp.", ".pp"]
HEART = [".p.p.", "ppppp", ".ppp.", "..p.."]
TROPHY = [
    "oooooooooooo",
    "oYYYYYYYYYYo",
    "YoYYYYYYYYoY",
    "Y.oYYYLYYo.Y",
    ".Y.oYYLYo.Y.",
    "..YoYYYYoY..",
    "....oYYo....",
    ".....oo.....",
    ".....YY.....",
    "....oYYo....",
    "...oYYYYo...",
    "..oooooooo..",
]
TROPHY_PAL = {'o': OUTL, 'Y': CREAM, 'L': WHITE}
ARROW_UP = ["   #   ", "  ###  ", " ##### ", "#######", "  ###  ", "  ###  ", "  ###  "]


def rot(rows):  # 90° clockwise
    return [''.join(rows[len(rows) - 1 - r][c] for r in range(len(rows))) for c in range(len(rows[0]))]


ARROW_RIGHT = rot(ARROW_UP)
ARROW_DOWN = rot(ARROW_RIGHT)
ARROW_LEFT = rot(ARROW_DOWN)

# ── shared scenery ─────────────────────────────────────────────────────────
CSS = """
.tw{animation:tw 2.6s steps(2) infinite}@keyframes tw{0%{opacity:1}50%{opacity:.2}}
.blink{animation:bl 1.1s steps(1) infinite}@keyframes bl{0%{opacity:1}60%{opacity:0}}
.bounce{animation:bn 1.2s steps(1) infinite}@keyframes bn{0%{transform:translateY(0)}50%{transform:translateY(-5px)}}
.breathe{animation:br 2.4s steps(1) infinite}@keyframes br{0%{transform:translateY(0)}50%{transform:translateY(2px)}}
.fa{animation:fa .6s steps(1) infinite}.fb{animation:fb .6s steps(1) infinite}
@keyframes fa{0%{opacity:1}50%{opacity:0}}@keyframes fb{0%{opacity:0}50%{opacity:1}}
.eo{animation:eo 4s steps(1) infinite}.ec{animation:ec 4s steps(1) infinite}
@keyframes eo{0%{opacity:1}92%{opacity:0}97%{opacity:1}}@keyframes ec{0%{opacity:0}92%{opacity:1}97%{opacity:0}}
.rise{animation:rs 3.2s steps(16) infinite}@keyframes rs{0%{transform:translateY(0);opacity:0}10%{opacity:1}70%{opacity:1}100%{transform:translateY(-44px);opacity:0}}
.bob{animation:bo 1s steps(1) infinite}@keyframes bo{0%{transform:translateY(0)}50%{transform:translateY(-6px)}}
"""


def fall_css(h):
    return (f"@keyframes f1{{0%{{transform:translate(0,-20px)}}50%{{transform:translate(60px,{h//2}px)}}100%{{transform:translate(20px,{h+20}px)}}}}"
            f"@keyframes f2{{0%{{transform:translate(0,-20px)}}50%{{transform:translate(-50px,{h//2}px)}}100%{{transform:translate(30px,{h+20}px)}}}}"
            f"@keyframes f3{{0%{{transform:translate(0,-20px)}}50%{{transform:translate(90px,{h//2}px)}}100%{{transform:translate(140px,{h+20}px)}}}}"
            ".f1{animation:f1 7s steps(70) infinite}.f2{animation:f2 9s steps(90) infinite}.f3{animation:f3 8s steps(80) infinite}")


def svg(w, h, body, extra_css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" shape-rendering="crispEdges">'
            f'<style>{CSS}{extra_css}</style>{body}</svg>')


def frame(w, h, col=LINE, t=4):
    return f'<rect x="{t/2}" y="{t/2}" width="{w-t}" height="{h-t}" fill="none" stroke="{col}" stroke-width="{t}"/>'


def stars(rng, n, w, y0, y1):
    out = []
    for _ in range(n):
        x, y = rng.randint(10, w - 10), rng.randint(y0, y1)
        s = rng.choice([2, 2, 3])
        col = rng.choice([WHITE, WHITE, P2, CREAM])
        out.append(f'<rect class="tw" style="animation-delay:-{rng.uniform(0, 2.6):.2f}s" x="{x}" y="{y}" width="{s}" height="{s}" fill="{col}"/>')
    return "".join(out)


def petals(rng, n, w):
    out = []
    for _ in range(n):
        cls = rng.choice(["f1", "f2", "f3"])
        dur = {"f1": 7, "f2": 9, "f3": 8}[cls]
        col = rng.choice([P1, P2, P3])
        out.append(f'<g class="{cls}" style="animation-delay:-{rng.uniform(0, dur):.2f}s">'
                   f'{sprite(PETAL, {"p": col}, rng.randint(-30, w - 60), 0, 3)}</g>')
    return "".join(out)


def moon(cx, cy, r=7, p=5):
    out = []
    for gy in range(-r, r + 1):
        for gx in range(-r, r + 1):
            if gx * gx + gy * gy <= r * r + 2:
                col = "#EAD9B4" if (gx, gy) in {(-2, -2), (-3, -2), (2, 3), (3, 1)} else CREAM
                out.append(f'<rect x="{cx+gx*p}" y="{cy+gy*p}" width="{p}" height="{p}" fill="{col}"/>')
    return "".join(out)


def branch(segs, blossoms):
    out = []
    for x, y, w in segs:
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="10" fill="#5A3A2E"/><rect x="{x}" y="{y}" width="{w}" height="3" fill="#7A5240"/>')
    for i, (bx, by) in enumerate(blossoms):
        pal = {'p': P2 if i % 2 else P3, 's': P4 if i % 2 else CREAM}
        out.append(sprite(BLOSSOM, pal, bx, by, 4))
    return "".join(out)


# ── 1. ATTRACT MODE (title banner) ─────────────────────────────────────────
def attract():
    W, H = 880, 300
    rng = random.Random(3)
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', stars(rng, 50, W, 50, 240), moon(610, 82)]
    b.append(text("1UP", 24, 16, 2, P4))
    b.append(text("003870", 66, 16, 2, WHITE, ' class="blink"'))
    b.append(ctext("HI-SCORE 999999", W / 2, 16, 2, CREAM))
    b.append(sprite(COIN, COIN_PAL, 772, 14, 2) + text("X04", 794, 16, 2, WHITE))
    b.append(f'<rect x="16" y="40" width="{W-32}" height="2" fill="{LINE}"/>')
    for line, y in (("MUH FATWAH", 72), ("FAJRIANSYAH M", 128)):
        b.append(text(line, 44, y + 4, 6, "#5A2440"))
        b.append(text(line, 40, y, 6, P2))
    b.append(text("SPEECH AI · NLP · WEB & MOBILE", 42, 190, 2, CREAM))
    b.append(text("▶ PRESS START", 42, 226, 3, P1, ' class="blink"'))
    b.append(branch([(560, 236, 120), (680, 232, 200)], [(574, 222), (628, 244), (842, 222), (800, 246), (668, 248)]))
    b.append(mochi_cat(706, 232 - 14 * 5 + 2, 5))
    for i, dx in enumerate((-6, 118)):
        b.append(f'<g class="rise" style="animation-delay:-{i*1.6:.1f}s">{sprite(HEART, {"p": P3}, 706 + dx, 170, 3)}</g>')
    b.append(f'<rect x="0" y="{H-26}" width="{W}" height="26" fill="{PANEL}"/><rect x="0" y="{H-26}" width="{W}" height="2" fill="{P4}" opacity=".6"/>')
    b.append(ctext("SAKURA ARCADE · INSERT COIN", W / 2, H - 17, 1, MUTED))
    b.append(petals(rng, 18, W))
    b.append(frame(W, H))
    return svg(W, H, "".join(b), fall_css(H))


# ── 2. INSERT COIN buttons ─────────────────────────────────────────────────
def coin_button(label):
    W, H = 34 + tw(label, 2) + 22, 44
    b = [f'<rect x="2" y="2" width="{W-4}" height="{H-4}" fill="{BG}"/>',
         f'<rect x="4" y="0" width="{W-8}" height="2" fill="{P3}"/><rect x="4" y="{H-2}" width="{W-8}" height="2" fill="{P3}"/>',
         f'<rect x="0" y="4" width="2" height="{H-8}" fill="{P3}"/><rect x="{W-2}" y="4" width="2" height="{H-8}" fill="{P3}"/>',
         f'<rect x="2" y="2" width="2" height="2" fill="{P3}"/><rect x="{W-4}" y="2" width="2" height="2" fill="{P3}"/>',
         f'<rect x="2" y="{H-4}" width="2" height="2" fill="{P3}"/><rect x="{W-4}" y="{H-4}" width="2" height="2" fill="{P3}"/>',
         f'<rect x="4" y="{H-6}" width="{W-8}" height="2" fill="{P5}"/>',
         f'<g class="bounce">{sprite(COIN, COIN_PAL, 12, 14, 2)}</g>',
         text(label, 34, 15, 2, P1)]
    return W, svg(W, H, "".join(b))


# ── 3. MOCHI SAYS (dialog) ─────────────────────────────────────────────────
def mochi_says():
    W, H = 880, 196
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    b.append(f'<rect x="16" y="30" width="150" height="150" fill="{PANEL}" stroke="{P3}" stroke-width="4"/>')
    b.append(mochi_cat(30, 70, 5))
    b.append(f'<rect x="184" y="30" width="680" height="150" fill="{PANEL}" stroke="{P3}" stroke-width="4"/>')
    b.append(f'<rect x="192" y="38" width="664" height="134" fill="none" stroke="{OUTL}" stroke-width="2"/>')
    b.append(f'<rect x="200" y="12" width="{tw("MOCHI SAYS", 2)+24}" height="28" fill="{P4}"/>')
    b.append(text("MOCHI SAYS", 212, 19, 2, BG))
    lines = [
        ("", "PSST! HERE'S WHAT PLAYER 1 IS UP TO...", CREAM),
        ("MAIN  ", "TEACHING MACHINES TO UNDERSTAND MY THOUGHTS", P1),
        ("SIDE  ", "WEB & MOBILE APPS WITH LARAVEL & FLUTTER", P1),
        ("GRIND ", "LEVELING UP IN NATURAL LANGUAGE PROCESSING", P1),
    ]
    defs = []
    cycle, per = 12.0, 2.0
    for i, (label, body, col) in enumerate(lines):
        y = 56 + i * 28
        full = label + body
        width = tw(full, 2) + 4
        t0, t1 = (i * per) / cycle, ((i + 1) * per - 0.3) / cycle
        defs.append(f'<clipPath id="c{i}"><rect x="210" y="{y-2}" height="18" width="0">'
                    f'<animate attributeName="width" values="0;0;{width};{width};0" keyTimes="0;{t0:.3f};{t1:.3f};0.97;1" '
                    f'dur="{cycle}s" repeatCount="indefinite"/></rect></clipPath>')
        g = (text(label, 212, y, 2, P4) if label else "") + text(body, 212 + len(label) * 12, y, 2, col)
        b.append(f'<g clip-path="url(#c{i})">{g}</g>')
    b.append(text("▼", 832, 156, 2, P3, ' class="blink"'))
    return svg(W, H, f'<defs>{"".join(defs)}</defs>' + "".join(b))


# ── 4. CHARACTER SELECT ────────────────────────────────────────────────────
STATS = [("SPEECH AI", 8), ("NLP", 8), ("PYTHON", 9), ("WEB", 7), ("MOBILE", 6)]


def character_select():
    W, H = 880, 290
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    b.append(ctext("CHARACTER SELECT", W / 2, 18, 3, P2))
    b.append(f'<rect x="16" y="52" width="{W-32}" height="2" fill="{LINE}"/>')
    # portrait
    b.append(f'<rect x="24" y="70" width="200" height="200" fill="{PANEL}"/>')
    for (x, y, w, h) in ((20, 66, 40, 6), (20, 66, 6, 40), (188, 66, 40, 6), (222, 66, 6, 40),
                         (20, 268, 40, 6), (20, 234, 6, 40), (188, 268, 40, 6), (222, 234, 6, 40)):
        b.append(f'<rect class="blink" x="{x}" y="{y}" width="{w}" height="{h}" fill="{P3}"/>')
    b.append(f'<g class="bob">{sprite(HERO, HERO_PAL, 76, 86, 8)}</g>')
    b.append(ctext("FATWAH", 124, 244, 3, CREAM))
    b.append(text("P1", 32, 78, 2, P4))
    # info
    info = [("CLASS", "RESEARCHER / DEVELOPER"), ("GUILD", "UNIVERSITAS MUSLIM INDONESIA"),
            ("SPAWN", "MAKASSAR, INDONESIA"), ("LV", "3.87 GPA")]
    for i, (k, v) in enumerate(info):
        y = 74 + i * 22
        b.append(text(k, 256, y, 2, P4) + text(v, 336, y, 2, P1))
    # stat bars
    css = []
    for i, (name, lvl) in enumerate(STATS):
        y = 170 + i * 22
        b.append(text(name, 256, y, 2, CREAM))
        for s in range(10):
            x = 384 + s * 26
            if s < lvl:
                d = (i * 10 + s) * 0.04
                b.append(f'<rect x="{x}" y="{y-1}" width="22" height="16" fill="{DIM}"/>'
                         f'<rect class="fill" style="animation-delay:{d:.2f}s" x="{x}" y="{y-1}" width="22" height="16" fill="{P3 if s < 7 else P2}"/>')
            else:
                b.append(f'<rect x="{x}" y="{y-1}" width="22" height="16" fill="{DIM}"/>')
    css.append(".fill{opacity:0;animation:fl 7s steps(1) infinite}@keyframes fl{0%{opacity:1}92%{opacity:0}}")
    b.append(ctext("READY?", 774, 176, 3, P2))
    b.append(ctext("PRESS A", 774, 212, 2, P1, ' class="blink"'))
    b.append(f'<rect x="744" y="236" width="60" height="28" fill="{P4}"/>' + ctext("A", 774, 243, 2, BG))
    return svg(W, H, "".join(b), "".join(css))


# ── 5. CARTRIDGE SELECT ────────────────────────────────────────────────────
CARTRIDGES = [
    ("lab-loan", "LAB LOAN SYSTEM", "LAB RESERVATIONS", "PHP · MYSQL", P2),
    ("lab-chatbot", "LAB CHATBOT", "ICLABS HELPDESK", "FASTAPI · PYTHON", P3),
    ("bitbooth", "BITBOOTH", "PIXEL PHOTOBOOTH", "REACT · VITE", P1),
    ("cinema", "CINEMA SEAT BOOK", "SEAT BOOKING APP", "FLASK · XML-RPC", P3),
    ("shortener", "URL SHORT + QR", "AUTO QR LINKS", "FLASK · SQLITE", P2),
    ("portfolio", "PORTFOLIO", "RETRO ARCADE SITE", "REACT · TAILWIND", P1),
]


def cartridge_title():
    W, H = 880, 48
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         ctext("< CARTRIDGE SELECT >", W / 2, 12, 3, P2),
         f'<rect x="16" y="{H-4}" width="{W-32}" height="2" fill="{LINE}"/>']
    return svg(W, H, "".join(b))


def cartridge(num, title, desc, tech, sticker):
    W, H = 280, 210
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    # body with notched top
    b.append(f'<rect x="20" y="16" width="240" height="180" fill="{DIM}"/>')
    b.append(f'<rect x="20" y="16" width="240" height="180" fill="none" stroke="{OUTL}" stroke-width="4"/>')
    b.append(f'<rect x="20" y="10" width="200" height="8" fill="{DIM}"/><rect x="20" y="8" width="200" height="4" fill="{OUTL}"/>')
    for i in range(6):
        b.append(f'<rect x="{40+i*12}" y="22" width="6" height="12" fill="{LINE}"/>')
    # sticker
    b.append(f'<rect x="34" y="42" width="212" height="104" fill="{sticker}"/>')
    b.append(f'<rect x="40" y="48" width="200" height="92" fill="none" stroke="{OUTL}" stroke-width="2"/>')
    b.append(text(f"NO.{num:02d}", 48, 56, 1, OUTL))
    b.append(sprite(BLOSSOM, {'p': P5, 's': CREAM}, 216, 54, 3))
    b.append(ctext(title, 140, 84, 2, OUTL))
    b.append(ctext(desc, 140, 112, 1, P5))
    # shine sweep
    b.append('<clipPath id="st"><rect x="34" y="42" width="212" height="104"/></clipPath>'
             f'<g clip-path="url(#st)"><rect class="shine" x="-40" y="30" width="18" height="140" fill="{WHITE}" opacity=".45" transform="skewX(-20)"/></g>')
    b.append(ctext(tech, 140, 160, 1, CREAM))
    b.append(ctext("▶ PLAY", 140, 176, 2, P3, ' class="blink"'))
    css = ".shine{animation:sh 4s steps(24) infinite}@keyframes sh{0%{transform:skewX(-20deg) translateX(0)}60%{transform:skewX(-20deg) translateX(360px)}100%{transform:skewX(-20deg) translateX(360px)}}"
    return svg(W, H, "".join(b), css)


# ── 6. ACHIEVEMENT UNLOCKED ────────────────────────────────────────────────
def achievement():
    W, H = 880, 124
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    g = [f'<rect x="120" y="18" width="640" height="88" fill="{PANEL}"/>',
         f'<rect x="120" y="18" width="640" height="88" fill="none" stroke="{P3}" stroke-width="4"/>',
         f'<rect x="132" y="28" width="68" height="68" fill="{P4}"/>',
         sprite(TROPHY, TROPHY_PAL, 142, 38, 4),
         text("ACHIEVEMENT UNLOCKED", 220, 32, 2, P3),
         text("IEEE PAPER PUBLISHED", 220, 54, 3, P1),
         text("ASR FOR THE MAKASSAR DIALECT · IMCOM 2026", 220, 86, 1, CREAM),
         text("+100 XP", 666, 32, 2, P4, ' class="blink"'),
         '<clipPath id="ac"><rect x="120" y="18" width="640" height="88"/></clipPath>'
         f'<g clip-path="url(#ac)"><rect class="shine" x="60" y="0" width="24" height="130" fill="{WHITE}" opacity=".25"/></g>']
    b.append(f'<g class="pop">{"".join(g)}</g>')
    css = (".pop{animation:pp 9s steps(1) infinite}@keyframes pp{0%{transform:translateY(-8px)}3%{transform:translateY(0)}100%{transform:translateY(0)}}"
           ".shine{animation:sh 9s steps(30) infinite}@keyframes sh{0%{transform:translateX(0)}20%{transform:translateX(760px)}100%{transform:translateX(760px)}}")
    for x in (100, 780):
        b.append(sprite(BLOSSOM, {'p': P3, 's': CREAM}, x - 10, 50, 4).replace('<path', '<path class="tw"'))
    return svg(W, H, "".join(b), css)


# ── 9. ENTER CHEAT CODE (summary of <details>) ─────────────────────────────
def cheat():
    W, H = 880, 72
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<rect x="2" y="2" width="{W-4}" height="{H-4}" fill="{PANEL}" stroke="{LINE}" stroke-width="4"/>',
         text("ENTER CHEAT CODE", 22, 30, 2, P3)]
    keys = [ARROW_UP, ARROW_UP, ARROW_DOWN, ARROW_DOWN, ARROW_LEFT, ARROW_RIGHT, ARROW_LEFT, ARROW_RIGHT, "B", "A"]
    x = 236
    n = len(keys)
    for i, k in enumerate(keys):
        d = i * 0.4
        box = f'<rect x="{x}" y="18" width="36" height="36" fill="{DIM}"/>'
        lit = f'<rect class="key" style="animation-delay:{d:.1f}s" x="{x}" y="18" width="36" height="36" fill="{P4}"/>'
        if isinstance(k, str):
            glyph = text(k, x + 13, 29, 2, P1)
        else:
            glyph = sprite(k, {'#': P1}, x + 11, 29, 2)
        b.append(box + lit + glyph)
        x += 42 if i < n - 1 else 0
    b.append(text("CLICK TO UNLOCK", 668, 30, 2, P1, ' class="blink"'))
    css = (f".key{{opacity:0;animation:ky 6s steps(1) infinite}}"
           f"@keyframes ky{{0%{{opacity:1}}{(0.4/6)*100:.1f}%{{opacity:0}}100%{{opacity:0}}}}")
    return svg(W, H, "".join(b), css)


# ── 10. CONTINUE? ──────────────────────────────────────────────────────────
def continue_screen():
    W, H = 880, 270
    rng = random.Random(9)
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', stars(rng, 30, W, 10, 200)]
    b.append(ctext("CONTINUE?", W / 2, 24, 5, P2))
    for i in range(10):
        digit = str(9 - i)
        b.append(f'<g class="dg" style="animation-delay:{i}s">{ctext(digit, W / 2, 86, 8, P1)}</g>')
    b.append(f'<g class="th">{ctext("THANKS FOR PLAYING!", W / 2, 110, 3, CREAM)}'
             f'{ctext("SEE YOU NEXT STAGE", W / 2, 146, 2, P3)}</g>')
    b.append(branch([(600, 230, 280)], [(620, 216), (700, 240), (820, 214), (860, 238)]))
    b.append(mochi_cat(700, 230 - 14 * 5 + 2, 5, sleeping=True))
    for i, (dx, s) in enumerate(((112, 2), (126, 3), (142, 4))):
        b.append(f'<g class="rise" style="animation-delay:-{i*1.0:.1f}s">{text("Z", 700 + dx, 150 - i * 6, s, P2)}</g>')
    b.append(f'<rect x="0" y="{H-18}" width="{W}" height="18" fill="{PANEL}"/>')
    b.append(text("2026 SAKURA ARCADE · MUH FATWAH FAJRIANSYAH M", 24, H - 12, 1, MUTED))
    b.append(petals(rng, 12, W))
    b.append(frame(W, H))
    css = (".dg{opacity:0;animation:dg 14s steps(1) infinite}@keyframes dg{0%{opacity:1}7.14%{opacity:0}100%{opacity:0}}"
           ".th{animation:th 14s steps(1) infinite}@keyframes th{0%{opacity:0}71.4%{opacity:1}100%{opacity:1}}" + fall_css(H))
    return svg(W, H, "".join(b), css)


# ── daily data ─────────────────────────────────────────────────────────────
QUERY = """query($login:String!){user(login:$login){
  followers{totalCount}
  contributionsCollection{totalCommitContributions restrictedContributionsCount
    contributionCalendar{totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}}
  repositories(ownerAffiliations:OWNER,isFork:false,privacy:PUBLIC,first:100){totalCount
    nodes{languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name}}}}}}}"""

LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}


def fetch():
    req = urllib.request.Request("https://api.github.com/graphql",
                                 data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
                                 headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}",
                                          "Content-Type": "application/json", "User-Agent": "sakura-arcade"})
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.load(r)
    if "errors" in res:
        raise RuntimeError(res["errors"])
    u = res["data"]["user"]
    cc = u["contributionsCollection"]
    days = [(d["date"], d["contributionCount"], LEVEL.get(d["contributionLevel"], 0))
            for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    langs = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    return {"total": cc["contributionCalendar"]["totalContributions"], "commits": cc["totalCommitContributions"],
            "repos": u["repositories"]["totalCount"], "followers": u["followers"]["totalCount"],
            "days": days, "langs": langs}


def fake():
    rng = random.Random(1)
    start = dt.date.today() - dt.timedelta(days=364 + (dt.date.today().weekday() + 1) % 7)
    days = []
    for i in range((dt.date.today() - start).days + 1):
        c = rng.choice([0, 0, 0, 1, 2, 3, 5, 9])
        days.append(((start + dt.timedelta(i)).isoformat(), c, min(4, (c + 1) // 2)))
    return {"total": 621, "commits": 179, "repos": 12, "followers": 9, "days": days,
            "langs": {"Python": 900, "Jupyter Notebook": 300, "JavaScript": 200, "PHP": 150, "Dart": 90, "HTML": 60}}


def streaks(days):
    counts = [c for _, c, _ in days]
    best = run = 0
    for c in counts:
        run = run + 1 if c > 0 else 0
        best = max(best, run)
    cur, i = 0, len(counts) - 1
    if i >= 0 and counts[i] == 0:
        i -= 1  # today not played yet: count from yesterday
    while i >= 0 and counts[i] > 0:
        cur += 1
        i -= 1
    return cur, best


# ── 7. SAKURA SEASON (contribution calendar as blossoms) ───────────────────
BLOOM = {
    1: (["...", ".p.", "..."], P5),
    2: ([".p.", "psp", ".p."], P4),
    3: (["..p..", ".ppp.", "ppspp", ".ppp.", ".p.p."], P3),
    4: (["..p..", ".ppp.", "ppspp", ".ppp.", ".p.p."], P1),
}


def sakura_season(data):
    W, H = 880, 236
    cell = 14
    days = data["days"]
    weeks = []
    for i in range(0, len(days), 7):
        weeks.append(days[i:i + 7])
    weeks = weeks[-53:]
    x0 = (W - len(weeks) * cell) // 2
    y0 = 78
    defs = [f'<symbol id="b0" viewBox="0 0 14 14"><rect x="5" y="5" width="4" height="4" fill="{DIM}"/></symbol>']
    for lvl, (rows, col) in BLOOM.items():
        n = len(rows)
        off = (14 - n * 2) // 2
        inner = sprite(rows, {'p': col, 's': CREAM if lvl > 2 else col}, off, off, 2)
        defs.append(f'<symbol id="b{lvl}" viewBox="0 0 14 14">{inner}</symbol>')
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         text("SAKURA SEASON", 24, 20, 3, P2),
         text(f"{data['total']} PETALS IN THE LAST YEAR", W - 24 - tw(f"{data['total']} PETALS IN THE LAST YEAR", 2), 24, 2, CREAM),
         f'<rect x="16" y="50" width="{W-32}" height="2" fill="{LINE}"/>']
    last_month = None
    for wi, week in enumerate(weeks):
        m = week[0][0][5:7]
        if m != last_month and wi < len(weeks) - 2:
            name = dt.date(2000, int(m), 1).strftime("%b").upper()
            b.append(text(name, x0 + wi * cell, y0 - 14, 1, MUTED))
            last_month = m
        for di, (date, count, lvl) in enumerate(week):
            cls = ' class="tw"' if lvl == 4 else ""
            b.append(f'<use href="#b{lvl}" x="{x0+wi*cell}" y="{y0+di*cell}" width="14" height="14"{cls}/>')
    ly = y0 + 7 * cell + 16
    lx = W - 24 - (tw("LESS", 1) + 8 + 5 * 16 + 8 + tw("MORE", 1))
    b.append(text("LESS", lx, ly + 4, 1, MUTED))
    for i in range(5):
        b.append(f'<use href="#b{i}" x="{lx + tw("LESS", 1) + 8 + i*16}" y="{ly}" width="14" height="14"/>')
    b.append(text("MORE", lx + tw("LESS", 1) + 8 + 5 * 16 + 8, ly + 4, 1, MUTED))
    b.append(text("EACH BLOSSOM = ONE DAY OF CODE", 24, ly + 4, 1, MUTED))
    return svg(W, H, f'<defs>{"".join(defs)}</defs>' + "".join(b))


# ── 8. HIGH SCORES ─────────────────────────────────────────────────────────
def high_scores(data):
    W, H = 880, 330
    cur, best = streaks(data["days"])
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         ctext("HIGH SCORES", W / 2, 18, 4, P2),
         f'<rect x="16" y="58" width="{W-32}" height="2" fill="{LINE}"/>',
         text("RANK  SCORE   NAME", 40, 78, 2, P4)]
    rows = [("1ST", data["total"], "CONTRIBUTIONS", P1), ("2ND", data["commits"], "COMMITS", P2),
            ("3RD", best, "BEST STREAK", P3), ("4TH", cur, "STREAK NOW", P4), ("5TH", data["repos"], "PUBLIC REPOS", CREAM)]
    for i, (rank, score, name, col) in enumerate(rows):
        y = 112 + i * 32
        extra = ' class="blink"' if i == 0 else ""
        b.append(text(f"{rank}  {score:06d}  {name}", 40, y, 2, col, extra))
    b.append(f'<rect x="478" y="78" width="2" height="190" fill="{LINE}"/>')
    b.append(text("TOP WEAPONS", 506, 78, 2, P4))
    total = sum(data["langs"].values()) or 1
    top = sorted(data["langs"].items(), key=lambda kv: -kv[1])[:5]
    shades = [P1, P2, P3, P4, P5]
    for i, (name, size) in enumerate(top):
        y = 112 + i * 32
        pct = size * 100 / total
        short = {"JUPYTER NOTEBOOK": "JUPYTER", "JAVASCRIPT": "JS", "TYPESCRIPT": "TS"}
        label = short.get(name.upper(), name.upper())[:9]
        b.append(text(label, 506, y, 2, CREAM))
        segs = max(1, round(pct / 100 * 12)) if pct > 0 else 0
        for s in range(12):
            b.append(f'<rect x="{622+s*13}" y="{y}" width="10" height="14" fill="{shades[i] if s < segs else DIM}"/>')
        b.append(text(f"{pct:4.1f}%".strip(), 784, y, 2, MUTED))
    b.append(ctext("INSERT COIN TO BEAT THESE SCORES", W / 2, 284, 2, P3, ' class="blink"'))
    b.append(ctext(f"UPDATED {dt.date.today().isoformat()}", W / 2, 308, 1, MUTED))
    b.append(frame(W, H))
    return svg(W, H, "".join(b))


# ── main ───────────────────────────────────────────────────────────────────
def write(name, content):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(content, encoding="utf-8")
    print(f"  wrote assets/{name} ({len(content)//1024} KB)")


def main():
    print("Sakura Arcade: building screens")
    write("attract.svg", attract())
    for label, slug in (("PORTFOLIO", "portfolio"), ("CV", "cv"), ("LINKEDIN", "linkedin"), ("EMAIL", "email")):
        write(f"coin-{slug}.svg", coin_button(label)[1])
    write("mochi-says.svg", mochi_says())
    write("character-select.svg", character_select())
    write("cartridge-title.svg", cartridge_title())
    for i, (slug, title, desc, tech, col) in enumerate(CARTRIDGES, 1):
        write(f"cart-{slug}.svg", cartridge(i, title, desc, tech, col))
    write("achievement.svg", achievement())
    write("cheat-code.svg", cheat())
    write("continue.svg", continue_screen())
    data = None
    if os.environ.get("FAKE_DATA"):
        data = fake()
    elif os.environ.get("GITHUB_TOKEN"):
        try:
            data = fetch()
        except Exception as e:  # keep yesterday's scoreboard if the API hiccups
            print(f"  ! GitHub API failed: {e}")
    if data:
        write("sakura-season.svg", sakura_season(data))
        write("high-scores.svg", high_scores(data))
    else:
        print("  (no data: daily screens skipped)")


if __name__ == "__main__":
    main()
