# -*- coding: utf-8 -*-
"""Erzeugt alle HTML-Seiten der Website Malerbetrieb Kötter in website/.

Aufruf (im Projektordner):  python werkzeuge/seiten_bauen.py

Kopf, Menü und Fußbereich stehen hier nur einmal und landen auf allen Seiten.
Texte ändern: unten bei der jeweiligen Seite. Danach das Skript neu starten.
Die fertigen HTML-Dateien in website/ sind das, was hochgeladen wird.
"""
import json
import os

HIER = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(HIER, "..", "website")
DOMAIN = "https://www.malerbetrieb-koetter.de"

TEL_ANZEIGE = "05462 00000"
TEL_LINK = "tel:+49546200000"
WA_ANZEIGE = "0170 0000000"
WA_LINK = "https://wa.me/491700000000"
MAIL = "info@malerbetrieb-koetter.de"
ROUTE = "https://www.google.com/maps/dir/?api=1&destination=Hauptstra%C3%9Fe+41%2C+49577+Ankum"
BEWERTUNGEN = "https://www.google.com/maps/search/?api=1&query=Malerbetrieb+K%C3%B6tter+Ankum"
OSM = "https://www.openstreetmap.org/export/embed.html?bbox=7.8530%2C52.5380%2C7.8890%2C52.5500&layer=mapnik&marker=52.5440%2C7.8710"

# ------------------------------------------------------------------ Symbole
_ICONS = {
    "telefon": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>',
    "ort": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "uhr": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "haken": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4L12 14.01l-3-3"/>',
    "menue": '<path d="M3 6h18M3 12h18M3 18h18"/>',
    "pfeile": '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5"/>',
    "meister": '<circle cx="12" cy="8" r="6"/><path d="M15.48 12.89L17 22l-5-3-5 3 1.52-9.11"/>',
    "haus": '<path d="M3 10.5L12 3l9 7.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    "team": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "kalender": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "euro": '<path d="M18 7a7 7 0 1 0 0 10M4 10h10M4 14h10"/>',
    "werkzeug": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "sonne": '<circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>',
    "geruest": '<path d="M6 2v20M18 2v20M6 6h12M6 11h12M6 16h12M6 6l12 5"/>',
    "route": '<path d="M3 11l19-9-9 19-2-8-8-2z"/>',
    "stern": '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>',
    "whatsapp": '<path d="M3 21l1.65-4.95A9 9 0 1 1 8 19.4L3 21z"/><path d="M9.2 8.6c.2-.5.6-.6 1-.6.3 0 .5.4.8 1.1.2.5.1.7-.1 1l-.4.5c.5 1 1.3 1.8 2.3 2.3l.5-.4c.3-.2.5-.3 1-.1.7.3 1.1.5 1.1.8 0 .4-.1.8-.6 1-.8.4-1.8.4-3-.2a8 8 0 0 1-3-3c-.6-1.2-.6-2.2.4-2.4z" fill="currentColor" stroke="none"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_ICONS[name]}</svg>')


def bild(datei, alt, breite, hoehe, cls="", lazy=True, prio=False):
    attr = ' loading="lazy" decoding="async"' if lazy else ""
    if prio:
        attr += ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="/assets/img/{datei}" alt="{alt}" width="{breite}" height="{hoehe}"{c}{attr}>'


# ------------------------------------------------------------------ Bausteine
MENUE = [("/", "Start"), ("/leistungen", "Leistungen"), ("/ueber-uns", "Über uns"),
         ("/referenzen", "Referenzen"), ("/karriere", "Karriere"), ("/kontakt", "Kontakt")]


def kopf(aktiv):
    punkte = ""
    for href, text in MENUE:
        aktuell = ' aria-current="page"' if href == aktiv else ""
        punkte += f'<li><a href="{href}"{aktuell}>{text}</a></li>'
    return f'''<a class="springen" href="#inhalt">Zum Inhalt springen</a>
<header class="kopf">
  <div class="container kopf__innen">
    <a class="kopf__logo" href="/" aria-label="Malerbetrieb Kötter, zur Startseite">
      <img src="/assets/img/logo-kopf.webp" alt="Kötter Malerbetrieb" width="900" height="202">
    </a>
    <button class="menue-knopf" type="button" aria-expanded="false" aria-controls="hauptmenue" aria-label="Menü öffnen">{icon("menue")}</button>
    <nav class="nav" id="hauptmenue" aria-label="Hauptmenü">
      <ul>{punkte}<li><a class="knopf knopf--gelb kopf__anruf" href="{TEL_LINK}">{icon("telefon")}{TEL_ANZEIGE}</a></li></ul>
    </nav>
  </div>
</header>'''


FUSS = f'''<footer class="fuss">
  <div class="container fuss__raster">
    <div>
      <img class="fuss__logo" src="/assets/img/logo-koetter-hell.webp" alt="Kötter Malerbetrieb" width="480" height="506" loading="lazy">
      <p>Meisterbetrieb in zweiter Generation seit 1987. Für Ankum, Bersenbrück, Quakenbrück und die ganze Region.</p>
    </div>
    <div>
      <h2>Kontakt</h2>
      <address>
        Malerbetrieb Kötter<br>Inhaber Jens Kötter<br>Hauptstraße 41<br>49577 Ankum
      </address>
      <ul style="margin-top:12px">
        <li><a href="{TEL_LINK}">{TEL_ANZEIGE}</a></li>
        <li><a href="mailto:{MAIL}">{MAIL}</a></li>
      </ul>
    </div>
    <div>
      <h2>Erreichbar</h2>
      <p style="margin:0">Büro: Mo bis Fr, 8 bis 12 Uhr<br>WhatsApp: meist abends bis 20 Uhr<br>Samstag und Sonntag geschlossen</p>
    </div>
    <div>
      <h2>Seiten</h2>
      <ul>
        <li><a href="/leistungen">Leistungen</a></li>
        <li><a href="/ueber-uns">Über uns</a></li>
        <li><a href="/referenzen">Referenzen</a></li>
        <li><a href="/karriere">Karriere</a></li>
        <li><a href="/kontakt">Kontakt</a></li>
      </ul>
    </div>
  </div>
  <div class="container fuss__unten">
    <span>© <span id="jahr">2027</span> Malerbetrieb Kötter</span>
    <ul>
      <li><a href="/impressum">Impressum</a></li>
      <li><a href="/datenschutz">Datenschutz</a></li>
      <li>Webdesign: Sinner Webdesign</li>
    </ul>
  </div>
</footer>
<a class="wa-knopf" href="{WA_LINK}" target="_blank" rel="noopener">
  {icon("whatsapp")}
  <span class="wa-knopf__text">WhatsApp<small>Antwort meist abends bis 20 Uhr</small></span>
  <span class="sr-only"> (öffnet WhatsApp)</span>
</a>
<script src="/assets/js/main.js" defer></script>'''


