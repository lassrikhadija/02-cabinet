#!/usr/bin/env python3
"""
optimize-images.py
Studio Dentaire Belmont - Pipeline d'images

1. Extrait les variantes logo depuis logo-source.png (sheet 2-en-1)
2. Genere favicon + apple-touch-icon depuis l'icone du logo
3. Convertit toutes les photos PNG -> WebP + JPG optimises
4. Genere l'OG image depuis og-source.png

Usage:
    python scripts/optimize-images.py
"""
from pathlib import Path
from PIL import Image, ImageOps
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "images" / "originals"
OUT = ROOT / "images" / "optimized"
OUT.mkdir(parents=True, exist_ok=True)

# Cibles dimensionnelles (largeur max)
PHOTO_TARGETS = {
    "hero.png":             {"w": 1920, "name": "hero"},
    "dentiste-femme.png":   {"w": 800,  "name": "dentiste-femme"},
    "dentiste-homme.png":   {"w": 800,  "name": "dentiste-homme"},
    "hygieniste.png":       {"w": 800,  "name": "hygieniste"},
    "assistante.png":       {"w": 800,  "name": "assistante"},
    "outil.png":            {"w": 1200, "name": "outil"},
    "scan.png":             {"w": 1200, "name": "scan"},
    "reception.png":        {"w": 1600, "name": "reception"},
    "sourire.png":          {"w": 1200, "name": "sourire"},
    "enfant.png":           {"w": 1200, "name": "enfant"},
}

WEBP_QUALITY = 82
JPG_QUALITY = 85

# Charte refondue : eucalyptus profond (remplace bleu pétrole)
LOGO_TARGET_RGB = (61, 90, 78)  # #3D5A4E


