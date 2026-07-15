#!/usr/bin/env python3
"""Renders the profile banner into light_mode.svg / dark_mode.svg.

The face is ASCII art emitted as <tspan> rows, not an embedded raster, so the
whole banner is a few KB of text that recolors per theme.

Two renderings are produced. Dense characters read as dark ink on a light
background but as bright pixels on a dark one, so the luminance ramp is
inverted for the dark theme; reusing one rendering would look photo-negative
in whichever theme it wasn't built for.

Regenerate with:  python3 generate_banner.py
"""

import pathlib
from xml.sax.saxutils import escape

from PIL import Image, ImageOps

FACE_SRC = pathlib.Path("face.png")  # RGBA cutout; alpha drives the blanking

RAMP = " .-=+*x#$&X@"  # sparse -> dense
COLS = 46
ALPHA_CUT = 110
CHAR_ASPECT = 2.08  # Consolas cell at font-size 16 / line-height 20

PROMPT = "piotr@realytica"
STATS = [
    ("OS", "Ubuntu 26.04 · macOS Tahoe 26.5.2 · Win 11"),
    ("Kernel", "Python · Go · TypeScript · C# · C++23"),
    ("DB", "PostgreSQL 17 + PostGIS · 7M records"),
    ("Spatial", "custom Google S2 index over gRPC"),
    ("Frontend", "Next.js 16 · React 19 · Mapbox GL"),
    ("Network", "OPNsense · Proxmox"),
    ("Location", "Chicago, IL"),
]

THEMES = {
    "light_mode.svg": {
        "bg": "#f6f8fa",
        "face": "#24292f",
        "prompt": "#953800",
        "key": "#953800",
        "value": "#0a3069",
        "rule": "#8c959f",
        "dark": False,
    },
    "dark_mode.svg": {
        "bg": "#161b22",
        "face": "#c9d1d9",
        "prompt": "#ffa657",
        "key": "#ffa657",
        "value": "#a5d6ff",
        "rule": "#616e7f",
        "dark": True,
    },
}

FS, LH = 16, 20  # font-size, line-height
FACE_X, TOP_Y = 15, 30
STATS_X = 480
VALUE_X = 580  # absolute, so alignment survives font substitution
PAD = 20

# Consolas advance width at font-size 16 with size-adjust 109%. Only used to
# size the canvas, and deliberately rounded up: a substituted font that runs
# slightly wide should still fit rather than clip.
CHAR_W = 9.7


def asciify(dark_mode):
    im = Image.open(FACE_SRC).convert("RGBA")
    im = im.crop(im.split()[-1].getbbox())  # trim to the subject

    w, h = im.size
    rows = max(1, round((h / w) * COLS / CHAR_ASPECT))

    lum = ImageOps.autocontrast(im.convert("L"), cutoff=1).resize(
        (COLS, rows), Image.LANCZOS
    )
    alpha = im.split()[-1].resize((COLS, rows), Image.LANCZOS)

    lp, ap = lum.load(), alpha.load()
    out = []
    for y in range(rows):
        line = []
        for x in range(COLS):
            if ap[x, y] < ALPHA_CUT:
                line.append(" ")
                continue
            v = lp[x, y]
            t = (v / 255) if dark_mode else (1 - v / 255)
            line.append(RAMP[min(len(RAMP) - 1, int(t * len(RAMP)))])
        out.append("".join(line).rstrip())
    return out


def render(theme):
    face = asciify(theme["dark"])

    # centre the stats block against the taller face column
    stats_h = (len(STATS) + 2) * LH
    face_h = len(face) * LH
    stats_y = TOP_Y + max(0, (face_h - stats_h) // 2)

    # size the canvas to whichever column is taller and to the longest value,
    # so editing STATS can't silently clip
    widest = max(len(v) for _, v in STATS)
    W = round(VALUE_X + widest * CHAR_W) + PAD
    H = TOP_Y + max(face_h, stats_h) + PAD

    p = [
        "<?xml version='1.0' encoding='UTF-8'?>",
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}px" height="{H}px" '
        f'font-size="{FS}px" font-family="ConsolasFallback,Consolas,monospace">',
        "<style>",
        "@font-face {",
        "  src: local('Consolas'), local('Consolas Bold');",
        "  font-family: 'ConsolasFallback';",
        "  font-display: swap;",
        "  -webkit-size-adjust: 109%;",
        "  size-adjust: 109%;",
        "}",
        f'.face {{fill: {theme["face"]};}}',
        f'.prompt {{fill: {theme["prompt"]}; font-weight: bold;}}',
        f'.key {{fill: {theme["key"]}; font-weight: bold;}}',
        f'.value {{fill: {theme["value"]};}}',
        f'.rule {{fill: {theme["rule"]};}}',
        "text, tspan {white-space: pre;}",
        "</style>",
        f'<rect width="{W}px" height="{H}px" fill="{theme["bg"]}" rx="15"/>',
        '<text class="face">',
    ]

    for i, line in enumerate(face):
        p.append(f'<tspan x="{FACE_X}" y="{TOP_Y + i * LH}">{escape(line)}</tspan>')
    p.append("</text>")

    p.append("<text>")
    p.append(
        f'<tspan class="prompt" x="{STATS_X}" y="{stats_y}">{escape(PROMPT)}</tspan>'
    )
    p.append(
        f'<tspan class="rule" x="{STATS_X}" y="{stats_y + LH}">'
        f'{"─" * len(PROMPT)}</tspan>'
    )
    for i, (key, value) in enumerate(STATS):
        y = stats_y + (i + 2) * LH
        p.append(
            f'<tspan class="key" x="{STATS_X}" y="{y}">{escape(key)}</tspan>'
            f'<tspan class="value" x="{VALUE_X}" y="{y}">{escape(value)}</tspan>'
        )
    p.append("</text>")
    p.append("</svg>")
    return "\n".join(p)


def main():
    for filename, theme in THEMES.items():
        path = pathlib.Path(filename)
        path.write_text(render(theme), encoding="utf-8")
        print(f"{path}  {path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