def seite(datei, pfad, titel, beschreibung, inhalt, extra_head=""):
    url = DOMAIN + pfad
    html = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titel}</title>
<meta name="description" content="{beschreibung}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="Malerbetrieb Kötter">
<meta property="og:title" content="{titel}">
<meta property="og:description" content="{beschreibung}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/assets/img/og-bild.jpg">
<meta name="theme-color" content="#1d2f4f">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/img/favicon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/css/style.css">
{extra_head}
</head>
<body>
{kopf(pfad)}
<main id="inhalt">
{inhalt}
</main>
{FUSS}
</body>
</html>
'''
    with open(os.path.join(ZIEL, datei), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


def knoepfe_kontakt(hell=False, anfrage_text="Anfrage senden"):
    rand = "knopf--hell" if hell else "knopf--rand"
    return (f'<div class="knoepfe">'
            f'<a class="knopf knopf--gelb" href="{TEL_LINK}">{icon("telefon")}{TEL_ANZEIGE} anrufen</a>'
            f'<a class="knopf knopf--wa" href="{WA_LINK}" target="_blank" rel="noopener">{icon("whatsapp")}Per WhatsApp schreiben</a>'
            f'<a class="knopf {rand}" href="/kontakt#formular">{anfrage_text}</a></div>')


def aufruf_band(titel, text, anfrage_text="Anfrage senden"):
    return f'''<section class="abschnitt abschnitt--blau">
  <div class="container aufruf">
    <div><h2>{titel}</h2><p class="einleitung" style="margin:0">{text}</p></div>
    {knoepfe_kontakt(hell=True, anfrage_text=anfrage_text)}
  </div>
</section>'''


def vorher_nachher(vorher, nachher, alt_vorher, alt_nachher):
    return f'''<div class="vn">
  {bild(vorher, alt_vorher, 1400, 933)}
  {bild(nachher, alt_nachher, 1400, 933, cls="vn__nachher")}
  <span class="vn__etikett vn__etikett--vorher">Vorher</span>
  <span class="vn__etikett vn__etikett--nachher">Nachher</span>
  <span class="vn__linie"></span>
  <input class="vn__regler" type="range" min="0" max="100" value="50" aria-label="Vorher-nachher-Vergleich: Regler verschieben">
  <span class="vn__griff">{icon("pfeile")}</span>
</div>'''


STIMMEN = f'''<div class="stimmen">
  <figure class="stimme"><blockquote>„Pünktlich, sauber und unser Wohnzimmer sieht aus wie neu. Gerne wieder!“</blockquote><figcaption>Familie M. aus Bersenbrück</figcaption></figure>
  <figure class="stimme"><blockquote>„Seit Jahren unser fester Partner für die Treppenhäuser. Termine werden immer eingehalten.“</blockquote><figcaption>Hausverwaltung aus Quakenbrück</figcaption></figure>
</div>
<div class="sterne"><span class="sterne__symbole" aria-hidden="true">★★★★★</span><span>4,8 von 5 Sternen bei Google</span>
<a href="{BEWERTUNGEN}" target="_blank" rel="noopener">Alle Bewertungen bei Google lesen</a></div>'''


# ------------------------------------------------------------------ Startseite
def startseite():
    schema = {
        "@context": "https://schema.org", "@type": "HousePainter",
        "name": "Malerbetrieb Kötter", "founder": "Heinz Kötter", "foundingDate": "1987",
        "url": DOMAIN + "/", "logo": DOMAIN + "/assets/img/logo-koetter.png", "image": DOMAIN + "/assets/img/og-bild.jpg",
        "telephone": "+49 5462 00000", "email": MAIL,
        "address": {"@type": "PostalAddress", "streetAddress": "Hauptstraße 41", "postalCode": "49577",
                    "addressLocality": "Ankum", "addressCountry": "DE"},
        "areaServed": ["Ankum", "Bersenbrück", "Quakenbrück", "Fürstenau", "Bramsche", "Alfhausen", "Osnabrück"],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                       "opens": "08:00", "closes": "12:00"}],
    }
    head = '<link rel="preload" as="image" href="/assets/img/hero-fassade.webp">\n' \
           f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'
    kacheln = ""
    for anker, img, titel, text in [
        ("innen", "leistung-innen.webp", "Innenarbeiten", "Wände und Decken streichen, Türen und Heizkörper lackieren, Wände glatt spachteln."),
        ("tapezieren", "leistung-tapezieren.webp", "Tapezieren", "Von Raufaser bis Mustertapete. Alte Tapeten entfernen wir gleich mit."),
        ("fassade", "leistung-fassade.webp", "Fassade", "Reinigen, Risse ausbessern, streichen, Klinker reinigen und imprägnieren."),
        ("boden", "leistung-boden.webp", "Böden", "Vinyl, Designboden, Laminat und Teppich."),
        ("daemmung", "leistung-daemmung.webp", "Wärmedämmung", "Dämmung der Fassade mit Wärmedämmverbundsystem (WDVS)."),
    ]:
        kacheln += (f'<a class="kachel" href="/leistungen#{anker}">{bild(img, titel, 1200, 900)}'
                    f'<div class="kachel__text"><h3>{titel}</h3><p>{text}</p></div></a>')
    kacheln += (f'<a class="kachel kachel--aufruf" href="/kontakt#formular"><div class="kachel__text">'
                f'<h3>Kostenlose Besichtigung</h3><p>Wir kommen vorbei, sehen uns alles an und machen Ihnen ein Angebot.</p>'
                f'<span class="knopf knopf--gelb">Termin anfragen</span></div></a>')
    orte = "".join(f"<li>{o}</li>" for o in ["Ankum", "Bersenbrück", "Quakenbrück", "Fürstenau", "Bramsche", "Alfhausen", "und die Orte dazwischen"])
    inhalt = f'''<section class="hero">
  {bild("hero-fassade.webp", "Maler von Kötter streicht auf dem eigenen Gerüst eine Hausfassade", 1600, 900, cls="hero__bild", lazy=False, prio=True)}
  <div class="container">
    <div class="hero__inhalt">
      <span class="dachzeile">Meisterbetrieb in Ankum</span>
      <h1>Seit 1987 der Malerbetrieb <span class="strich">Ihres Vertrauens</span> in Ankum</h1>
      <p>Wir streichen, tapezieren, verlegen Böden und machen Fassaden wieder schön. Mit eigenem Team, eigenem Gerüst und Terminen, auf die Sie sich verlassen können.</p>
      <div class="knoepfe">
        <a class="knopf knopf--gelb" href="{TEL_LINK}">{icon("telefon")}Jetzt anrufen</a>
        <a class="knopf knopf--hell" href="{WA_LINK}" target="_blank" rel="noopener">{icon("whatsapp")}Per WhatsApp schreiben</a>
      </div>
    </div>
  </div>
