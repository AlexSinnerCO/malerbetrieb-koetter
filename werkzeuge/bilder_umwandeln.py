# -*- coding: utf-8 -*-
"""Wandelt die Rohbilder aus bilder-roh/ in schnelle WebP-Bilder für die Website um.

Aufruf (im Projektordner):  python werkzeuge/bilder_umwandeln.py
Neue Bilder: in bilder-roh/ legen und unten in ZUORDNUNG eintragen.
"""
import os
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
ROH = os.path.join(HIER, "..", "bilder-roh")
ZIEL = os.path.join(HIER, "..", "website", "assets", "img")

# Rohdatei -> (Zieldatei ohne Endung, maximale Breite)
ZUORDNUNG = {
    "Hausfassade im Sonnenschein streichen.png": ("hero-fassade", 1600),
    "Hausfassade mit Maler auf Gerüst.png": ("galerie-fassade-streichen", 1200),
    "Verwittertes Haus im Vorgarten.png": ("vorher-haus", 1400),
    "Frisch renoviertes weißes Haus mit gepflegtem Garten.png": ("nachher-haus", 1400),
    "Maler renoviert helles Wohnzimmer.png": ("leistung-innen", 1200),
    "Tapeten anbringen in hellem Renovierungsraum.png": ("leistung-tapezieren", 1200),
    "Hochdruckreinigung einer Backsteinfassade.png": ("leistung-fassade", 1200),
    "Bodenverlegung im hellen Raum.png": ("leistung-boden", 1200),
    "Dämmplattenmontage am Haus mit Gerüst.png": ("leistung-daemmung", 1200),
    "Verwittertes niedersächsisches Fachwerkhaus.png": ("referenz-fachwerk-vorher", 1200),
    "Frisch renoviertes Fachwerkhaus im Sonnengarten.png": ("referenz-fachwerk-nachher", 1200),
    "Modernes Treppenhaus mit Grünblick.png": ("referenz-treppenhaus", 1200),
    "Modernes Einfamilienhaus mit Gartenweg.png": ("referenz-einfamilienhaus", 1200),
    "Gemeinsam streichen und lernen.png": ("karriere-ausbildung", 1200),
    "Beschrifteter Mercedes-Transporter vor Backsteingebäude.png": ("firmenwagen", 1200),
    "team-jens.png": ("team-jens", 432),
    "team-sabine.png": ("team-sabine", 432),
    "team-marco.png": ("team-marco", 432),
    "team-timo.png": ("team-timo", 432),
    "team-pawel.png": ("team-pawel", 432),
    "team-lukas.png": ("team-lukas", 432),
}


def webp(src, name, breite, qualitaet=78):
    im = Image.open(src)
    im = im.convert("RGB")
    if im.width > breite:
        im = im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS)
    ziel = os.path.join(ZIEL, name + ".webp")
    im.save(ziel, "WEBP", quality=qualitaet, method=6)
    return ziel, im.size


def klein(im, breite):
    if im.width > breite:
        im = im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS)
    return im


def logos():
    """Logo zuschneiden: komplettes Logo, Schriftzug für die Kopfzeile, Farbrolle als Symbol."""
    src = Image.open(os.path.join(ROH, "koetter-logo-transparent.png")).convert("RGBA")
    voll = src.crop(src.getchannel("A").getbbox())
    voll = klein(voll, 480)
    voll.save(os.path.join(ZIEL, "logo-koetter.png"), optimize=True)
    voll.save(os.path.join(ZIEL, "logo-koetter.webp"), "WEBP", quality=88)
    # Schriftzug "KÖTTER / MALERBETRIEB" ohne Rolle (für die Kopfzeile)
    wort = src.crop((60, 372, 965, 672))
    wort = wort.crop(wort.getchannel("A").getbbox())
    wort = klein(wort, 560)
    wort.save(os.path.join(ZIEL, "logo-schriftzug.webp"), "WEBP", quality=90)
    wort.save(os.path.join(ZIEL, "logo-schriftzug.png"), optimize=True)
    # Komplettes Logo als Tab-Symbol (Favicon) und App-Symbol
    ganz = src.crop(src.getchannel("A").getbbox())
    seite = round(max(ganz.size) * 1.08)
    quadrat = Image.new("RGBA", (seite, seite), (255, 255, 255, 0))
    quadrat.paste(ganz, ((seite - ganz.width) // 2, (seite - ganz.height) // 2), ganz)
    for groesse in (32, 48, 192):
        quadrat.resize((groesse, groesse), Image.LANCZOS).save(os.path.join(ZIEL, f"favicon-{groesse}.png"))
    quadrat.save(os.path.join(ZIEL, "..", "..", "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    weiss = Image.new("RGBA", quadrat.size, (255, 255, 255, 255))
    weiss.alpha_composite(quadrat)
    weiss.convert("RGB").resize((180, 180), Image.LANCZOS).save(os.path.join(ZIEL, "apple-touch-icon.png"))
    # Helle Version für den dunkelblauen Fußbereich: Dunkelblau wird Weiß, Gelb bleibt
    hell = voll.copy()
    px = hell.load()
    for y in range(hell.height):
        for x in range(hell.width):
            r, g, b, a = px[x, y]
            if a and (r + g + b) / 3 < 120:
                px[x, y] = (255, 255, 255, a)
    hell.save(os.path.join(ZIEL, "logo-koetter-hell.webp"), "WEBP", quality=88)


def og_bild():
    """Vorschaubild beim Teilen (1200 x 630)."""
    im = Image.open(os.path.join(ROH, "Hausfassade im Sonnenschein streichen.png")).convert("RGB")
    ziel_v = 1200 / 630
    w, h = im.size
    neu_h = round(w / ziel_v)
    oben = max(0, (h - neu_h) // 2)
    im = im.crop((0, oben, w, oben + neu_h)).resize((1200, 630), Image.LANCZOS)
    im.save(os.path.join(ZIEL, "og-bild.jpg"), "JPEG", quality=82, optimize=True, progressive=True)


if __name__ == "__main__":
    os.makedirs(ZIEL, exist_ok=True)
    gesamt = 0
    for roh, (name, breite) in ZUORDNUNG.items():
        pfad, groesse = webp(os.path.join(ROH, roh), name, breite)
        kb = os.path.getsize(pfad) // 1024
        gesamt += kb
        print(f"{name:32} {groesse[0]}x{groesse[1]:<5} {kb:>4} KB")
    logos()
    og_bild()
    print(f"Fotos zusammen: {gesamt} KB")
