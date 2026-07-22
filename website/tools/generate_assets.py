#!/usr/bin/env python3
"""Generate PhotoPots website raster assets: app icon copies, maskable icon,
apple-touch-icon, and the 1200x630 Open Graph image."""
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path("/Users/tavisroberts/Developer/PhotoPots/PhotoPots")
SRC_ICON = ROOT / "PhotoPots/Assets.xcassets/AppIcon.appiconset/icon_512.png"
OUT = ROOT / "website/assets/img"
OUT.mkdir(parents=True, exist_ok=True)

CREAM = (250, 247, 242)
INK = (35, 38, 46)
INK_SOFT = (74, 79, 90)

FONT_ROUNDED = "/System/Library/Fonts/SFNSRounded.ttf"
FONT_BODY = "/Users/tavisroberts/Library/Application Support/kimi-desktop/daimon-share/daimon/runtime/python/fonts/NotoSansSC-Regular.ttf"

# ---------------------------------------------------------------- 1. copies
icon = Image.open(SRC_ICON).convert("RGBA")
corner = icon.getpixel((2, 2))[:3]
print("icon corner color:", corner)

shutil.copyfile(SRC_ICON, OUT / "app-icon-512.png")

def on_field(size, scale, bg):
    """Icon centered on a solid field of its own corner color."""
    canvas = Image.new("RGB", (size, size), bg)
    inner = int(size * scale)
    canvas.paste(icon.resize((inner, inner), Image.LANCZOS),
                 ((size - inner) // 2, (size - inner) // 2))
    return canvas

# Maskable: OS masks to circle/squircle -> keep icon inside ~72% safe zone
on_field(512, 0.72, corner).save(OUT / "app-icon-maskable-512.png")
# Apple touch icon
on_field(180, 0.86, corner).save(OUT / "apple-touch-icon.png")
# PNG favicon fallback
on_field(32, 0.92, corner).save(OUT / "favicon-32.png")
print("icon derivatives written")

# ---------------------------------------------------------------- helpers
def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def rounded_gradient(size, radius, top, bottom):
    """Vertical gradient clipped to a rounded rectangle."""
    grad = Image.new("RGB", size)
    px = grad.load()
    w, h = size
    for y in range(h):
        row = lerp(top, bottom, y / max(h - 1, 1))
        for x in range(w):
            px[x, y] = row
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    out.paste(grad, (0, 0), mask)
    return out

def glow_layer(canvas_size, box, radius, color, blur=16, alpha=115, dy=8):
    """Soft colored glow under a tile (app recipe: 45% alpha, blur 14, y 6)."""
    layer = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0, y0 + dy, x1, y1 + dy], radius=radius,
                        fill=color + (alpha,))
    return layer.filter(ImageFilter.GaussianBlur(blur))

# ---------------------------------------------------------------- og image
W, H = 1200, 630
og = Image.new("RGB", (W, H), CREAM).convert("RGBA")

# Right side: 2x2 pastel pot tiles with colored glows
TILES = [
    ("Work",     (220, 240, 250), (186, 225, 246), (28, 157, 224)),   # blue
    ("Family",   (251, 237, 221), (248, 219, 187), (234, 138, 30)),   # orange
    ("Projects", (223, 248, 250), (191, 242, 246), (44, 211, 225)),   # cyan
    ("Personal", (221, 240, 234), (187, 226, 214), (29, 158, 117)),   # green
]
tile, gap = 196, 26
grid_x, grid_y = W - 96 - (tile * 2 + gap), (H - (tile * 2 + gap)) // 2
name_font = ImageFont.truetype(FONT_ROUNDED, 30)
meta_font = ImageFont.truetype(FONT_BODY, 19)

for i, (name, tint_a, tint_b, accent) in enumerate(TILES):
    col, row = i % 2, i // 2
    x = grid_x + col * (tile + gap)
    y = grid_y + row * (tile + gap)
    og.alpha_composite(glow_layer((W, H), (x, y, x + tile, y + tile), 30, accent))
    og.alpha_composite(rounded_gradient((tile, tile), 30, tint_a, tint_b), (x, y))
    d = ImageDraw.Draw(og)
    d.text((x + 22, y + tile - 78), name, font=name_font, fill=INK)
    d.text((x + 22, y + tile - 40), "128 photos", font=meta_font, fill=INK_SOFT)

# Left: logo + wordmark + tagline
logo = icon.resize((168, 168), Image.LANCZOS)
logo_x, logo_y = 96, 196
# round the app icon like iOS does (~22.4% radius)
mask = Image.new("L", (168, 168), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, 167, 167], radius=38, fill=255)
og.paste(logo, (logo_x, logo_y), mask)

d = ImageDraw.Draw(og)
title_font = ImageFont.truetype(FONT_ROUNDED, 78)
tag_font = ImageFont.truetype(FONT_ROUNDED, 33)
d.text((292, 210), "PhotoPots", font=title_font, fill=INK)
d.text((294, 312), "Keep work and life photos apart.", font=tag_font, fill=INK_SOFT)

# Small pot-color dots as an accent underline
dot_y = 392
for i, c in enumerate([(44, 211, 225), (28, 157, 224), (234, 138, 30), (216, 69, 62)]):
    x = 296 + i * 34
    d.ellipse([x, dot_y, x + 16, dot_y + 16], fill=c)

og.convert("RGB").save(OUT / "og-image.png", optimize=True)
print("og-image.png written")