</section>
<div class="vertrauen">
  <ul class="container">
    <li>{icon("meister")}Meisterbetrieb seit 1987</li>
    <li>{icon("geruest")}Eigenes Gerüst</li>
    <li>{icon("team")}Nur eigene Mitarbeiter</li>
    <li>{icon("stern")}4,8 Sterne bei Google</li>
    <li>{icon("haus")}Kostenlose Besichtigung vor Ort</li>
  </ul>
</div>

<section class="abschnitt">
  <div class="container zweispaltig">
    <div>
      <p class="leitsatz">Wenn wir Montag sagen, kommen wir Montag.</p>
      <p>Das ist kein Werbespruch, sondern unser Anspruch an jeden Auftrag. Sie bekommen einen festen Termin, und der gilt. Unsere Leute kennen Sie, weil es immer dieselben sind: Wir arbeiten ausschließlich mit eigenen Mitarbeitern.</p>
      <p>Weil wir ein eigenes Gerüst haben, warten wir bei Fassadenarbeiten auf niemanden. Das spart Ihnen Zeit und uns Abstimmung.</p>
      <a class="knopf knopf--rand" href="/ueber-uns">Lernen Sie uns kennen</a>
    </div>
    {bild("firmenwagen.webp", "Firmenwagen des Malerbetriebs Kötter mit Leitern auf dem Dach", 1200, 800, cls="bild-rund")}
  </div>
</section>

<section class="abschnitt abschnitt--grau">
  <div class="container">
    <div class="kopf-abschnitt">
      <span class="dachzeile">Leistungen</span>
      <h2>Was wir für Sie machen</h2>
      <p class="einleitung">Vom einzelnen Zimmer bis zur kompletten Fassade, alles aus einer Hand.</p>
    </div>
    <div class="kacheln">{kacheln}</div>
    <div class="mehr-link"><a class="knopf knopf--blau" href="/leistungen">Alle Leistungen ansehen</a></div>
  </div>
</section>

<section class="abschnitt">
  <div class="container zweispaltig zweispaltig--umgekehrt">
    <div>
      <span class="dachzeile">Vorher und nachher</span>
      <h2>Aus grau wird wie neu</h2>
      <p>Am meisten Freude macht uns eine Fassade, die vorher grau und fleckig war und hinterher wie neu dasteht. Ziehen Sie den Regler und sehen Sie selbst, was aus alten Häusern werden kann.</p>
      <a class="knopf knopf--rand" href="/referenzen">Zu unseren Referenzen</a>
    </div>
    {vorher_nachher("vorher-haus.webp", "nachher-haus.webp", "Einfamilienhaus vorher: graue, fleckige Fassade mit Rissen", "Dasselbe Haus nachher: frisch gestrichene weiße Fassade mit anthrazitfarbenem Sockel")}
  </div>
</section>

<section class="abschnitt abschnitt--grau">
  <div class="container">
    <div class="kopf-abschnitt"><span class="dachzeile">Kundenstimmen</span><h2>Das sagen unsere Kunden</h2></div>
    {STIMMEN}
  </div>
</section>

<section class="abschnitt">
  <div class="container">
    <div class="kopf-abschnitt" style="margin-bottom:0">
      <span class="dachzeile">Region</span>
      <h2>Für Sie da in der Region</h2>
      <p>Wir arbeiten in rund 30 Kilometern um Ankum. Für größere Aufträge kommen wir auch nach Osnabrück.</p>
      <ul class="orte">{orte}</ul>
    </div>
  </div>
</section>

