# Studio Dentaire Belmont — Site démo

Site démo bilingue (FR/EN) pour cabinet dentaire familial à Montréal.
**Site #2 du portfolio Nextiweb.ca** — démontre l'approche "landing one-page" pour secteur santé.

> Cabinet **fictif** créé à des fins de démonstration. Toute ressemblance avec un cabinet existant serait fortuite.

---

## Stack

- HTML5 + CSS pur + JS vanilla
- **Zéro dépendance npm** (parfait pour Hostinger mutualisé)
- Pillow (Python) pour le pipeline d'images uniquement
- Polices : Plus Jakarta Sans + Inter (Google Fonts)

## Structure

```
02-clinique-dentaire-demo/
├── index.html                  # Version FR (defaut)
├── index.en.html               # Version EN
├── sitemap.xml
├── robots.txt
├── favicon.ico
├── css/
│   └── styles.css              # Tous les styles (mobile-first, charte bleu+sauge)
├── js/
│   └── main.js                 # Menu, smooth scroll, FAQ, form, créneaux RDV
├── images/
│   ├── originals/              # PNG IA (gitignored, lourds)
│   └── optimized/              # WebP + JPG générés (servis par <picture>)
└── scripts/
    └── optimize-images.py      # Pipeline images (extraction logo + WebP/JPG)
```

## Pages & sections

Site **one-page** (12 sections + header + footer) :

1. Hero — slogan + CTA RDV + photo cabinet
2. Bandeau confiance (4 chips)
3. Services (6 traitements avec prix indicatifs)
4. Équipe (4 fiches praticiens)
5. Approche (3 piliers : douceur · technologie · transparence)
6. Tarifs & assurances (table transparente)
7. Témoignages (3 avis 5★)
8. FAQ (6 questions)
9. Prise de RDV (formulaire + créneaux visuels CSS)
10. Contact (adresse, horaires, urgences, mini-plan SVG)
11. Footer (4 colonnes + crédit Nextiweb)
12. Badge flottant démo (bottom-left)

## Charte

| Token | Valeur |
|-------|--------|
| Primaire | `#1E5F8E` (bleu pétrole) |
| Secondaire | `#7FB3A4` (vert sauge) |
| Texte | `#1A1A2E` |
| Surface | `#FFFFFF` / `#F4F7FA` |
| Typo display | Plus Jakarta Sans |
| Typo body | Inter |

## Développement

### 1. Pipeline d'images

Mettre les PNG IA dans `images/originals/`, puis :

```bash
python scripts/optimize-images.py
```

Le script :
- Découpe `logo-source.png` (sheet 2-en-1) en `logo-square.png`, `logo-horizontal.png`, `logo-icon.png`
- Génère `apple-touch-icon.png` (512×512) et `favicon.ico` (16/32/48)
- Convertit chaque photo en `.webp` + `.jpg` optimisés
- Génère `og-image.jpg` (1200×630) à partir de `og-source.png`

### 2. Aperçu local

```bash
# Avec Python
python -m http.server 8000

# Avec Node
npx serve .
```

Ouvrir <http://localhost:8000>.

## SEO

- ✅ Schema.org `Dentist` complet (adresse, horaires, langues, spécialités, geo, ratings)
- ✅ Open Graph + Twitter Cards
- ✅ `hreflang` FR/EN/x-default
- ✅ `canonical` par page
- ✅ Sitemap XML avec liens alternatifs
- ✅ robots.txt
- ✅ Meta description optimisée (150-160 char)
- ✅ Width/height explicites sur images (CLS)
- ✅ Preload hero, font-display swap, DNS preconnect

## Accessibilité

- ✅ Skip-link
- ✅ ARIA (labels, expanded, controls, hidden)
- ✅ Focus visible (outline bleu 3px)
- ✅ Contraste AA minimum partout
- ✅ `prefers-reduced-motion` respecté
- ✅ `lang` attribute par version (fr-CA / en-CA)
- ✅ Alt text descriptif sur toutes les images
- ✅ Navigation clavier complète (Tab + Échap pour fermer menu)

## Performance cible

- Lighthouse 95+ sur Performance, A11y, SEO, Best Practices
- LCP < 2.5s
- CLS < 0.1
- Total page weight < 1 Mo (hors hero)

## Déploiement Hostinger

Sous-domaine cible : `clinique-dentaire-demo.nextiweb.ca`

1. Créer le sous-domaine dans hPanel Hostinger
2. Uploader le contenu du dossier (sauf `images/originals/`, `scripts/`, `.git/`) via FTP ou Git
3. Vérifier que `index.html` est servi par défaut

## Crédits

- ✨ **Conçu par [Nextiweb.ca](https://nextiweb.ca)** — agence web montréalaise
- Contenu : démo fictive (cabinet, équipe, témoignages tous fictifs)
- Photos : générées par IA
- Logo : généré par IA, retravaillé via `scripts/optimize-images.py`

---

© 2026 Nextiweb.ca · Site démo (cabinet fictif)
