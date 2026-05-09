#!/usr/bin/env python3
"""
download-photos.py
Telecharge 10 photos Pexels (libres de droits, usage commercial OK,
sans attribution requise) pour remplacer les photos IA Gemini.

Usage:
    python scripts/download-photos.py
"""
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
DST = ROOT / "images" / "originals"
DST.mkdir(parents=True, exist_ok=True)

# Pexels CDN, taille xl pour qualite max apres redim
SUFFIX = "?auto=compress&cs=tinysrgb&w=2400"

PHOTOS = {
    # Hero : interieur paysage, lumiere naturelle, sans personne (was portrait, switched to landscape)
    "hero.jpg":              "https://images.pexels.com/photos/305567/pexels-photo-305567.jpeg",
    # Equipe : 4 personnes distinctes, pas de branding visible (was Dentify-branded)
    "dentiste-femme.jpg":    "https://images.pexels.com/photos/32254667/pexels-photo-32254667.jpeg",
    "dentiste-homme.jpg":    "https://images.pexels.com/photos/32254662/pexels-photo-32254662.jpeg",
    "hygieniste.jpg":        "https://images.pexels.com/photos/18828738/pexels-photo-18828738.jpeg",
    "assistante.jpg":        "https://images.pexels.com/photos/19131221/pexels-photo-19131221.jpeg",
    "outil.jpg":             "https://images.pexels.com/photos/6502661/pexels-photo-6502661.jpeg",
    "scan.jpg":              "https://images.pexels.com/photos/6627668/pexels-photo-6627668.jpeg",
    "reception.jpg":         "https://images.pexels.com/photos/4687346/pexels-photo-4687346.jpeg",
    "sourire.jpg":           "https://images.pexels.com/photos/3762453/pexels-photo-3762453.jpeg",
    "enfant.jpg":            "https://images.pexels.com/photos/8260438/pexels-photo-8260438.jpeg",
}


def main():
    print("=== Telechargement photos Pexels (libres de droits) ===\n")
    # Supprime les anciennes photos IA (PNG)
    for old in DST.glob("*.png"):
        if old.name not in ("logo-source.png", "og-source.png"):
            old.unlink()
            print(f"[del] {old.name}")
    print()
    headers = {"User-Agent": "Mozilla/5.0 Nextiweb-portfolio"}
    for name, url in PHOTOS.items():
        full_url = url + SUFFIX
        out = DST / name
        try:
            req = urllib.request.Request(full_url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            out.write_bytes(data)
            print(f"[ok]  {name}: {len(data)//1024} ko")
        except Exception as e:
            print(f"[ERR] {name}: {e}")
    print(f"\n[OK] Sortie -> {DST}")


if __name__ == "__main__":
    main()