{aufruf_band("Lassen Sie uns über Ihr Vorhaben sprechen", "Rufen Sie uns an oder schreiben Sie uns kurz, was Sie vorhaben. Wir kommen kostenlos bei Ihnen vorbei, sehen uns alles an und machen Ihnen ein Angebot.")}'''
    seite("index.html", "/", "Malerbetrieb Kötter in Ankum | Maler, Fassade, Tapezieren, Boden",
          "Meisterbetrieb in zweiter Generation seit 1987. Innenarbeiten, Fassaden, Böden und Wärmedämmung in Ankum, Bersenbrück, Quakenbrück und Umgebung. Kostenlose Besichtigung vor Ort.",
          inhalt, head)


# ------------------------------------------------------------------ Leistungen
def leistungen():
    def liste(punkte):
        return '<ul class="liste-haken">' + "".join(f"<li>{p}</li>" for p in punkte) + "</ul>"

    bloecke = [
        ("innen", "leistung-innen.webp", "Maler rollt eine Wand im abgedeckten Wohnzimmer", "Innenarbeiten",
         "<p>Frische Farbe verändert einen Raum mehr als jede neue Einrichtung. Wir streichen Wände und Decken, lackieren Türen, Heizkörper und Fensterrahmen und decken vorher alles sorgfältig ab.</p>"
         + liste(["Wände und Decken streichen", "Türen, Heizkörper und Fensterrahmen lackieren", "Wände spachteln bis zur glatten Oberfläche (Qualitätsstufen Q3 und Q4)"])),
        ("tapezieren", "leistung-tapezieren.webp", "Maler bringt eine Bahn Vliestapete an", "Tapezieren",
         "<p>Ob klassisch oder mit Muster: Wir tapezieren sauber auf Stoß und kümmern uns auch um den unbeliebtesten Teil, das Entfernen der alten Tapete.</p>"
         + liste(["Raufaser", "Vliestapeten", "Mustertapeten", "Alte Tapeten entfernen und Untergrund vorbereiten"])),
        ("fassade", "leistung-fassade.webp", "Klinkerfassade wird mit dem Hochdruckreiniger gereinigt", "Fassade",
         "<p>Eine gepflegte Fassade schützt Ihr Haus und macht es wieder zu einem Hingucker. Mit unserem eigenen Gerüst können wir flexibel planen und schnell beginnen.</p>"
         + liste(["Fassade reinigen, mit Hochdruck oder schonend chemisch", "Risse ausbessern", "Fassadenanstrich", "Klinker reinigen und imprägnieren", "Fachwerk aufarbeiten und lasieren"])),
        ("boden", "leistung-boden.webp", "Handwerker verlegt Designboden in Holzoptik", "Bodenbeläge",
         "<p>Ein neuer Boden passt oft perfekt zum frisch gestrichenen Raum. Wir verlegen:</p>"
         + liste(["Vinyl und Designboden", "Laminat", "Teppichboden"])
         + '<p class="hinweis">Fliesenarbeiten führen wir nicht aus. Gern nennen wir Ihnen einen zuverlässigen Fachbetrieb.</p>'),
        ("daemmung", "leistung-daemmung.webp", "Dämmplatten werden an einer Hauswand angebracht", "Wärmedämmung",
         "<p>Eine gedämmte Fassade spart Heizkosten und wertet Ihr Haus auf. Wir dämmen mit einem Wärmedämmverbundsystem (WDVS) und gestalten die Fassade danach ganz nach Ihren Wünschen.</p>"
         "<p>Zu Fördermöglichkeiten geben wir Ihnen gern einen ersten Überblick. Für die Förderung selbst arbeiten wir eng mit der Energieberatung Wessels aus Bersenbrück zusammen.</p>"),
    ]
    marken = "".join(f'<a href="#{a}">{t}</a>' for a, _, _, t, _ in bloecke)
    teile = ""
    for i, (anker, img, alt, titel, text) in enumerate(bloecke):
        um = " zweispaltig--umgekehrt" if i % 2 else ""
        teile += f'''<article class="leistung zweispaltig{um}" id="{anker}">
  <div><h2>{titel}</h2>{text}</div>
  {bild(img, alt, 1200, 900, cls="bild-rund")}
</article>'''
    inhalt = f'''<section class="seitenkopf">
  <div class="container">
    <h1>Unsere Leistungen</h1>
    <p>Vom einzelnen Zimmer bis zur kompletten Fassade: Alles kommt bei uns aus einer Hand und von unserem eigenen Team.</p>
    <nav class="sprungmarken" aria-label="Leistungen auf dieser Seite">{marken}</nav>
  </div>
</section>
<section class="abschnitt"><div class="container">{teile}</div></section>
{aufruf_band("Kostenlose Besichtigung vor Ort", "Erzählen Sie uns, was Sie vorhaben. Wir kommen kostenlos zu Ihnen, schauen uns alles in Ruhe an und machen Ihnen danach ein Angebot.")}'''
    seite("leistungen.html", "/leistungen", "Leistungen | Malerbetrieb Kötter Ankum",
          "Streichen, Lackieren, Spachteln, Tapezieren, Fassadensanierung, Bodenbeläge und Wärmedämmung vom Meisterbetrieb aus Ankum. Kostenlose Besichtigung vor Ort.", inhalt)


# ------------------------------------------------------------------ Über uns
def ueber_uns():
    team = [
        ("team-jens.webp", "Jens Kötter", "Malermeister und Inhaber", "Seit 1998 im Betrieb, seit 2015 am Steuer. Am liebsten steht er vor einer alten Fassade, die wieder strahlen soll."),
        ("team-sabine.webp", "Sabine Kötter", "Büro", "Ihre erste Ansprechpartnerin am Telefon. Sie plant Termine, schreibt Angebote und behält den Überblick."),
        (None, "Dieter", "Geselle", "Seit 1991 dabei, schon zur Zeit von Heinz Kötter. Unser Spezialist für Altbau und Stuck, wenn es knifflig wird."),
        ("team-marco.webp", "Marco", "Geselle", "Seit 2017 bei uns und hier ausgebildet. Er macht am liebsten Fassaden und ist unser Mann fürs Gerüst."),
        ("team-timo.webp", "Timo", "Geselle", "Seit 2020 dabei und unser Bodenleger. Vinyl und Designboden sind sein Fachgebiet."),
        ("team-pawel.webp", "Pawel", "Geselle", "Seit Oktober im Team. Er kommt aus einem großen Betrieb in Osnabrück und wollte, in seinen Worten, „endlich wieder abends zu Hause sein“."),
        ("team-lukas.webp", "Lukas", "Auszubildender", "Im vergangenen Jahr Innungsbester bei der Zwischenprüfung."),
    ]
    karten = ""
    for img, name, rolle, text in team:
        if img:
            foto = bild(img, f"{name}, {rolle}", 432, 540)
        else:
            foto = f'<div class="person__ohne" role="img" aria-label="{name}, ohne Foto">{name[0]}</div>'
        karten += (f'<figure class="person"><div class="person__bild">{foto}</div>'
                   f'<figcaption><strong>{name}</strong><span class="rolle">{rolle}</span><p>{text}</p></figcaption></figure>')
    werte = [
        ("kalender", "Verlässliche Termine", "Wenn wir einen Tag zusagen, stehen wir an diesem Tag bei Ihnen vor der Tür."),
        ("team", "Eigene Leute", "Bei uns arbeiten keine wechselnden Subunternehmer, sondern Mitarbeiter, die wir selbst ausgebildet oder lange im Team haben."),
        ("haken", "Sauberes Arbeiten", "Wir rücken Ihre Möbel zusammen und decken alles mit Folie ab, auf den Boden kommt Malervlies. Abends wird gefegt, und zum Schluss saugen wir durch. Sie bekommen Ihr Zuhause besenrein zurück."),
        ("ort", "Kurze Wege", "Wir sind aus der Region und für die Region da."),
    ]
    werte_html = "".join(f'<div class="wert"><h3>{icon(i)}{t}</h3><p>{x}</p></div>' for i, t, x in werte)
    inhalt = f'''<section class="seitenkopf">
  <div class="container">
    <h1>Ein Familienbetrieb mit Geschichte</h1>
    <p>Meisterbetrieb in zweiter Generation, mit festem Team aus Ankum.</p>
  </div>