def trim_alpha(img: Image.Image) -> Image.Image:
    """Trim transparent borders to content bbox."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    bbox = img.getbbox()
    return img.crop(bbox) if bbox else img


def recolor_blue_logo(img: Image.Image, target_rgb: tuple) -> Image.Image:
    """Le logo source a un fond damier gris BAKED (pas vraiment transparent).
    On detecte les pixels bleus (logo) -> recoloriser en target_rgb,
    le reste -> vraiment transparent. Anti-aliasing preserve via alpha proportionnelle."""
    arr = np.array(img.convert("RGBA"))
    r = arr[:, :, 0].astype(np.int16)
    g = arr[:, :, 1].astype(np.int16)
    b = arr[:, :, 2].astype(np.int16)

    # Mask : pixels où le bleu domine clairement (logo bleu canard)
    is_blue = (b > r + 25) & (b > g + 5) & (r < 220)

    # Alpha proportionnelle a la saturation : pixels bleu profond = opaques,
    # pixels bleu clair (anti-aliasing) = partiellement transparents
    alpha = np.clip((255 - r) * 1.4, 0, 255).astype(np.uint8)
    alpha = np.where(is_blue, alpha, 0).astype(np.uint8)

    out = np.zeros_like(arr)
    out[..., 0] = target_rgb[0]
    out[..., 1] = target_rgb[1]
    out[..., 2] = target_rgb[2]
    out[..., 3] = alpha
    return Image.fromarray(out, mode="RGBA")


def extract_logo_variants():
    """logo-source.png contient 2 variantes cote a cote (carree | horizontale)
    avec labels en bas. On decoupe en 50/50, on retire le bas (labels), on trim."""
    src = SRC / "logo-source.png"
    if not src.exists():
        print(f"[!] Manquant: {src}")
        return

    img = Image.open(src).convert("RGBA")
    # Recolor : detection bleu -> eucalyptus, reste -> transparent
    img = recolor_blue_logo(img, LOGO_TARGET_RGB)
    W, H = img.size
    print(f"[logo] Source: {W}x{H} (bleu -> eucalyptus #3D5A4E + fond transparent)")

    # On enleve le bas 14% (labels "Variation Carree" / "Variation Horizontale")
    label_cutoff = int(H * 0.86)

    # Variante carree = moitie gauche (icone au-dessus du texte STUDIO DENTAIRE BELMONT)
    square = img.crop((0, 0, W // 2, label_cutoff))
    square = trim_alpha(square)
    square.save(OUT / "logo-square.png", optimize=True)
    print(f"[logo] -> logo-square.png ({square.size[0]}x{square.size[1]})")

    # Variante horizontale = moitie droite (icone a gauche du texte)
    horiz = img.crop((W // 2, 0, W, label_cutoff))
    horiz = trim_alpha(horiz)
    horiz.save(OUT / "logo-horizontal.png", optimize=True)
    print(f"[logo] -> logo-horizontal.png ({horiz.size[0]}x{horiz.size[1]})")

    # Icone seule : moitie haute de la variante carree (la dent au-dessus du texte)
    sw, sh = square.size
    icon = square.crop((0, 0, sw, int(sh * 0.62)))
    icon = trim_alpha(icon)
    # Pad to square pour favicon
    iw, ih = icon.size
    side = max(iw, ih)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(icon, ((side - iw) // 2, (side - ih) // 2), icon)
    canvas.save(OUT / "logo-icon.png", optimize=True)
    print(f"[logo] -> logo-icon.png ({side}x{side})")

    # Favicon multi-tailles + apple-touch
    icon_512 = canvas.resize((512, 512), Image.LANCZOS)
    icon_512.save(OUT / "apple-touch-icon.png", optimize=True)
    print(f"[logo] -> apple-touch-icon.png (512x512)")

    # favicon.ico (16, 32, 48)
    favicon_path = ROOT / "favicon.ico"
    canvas.save(favicon_path, sizes=[(16, 16), (32, 32), (48, 48)])
    print(f"[logo] -> favicon.ico")


def optimize_photo(filename: str, target_w: int, out_name: str):
    src = SRC / filename
    if not src.exists():
        print(f"[!] Manquant: {src}")
        return

    img = Image.open(src)
    img = ImageOps.exif_transpose(img)

    # Resize si trop large
    w, h = img.size
    if w > target_w:
        new_h = int(h * target_w / w)
        img = img.resize((target_w, new_h), Image.LANCZOS)
        w, h = img.size

    # JPG (background blanc pour les PNG avec alpha)
    rgb = Image.new("RGB", (w, h), (255, 255, 255))
    if img.mode in ("RGBA", "LA"):
        rgb.paste(img, mask=img.split()[-1])
    else:
        rgb.paste(img.convert("RGB"))
    rgb.save(OUT / f"{out_name}.jpg", "JPEG", quality=JPG_QUALITY, optimize=True, progressive=True)

    # WebP (preserve alpha si present)
    img.save(OUT / f"{out_name}.webp", "WEBP", quality=WEBP_QUALITY, method=6)

    sz_jpg = (OUT / f"{out_name}.jpg").stat().st_size // 1024
    sz_webp = (OUT / f"{out_name}.webp").stat().st_size // 1024
    print(f"[photo] {out_name}: {w}x{h} | webp={sz_webp}ko jpg={sz_jpg}ko")


def make_og_image():
    """og-source.png est deja un visuel cible (B-monogramme + tagline + fond bleu).
    On le redimensionne a 1200x630 pour Open Graph / Twitter."""
    src = SRC / "og-source.png"
    if not src.exists():
        print(f"[!] Manquant: {src}")
        return

    img = Image.open(src)
    img = ImageOps.exif_transpose(img)

    # Fit en 1200x630, fond bleu nuit si ratio different
    target = (1200, 630)
    img.thumbnail((target[0] * 2, target[1] * 2), Image.LANCZOS)
    canvas = Image.new("RGB", target, (15, 47, 70))  # bleu nuit
    iw, ih = img.size
    # Cover : redim pour remplir, crop centre
    ratio = max(target[0] / iw, target[1] / ih)
    nw, nh = int(iw * ratio), int(ih * ratio)
    img = img.resize((nw, nh), Image.LANCZOS).convert("RGB")
    cx, cy = (nw - target[0]) // 2, (nh - target[1]) // 2
    img = img.crop((cx, cy, cx + target[0], cy + target[1]))

    img.save(OUT / "og-image.jpg", "JPEG", quality=88, optimize=True, progressive=True)
    print(f"[og] -> og-image.jpg (1200x630)")


def main():
    print("=== Studio Dentaire Belmont - optimisation images ===\n")
    extract_logo_variants()
    print()
    for fname, conf in PHOTO_TARGETS.items():
        optimize_photo(fname, conf["w"], conf["name"])
    print()
    make_og_image()
    print("\n[OK] Sortie -> images/optimized/")


if __name__ == "__main__":
    main()
