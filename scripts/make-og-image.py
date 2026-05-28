# -*- coding: utf-8 -*-
"""Génère og-image.jpg (1200x630) dans la palette Clinical Premium 2026."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

S = 2  # supersampling
W, H = 1200 * S, 630 * S

# Palette
NAVY   = (15, 42, 63)     # #0F2A3F
NAVY_D = (9, 22, 36)      # #061320
MINT   = (127, 209, 185)  # #7FD1B9
GOLD   = (201, 168, 118)  # #C9A876
WHITE  = (250, 250, 247)  # #FAFAF7

# --- Fond dégradé vertical navy ---
img = Image.new("RGB", (W, H), NAVY)
top = Image.new("RGB", (W, H), NAVY)
px = top.load()
for y in range(H):
    t = y / H
    r = int(NAVY[0] + (NAVY_D[0] - NAVY[0]) * t)
    g = int(NAVY[1] + (NAVY_D[1] - NAVY[1]) * t)
    b = int(NAVY[2] + (NAVY_D[2] - NAVY[2]) * t)
    for x in range(0, W, 1):
        px[x, y] = (r, g, b)
img = top

# --- Glows (menthe haut-droite, or bas-gauche) ---
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([W*0.55, -H*0.35, W*1.25, H*0.55], fill=MINT + (70,))
gd.ellipse([-W*0.30, H*0.55, W*0.45, H*1.35], fill=GOLD + (55,))
glow = glow.filter(ImageFilter.GaussianBlur(180 * S // 2))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")

d = ImageDraw.Draw(img)

# --- Emblème : cercle + dent stylisée menthe ---
cx, cy, rad = W // 2, int(H * 0.30), 92 * S
d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=MINT, width=4 * S)
# dent (deux bosses + base) en menthe
tw = 54 * S
d.pieslice([cx - tw, cy - tw, cx, cy], 180, 360, fill=MINT)
d.pieslice([cx, cy - tw, cx + tw, cy], 180, 360, fill=MINT)
d.polygon([(cx - tw, cy - tw//2), (cx + tw, cy - tw//2),
           (cx + tw*0.55, cy + tw), (cx + tw*0.18, cy + tw*0.35),
           (cx - tw*0.18, cy + tw), (cx - tw*0.55, cy + tw*0.35)], fill=MINT)
# petit sourire or
d.arc([cx - 26*S, cy - 8*S, cx + 26*S, cy + 30*S], 20, 160, fill=GOLD, width=5*S)

# --- Polices ---
def font(path, size):
    return ImageFont.truetype(path, size * S)
f_title = font("C:/Windows/Fonts/georgiab.ttf", 76)
f_sub   = font("C:/Windows/Fonts/arial.ttf", 33)
f_small = font("C:/Windows/Fonts/arialbd.ttf", 22)

def center_text(y, text, fnt, fill, spacing=0):
    bbox = d.textbbox((0, 0), text, font=fnt)
    w = bbox[2] - bbox[0]
    d.text(((W - w) // 2, y), text, font=fnt, fill=fill)
    return bbox[3] - bbox[1]

# --- Titre ---
center_text(int(H * 0.52), "Studio Dentaire Belmont", f_title, WHITE)

# --- Ligne or ---
ly = int(H * 0.68)
d.line([(W//2 - 60*S, ly), (W//2 + 60*S, ly)], fill=GOLD, width=3*S)

# --- Sous-titre ---
center_text(int(H * 0.71), "Cabinet dentaire familial  ·  Montreal", f_sub, MINT)

# --- Chip bas : badge (texte menthe bien lisible) ---
chip = "BILINGUE FR / EN      ·      CONFORME LOI 25      ·      URGENCES 24/7"
bbox = d.textbbox((0, 0), chip, font=f_small)
cw = bbox[2] - bbox[0]
ch = bbox[3] - bbox[1]
cy2 = int(H * 0.85)
pad_x, pad_y = 34 * S, 18 * S
box = [(W - cw)//2 - pad_x, cy2 - pad_y, (W + cw)//2 + pad_x, cy2 + ch + pad_y]
# panneau semi-opaque via composite
panel = Image.new("RGBA", img.size, (0, 0, 0, 0))
pdr = ImageDraw.Draw(panel)
pdr.rounded_rectangle(box, radius=34*S, fill=(255, 255, 255, 28), outline=GOLD + (255,), width=2*S)
img = Image.alpha_composite(img.convert("RGBA"), panel).convert("RGB")
d = ImageDraw.Draw(img)
d.text(((W - cw)//2, cy2), chip, font=f_small, fill=MINT)

# --- Downscale + save ---
final = img.resize((1200, 630), Image.LANCZOS)
final.save("images/optimized/og-image.jpg", "JPEG", quality=88, optimize=True)
print("OK -> images/optimized/og-image.jpg", final.size)