</section>
<section class="abschnitt">
  <div class="container zweispaltig">
    <div>
      <p>1987 hat sich Heinz Kötter mit einem Gesellen und einem alten VW-Bus selbstständig gemacht. Sein Sohn Jens hat 1998 im Betrieb gelernt, 2008 seinen Meister gemacht und den Betrieb 2015 übernommen. Der Senior schaut heute noch ab und zu vorbei und guckt, ob alles richtig gemacht wird.</p>
      <p>Aus dem kleinen Betrieb ist ein festes Team geworden: vier Gesellen, zwei Auszubildende und Sabine Kötter, die im Büro alle Fäden in der Hand hält.</p>
      <ol class="zeitleiste">
        <li><strong>1987</strong>Heinz Kötter gründet den Betrieb, mit einem Gesellen und einem VW-Bus.</li>
        <li><strong>1998</strong>Jens Kötter beginnt seine Ausbildung im Betrieb.</li>
        <li><strong>2008</strong>Jens Kötter macht seinen Meister.</li>
        <li><strong>2015</strong>Übergabe an die zweite Generation.</li>
        <li><strong>Heute</strong>Sieben Leute, ein eigenes Gerüst und Kunden in der ganzen Region.</li>
      </ol>
    </div>
    {bild("firmenwagen.webp", "Firmenwagen des Malerbetriebs Kötter", 1200, 800, cls="bild-rund")}
  </div>
</section>
<section class="abschnitt abschnitt--grau">
  <div class="container">
    <div class="kopf-abschnitt"><span class="dachzeile">Was uns wichtig ist</span><h2>Darauf können Sie sich verlassen</h2></div>
    <div class="werte">{werte_html}</div>
  </div>
</section>
<section class="abschnitt">
  <div class="container">
    <div class="kopf-abschnitt"><span class="dachzeile">Unser Team</span><h2>Die Leute hinter dem Pinsel</h2></div>
    <div class="team">{karten}</div>
  </div>
</section>
<section class="abschnitt abschnitt--grau">
  <div class="container">
    <div class="kopf-abschnitt"><span class="dachzeile">Kundenstimmen</span><h2>Was unsere Kunden sagen</h2></div>
    {STIMMEN}
  </div>
</section>
{aufruf_band("Lernen Sie uns persönlich kennen", "Wir kommen kostenlos zu Ihnen und schauen uns Ihr Vorhaben an.")}'''
    seite("ueber-uns.html", "/ueber-uns", "Über uns | Familienbetrieb Kötter seit 1987",
          "Der Malerbetrieb Kötter aus Ankum: Meisterbetrieb in zweiter Generation mit festem Team aus Gesellen und Azubis.", inhalt)


# ------------------------------------------------------------------ Referenzen
def referenzen():
    galerie = [
        ("fassade", "nachher-haus.webp", "Einfamilienhaus mit frisch gestrichener Fassade", 1400, 933),
        ("fassade", "galerie-fassade-streichen.webp", "Fassadenanstrich vom eigenen Gerüst aus", 1200, 675),
        ("fassade", "referenz-fachwerk-nachher.webp", "Sanierte Fachwerkfassade in Alfhausen", 1200, 800),
        ("fassade", "leistung-fassade.webp", "Klinkerreinigung mit dem Hochdruckreiniger", 1200, 900),
        ("daemmung", "referenz-einfamilienhaus.webp", "Einfamilienhaus mit Wärmedämmung und neuer Fassade", 1200, 800),
        ("daemmung", "leistung-daemmung.webp", "Anbringen der Dämmplatten", 1200, 900),
        ("innen", "leistung-innen.webp", "Frisch gestrichenes Wohnzimmer", 1200, 900),
        ("innen", "referenz-treppenhaus.webp", "Renoviertes Treppenhaus in Quakenbrück", 1200, 800),
        ("tapete", "leistung-tapezieren.webp", "Vliestapete mit dezentem Muster", 1200, 900),
        ("boden", "leistung-boden.webp", "Neu verlegter Designboden in Holzoptik", 1200, 900),
    ]
    items = "".join(
        f'<li data-art="{art}"><button type="button" data-gross="/assets/img/{img}">{bild(img, alt, w, h)}</button></li>'
        for art, img, alt, w, h in galerie)
    filter_knoepfe = "".join(
        f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k == "alle" else "false"}">{t}</button>'
        for k, t in [("alle", "Alle"), ("innen", "Innen"), ("tapete", "Tapete"), ("fassade", "Fassade"), ("boden", "Boden"), ("daemmung", "Dämmung")])
    inhalt = f'''<section class="seitenkopf">
  <div class="container">
    <h1>Unsere Arbeiten</h1>
    <p>Eine Auswahl unserer Projekte aus der Region, viele davon im direkten Vorher-nachher-Vergleich.</p>
  </div>
</section>
<section class="abschnitt">
  <div class="container">
    <article class="projekt zweispaltig">
      <div>
        <div class="projekt__daten"><span class="marke">Alfhausen</span><span class="marke">Fassade</span><span class="marke">3 Wochen</span></div>
        <h2>Bauernhaus mit Fachwerk</h2>
        <p>Die Fachwerkfassade hat einen kompletten neuen Anstrich bekommen. Die Holzbalken haben wir abgeschliffen und neu lasiert, damit sie wieder geschützt sind und ihre Farbe zeigen.</p>
      </div>
      <div class="paar">
        <figure>{bild("referenz-fachwerk-vorher.webp", "Bauernhaus vorher: verwitterte Balken und abblätternde Farbe", 1200, 800)}<span class="vn__etikett vn__etikett--vorher">Vorher</span></figure>
        <figure>{bild("referenz-fachwerk-nachher.webp", "Bauernhaus nachher: lasierte Balken und weiße Gefache", 1200, 800)}<span class="vn__etikett vn__etikett--nachher">Nachher</span></figure>
      </div>
    </article>
    <article class="projekt zweispaltig zweispaltig--umgekehrt">
      <div>
        <div class="projekt__daten"><span class="marke">Quakenbrück</span><span class="marke">Innen</span><span class="marke">Boden</span></div>
        <h2>Sechs Treppenhäuser für eine Hausverwaltung</h2>
        <p>In einem Mehrfamilienhaus haben wir alle sechs Treppenhäuser erneuert: Wände gestrichen, Geländer lackiert, neue Böden verlegt. Und das, während alle Mieter weiter dort gewohnt haben.</p>
      </div>
      {bild("referenz-treppenhaus.webp", "Renoviertes Treppenhaus mit lackiertem Geländer", 1200, 800, cls="bild-rund")}
    </article>
    <article class="projekt zweispaltig">
      <div>
        <div class="projekt__daten"><span class="marke">Ankum</span><span class="marke">Wärmedämmung</span><span class="marke">Fassade</span></div>
        <h2>Einfamilienhaus mit neuer Dämmung</h2>
        <p>Wärmedämmung mit WDVS und eine neue Fassade in Anthrazit und Weiß. Die Familie berichtet, dass ihre Heizkosten seitdem um fast ein Drittel gesunken sind.</p>
      </div>
      {bild("referenz-einfamilienhaus.webp", "Einfamilienhaus mit neuer Fassade in Weiß und Anthrazit", 1200, 800, cls="bild-rund")}
    </article>
  </div>
</section>
<section class="abschnitt abschnitt--grau">
  <div class="container">
    <div class="kopf-abschnitt"><span class="dachzeile">Galerie</span><h2>Mehr aus unserer Arbeit</h2></div>
    <div class="filter" role="group" aria-label="Galerie filtern">{filter_knoepfe}</div>
    <ul class="galerie" style="list-style:none;padding:0;margin:0">{items}</ul>
  </div>
</section>
<dialog class="lightbox" aria-label="Großansicht">
  <button class="lightbox__zu" type="button" aria-label="Schließen">×</button>
  <img src="" alt="">
  <p></p>
</dialog>
{aufruf_band("Ihr Haus könnte das nächste sein.", "Wir kommen kostenlos vorbei und sehen uns alles an.", anfrage_text="Kostenlose Besichtigung anfragen")}'''
    seite("referenzen.html", "/referenzen", "Referenzen und Vorher-nachher-Bilder | Malerbetrieb Kötter",
          "Fassaden, Treppenhäuser und Wärmedämmung aus Ankum und Umgebung: Projekte des Malerbetriebs Kötter mit Vorher-nachher-Bildern.", inhalt)


# ------------------------------------------------------------------ Formulare
def formular(art):
    bewerbung = art == "bewerbung"
    if bewerbung:
        auswahl = ["Ausbildung Maler und Lackierer", "Geselle Maler und Lackierer", "Initiativbewerbung"]
        auswahl_label, nachricht_label, ort_label = "Worum geht es?", "Erzählen Sie kurz etwas über sich", "Wohnort"
        danke = "Danke für Ihre Bewerbung! Wir melden uns innerhalb von zwei Werktagen bei Ihnen."
        knopf = "Bewerbung senden"
    else:
        auswahl = ["Innenarbeiten", "Tapezieren", "Fassade", "Boden", "Wärmedämmung", "Sonstiges"]
        auswahl_label, nachricht_label, ort_label = "Worum geht es?", "Ihre Nachricht", "Ort"
        danke = "Danke für Ihre Anfrage! Wir melden uns innerhalb von zwei Werktagen bei Ihnen."
        knopf = "Anfrage senden"
    optionen = '<option value="">Bitte wählen</option>' + "".join(f"<option>{o}</option>" for o in auswahl)
    p = "b-" if bewerbung else "k-"
    return f'''<form class="formular" id="formular" action="/send.php" method="post" data-formular data-danke="{danke}">
  <input type="hidden" name="art" value="{art}">
  <input type="hidden" name="t" value="">
  <div class="honig" aria-hidden="true"><label for="{p}website">Bitte leer lassen</label><input id="{p}website" name="website" tabindex="-1" autocomplete="off"></div>
  <div class="felder-2">
    <div class="feld"><label for="{p}name">Name</label><input id="{p}name" name="name" autocomplete="name" required></div>
    <div class="feld"><label for="{p}telefon">Telefon <span class="optional">(optional)</span></label><input id="{p}telefon" name="telefon" type="tel" autocomplete="tel"></div>
  </div>
  <div class="felder-2">
    <div class="feld"><label for="{p}email">E-Mail</label><input id="{p}email" name="email" type="email" autocomplete="email" required></div>
    <div class="feld"><label for="{p}ort">{ort_label} <span class="optional">(optional)</span></label><input id="{p}ort" name="ort" autocomplete="address-level2"></div>
  </div>
  <div class="feld"><label for="{p}vorhaben">{auswahl_label}</label><select id="{p}vorhaben" name="vorhaben">{optionen}</select></div>
  <div class="feld"><label for="{p}nachricht">{nachricht_label}</label><textarea id="{p}nachricht" name="nachricht" required></textarea></div>
  <label class="check"><input type="checkbox" name="datenschutz" value="ja" required><span>Ich bin einverstanden, dass meine Angaben zur Bearbeitung meiner Anfrage verwendet werden. Mehr dazu in der <a href="/datenschutz">Datenschutzerklärung</a>.</span></label>
  <button class="knopf knopf--blau" type="submit">{knopf}</button>
  <p class="meldung" role="status" tabindex="-1" hidden></p>
</form>'''


# ------------------------------------------------------------------ Karriere
def karriere():
    vorteile = [
        ("haus", "Keine Montage", "Wir arbeiten nur in der Region, jeder ist abends zu Hause."),
        ("uhr", "Freitags um 13 Uhr Feierabend", "Sonst 7 bis 16 Uhr."),
        ("euro", "Bezahlung über Tarif", "Wir zahlen mehr als den Tariflohn im Malerhandwerk."),
        ("werkzeug", "Kleidung und Werkzeug", "Arbeitskleidung und Werkzeug stellen wir."),
        ("meister", "Weiterbildung zum Meister", "Wir unterstützen Sie dabei, wie schon zwei Kollegen vor Ihnen."),
        ("sonne", "Ein festes Team", "Familienbetrieb mit festen Kollegen, und im Sommer wird gegrillt."),
    ]
    v_html = "".join(f'<div class="vorteil">{icon(i)}<div><strong>{t}</strong><span>{x}</span></div></div>' for i, t, x in vorteile)
    inhalt = f'''<section class="hero">
  {bild("karriere-ausbildung.webp", "Geselle zeigt einem Auszubildenden, wie man eine Kante sauber streicht", 1200, 800, cls="hero__bild", lazy=False, prio=True)}
  <div class="container">
    <div class="hero__inhalt">
      <span class="dachzeile">Karriere</span>
      <h1>Arbeiten bei Kötter</h1>
      <p>Abends zu Hause, freitags früh ins Wochenende und ein Team, auf das man sich verlassen kann. Wir suchen Verstärkung.</p>
      <div class="knoepfe">
        <a class="knopf knopf--gelb" href="#stellen">Offene Stellen ansehen</a>
        <a class="knopf knopf--hell" href="{WA_LINK}" target="_blank" rel="noopener">{icon("whatsapp")}Per WhatsApp bewerben</a>
      </div>
    </div>
  </div>
</section>
<section class="abschnitt abschnitt--blau">
  <div class="container">
    <div class="kopf-abschnitt"><span class="dachzeile">Das bieten wir</span><h2>Darum lohnt es sich bei uns</h2></div>
    <div class="vorteile">{v_html}</div>
    <figure class="zitat-gross"><blockquote>„Ich wollte endlich wieder abends zu Hause sein.“</blockquote><figcaption>Pawel, Geselle, seit Oktober bei uns</figcaption></figure>
  </div>
</section>
<section class="abschnitt" id="stellen">
  <div class="container">
    <div class="kopf-abschnitt"><span class="dachzeile">Offene Stellen</span><h2>Wen wir suchen</h2></div>
    <div class="stellen">
      <article class="stelle">
        <span class="stelle__start">Start: 1. August</span>
        <h3>Ausbildung zum Maler und Lackierer (m/w/d)</h3>
        <p>Bei uns lernen Sie das Handwerk von Grund auf, auf echten Baustellen und mit erfahrenen Gesellen an Ihrer Seite. Wie gut das klappt, zeigt unser Azubi Lukas, der im vergangenen Jahr Innungsbester bei der Zwischenprüfung wurde.</p>
        <p><strong>Was Sie mitbringen sollten:</strong> einen Hauptschulabschluss, Freude an handwerklicher Arbeit, Zuverlässigkeit und Lust, im Team anzupacken. Einen Führerschein brauchen Sie nicht.</p>
      </article>
      <article class="stelle">
        <span class="stelle__start">Ab sofort</span>
        <h3>Geselle Maler und Lackierer (m/w/d)</h3>
        <p>Sie haben Ihre Ausbildung abgeschlossen und suchen einen Betrieb, in dem Sie sich wohlfühlen? Erfahrung mit Fassaden und Wärmedämmung (WDVS) ist ein Plus, aber kein Muss.</p>
      </article>
    </div>
  </div>
</section>
<section class="abschnitt abschnitt--grau">
  <div class="container kontakt-raster">
    <div>
      <span class="dachzeile">Bewerben</span>
      <h2>So bewerben Sie sich</h2>
      <p>Ganz unkompliziert: Rufen Sie an, schreiben Sie uns auf WhatsApp oder schicken Sie ein paar Zeilen über das Formular. Ein Lebenslauf reicht, ein langes Anschreiben brauchen wir nicht.</p>
      <p>Ihren Lebenslauf können Sie uns per E-Mail an <a href="mailto:{MAIL}">{MAIL}</a> oder per WhatsApp schicken.</p>
      <div class="knoepfe">
        <a class="knopf knopf--gelb" href="{TEL_LINK}">{icon("telefon")}Jetzt anrufen</a>
        <a class="knopf knopf--wa" href="{WA_LINK}" target="_blank" rel="noopener">{icon("whatsapp")}Per WhatsApp bewerben</a>
      </div>
    </div>
    {formular("bewerbung")}
  </div>
</section>'''
    seite("karriere.html", "/karriere", "Jobs und Ausbildung | Malerbetrieb Kötter Ankum",
          "Ausbildung zum Maler und Lackierer ab 1. August und Gesellen gesucht. Über Tarif, keine Montage, freitags um 13 Uhr Feierabend.", inhalt)


# ------------------------------------------------------------------ Kontakt
def kontakt():
    inhalt = f'''<section class="seitenkopf">
  <div class="container">
    <h1>So erreichen Sie uns</h1>
    <p>Rufen Sie an, schreiben Sie uns oder nutzen Sie das Formular. Die Besichtigung vor Ort ist kostenlos.</p>
  </div>
</section>
<section class="abschnitt">
  <div class="container kontakt-raster">
    <div>
      <ul class="kontakt-liste">
        <li>{icon("ort")}<div><strong>Malerbetrieb Kötter</strong><span>Inhaber Jens Kötter<br>Hauptstraße 41<br>49577 Ankum</span></div></li>
        <li>{icon("telefon")}<div><strong>Telefon Büro</strong><a href="{TEL_LINK}">{TEL_ANZEIGE}</a><br><span>Montag bis Freitag, 8 bis 12 Uhr. Nachmittags hinterlassen Sie gern eine Nachricht auf dem Anrufbeantworter, wir rufen zurück.</span></div></li>
        <li>{icon("whatsapp")}<div><strong>WhatsApp</strong><a href="{WA_LINK}" target="_blank" rel="noopener">{WA_ANZEIGE}</a><br><span>Wir antworten in der Regel abends bis 20 Uhr, am Wochenende am nächsten Werktag.</span></div></li>
        <li>{icon("mail")}<div><strong>E-Mail</strong><a href="mailto:{MAIL}">{MAIL}</a></div></li>
        <li>{icon("uhr")}<div><strong>Wochenende</strong><span>Samstags und sonntags ist geschlossen.</span></div></li>
      </ul>
    </div>
    <div>
      <h2>Schreiben Sie uns</h2>
      <p>Beschreiben Sie kurz Ihr Vorhaben. Wir melden uns innerhalb von zwei Werktagen und vereinbaren gern einen kostenlosen Besichtigungstermin.</p>
      {formular("anfrage")}
    </div>
  </div>
</section>
<section class="abschnitt abschnitt--grau">
  <div class="container">
    <div class="kopf-abschnitt"><span class="dachzeile">Anfahrt</span><h2>So finden Sie uns</h2></div>
    <div class="karte" data-src="{OSM}">
      <div class="karte__hinweis">
        <p>Die Karte wird erst geladen, wenn Sie auf „Karte anzeigen“ klicken. Dabei werden Daten an OpenStreetMap übertragen.</p>
        <div class="knoepfe">
          <button class="knopf knopf--blau" type="button" data-karte-laden>Karte anzeigen</button>
          <a class="knopf knopf--rand" href="{ROUTE}" target="_blank" rel="noopener">{icon("route")}Route planen</a>
        </div>
      </div>
    </div>
    <p style="margin-top:12px;font-size:.88rem;color:var(--grau)">Kartendaten © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap-Mitwirkende</a></p>
  </div>
</section>'''
    seite("kontakt.html", "/kontakt", "Kontakt | Malerbetrieb Kötter Ankum",
          "Malerbetrieb Kötter, Hauptstraße 41, 49577 Ankum. Telefon 05462 00000, Büro Montag bis Freitag 8 bis 12 Uhr. Kostenlose Besichtigung vor Ort.", inhalt)


# ------------------------------------------------------------------ Rechtliches und 404
def rechtstext(datei, pfad, titel, h1, hinweis):
    inhalt = f'''<section class="seitenkopf"><div class="container"><h1>{h1}</h1></div></section>
<section class="abschnitt"><div class="container rechtstext">
  <div class="platzhalter-kasten">
    <h2 style="margin-top:0">Platzhalter</h2>
    <p>{hinweis}</p>
  </div>
</div></section>'''
    head = '<meta name="robots" content="noindex, follow">' if datei == "datenschutz.html" else ""
    seite(datei, pfad, titel, f"{h1} des Malerbetriebs Kötter, Ankum.", inhalt, head)


def fehlerseite():
    inhalt = f'''<section class="abschnitt"><div class="container" style="text-align:center">
  <p class="dachzeile">Fehler 404</p>
  <h1>Diese Seite gibt es leider nicht</h1>
  <p style="margin-inline:auto">Vielleicht hat sich die Adresse geändert. Von der Startseite aus finden Sie alles.</p>
  <div class="knoepfe" style="justify-content:center"><a class="knopf knopf--blau" href="/">Zur Startseite</a><a class="knopf knopf--rand" href="/kontakt">Kontakt</a></div>
</div></section>'''
    seite("404.html", "/404", "Seite nicht gefunden | Malerbetrieb Kötter", "Diese Seite gibt es leider nicht.", inhalt,
          '<meta name="robots" content="noindex">')


def sitemap():
    seiten = ["/", "/leistungen", "/ueber-uns", "/referenzen", "/karriere", "/kontakt", "/impressum"]
    eintraege = "".join(f"  <url><loc>{DOMAIN}{s}</loc></url>\n" for s in seiten)
    with open(os.path.join(ZIEL, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + eintraege + "</urlset>\n")


if __name__ == "__main__":
    startseite()
    leistungen()
    ueber_uns()
    referenzen()
    karriere()
    kontakt()
    rechtstext("impressum.html", "/impressum", "Impressum | Malerbetrieb Kötter", "Impressum",
               "Hier wird das Impressum eingefügt, das Frau Kötter mit dem Generator erstellt hat. Sinner Webdesign erstellt keine Rechtstexte, sondern baut sie nur technisch ein.")
    rechtstext("datenschutz.html", "/datenschutz", "Datenschutzerklärung | Malerbetrieb Kötter", "Datenschutzerklärung",
               "Hier wird die Datenschutzerklärung eingefügt, die Frau Kötter mit dem Generator erstellt hat. Technisch genutzt werden: Hosting bei all-inkl, Kontakt- und Bewerbungsformular (Versand per E-Mail), WhatsApp-Link, OpenStreetMap-Karte erst nach Klick, Link zu Google Maps. Schriften werden nicht von Google geladen, es gibt keine Cookies und keine Statistik.")
    fehlerseite()
    sitemap()
    print("Fertig:", sorted(f for f in os.listdir(ZIEL) if f.endswith((".html", ".xml"))))
