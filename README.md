# Website Malerbetrieb Kötter

Übungsprojekt von Sinner Webdesign (Angebot 2027-001). Kunde und alle Daten sind ausgedacht.

## Ordner

| Ordner | Inhalt |
|---|---|
| `website/` | **Das wird hochgeladen** (per SFTP zu all-inkl). Fertige HTML-Seiten, Bilder, Formular. |
| `werkzeuge/` | Hilfsskripte, werden **nicht** hochgeladen. |
| `bilder-roh/` | Originalbilder in voller Größe, werden nicht hochgeladen und nicht in Git gespeichert. |

## Arbeiten am Projekt

Texte und Seiten ändern: in `werkzeuge/seiten_bauen.py` (Kopf, Menü und Fuß stehen dort nur einmal), danach:

```
python werkzeuge/seiten_bauen.py
```

Neue Bilder: in `bilder-roh/` legen, in `werkzeuge/bilder_umwandeln.py` bei `ZUORDNUNG` eintragen, dann:

```
python werkzeuge/bilder_umwandeln.py
```

Gestaltung: `website/assets/css/style.css`. Funktionen (Menü, Vorher-nachher-Regler, Galerie, Karte, Formular): `website/assets/js/main.js`.

Lokale Vorschau mit sauberen Adressen:

```
python werkzeuge/vorschau.py
```

Dann im Browser `http://localhost:8770` öffnen. Das Formular (PHP) funktioniert nur auf dem echten Webspace.

## Technik

- Reines HTML, CSS und JavaScript, kein Baukasten, keine Cookies, keine Statistik
- Schriften sind Systemschriften, es wird nichts von Google geladen
- Karte: OpenStreetMap, lädt erst nach Klick. „Route planen“ ist ein normaler Link zu Google Maps
- Formular: `website/send.php` schickt Anfragen und Bewerbungen an info@malerbetrieb-koetter.de. Schutz durch unsichtbares Feld, Zeitfalle und Begrenzung auf 5 Anfragen pro Stunde
- `.htaccess`: HTTPS-Umleitung, saubere Adressen ohne `.html`, Sicherheits-Header, Zwischenspeicher

## Noch offen vor dem Livegang

- [ ] Impressum und Datenschutzerklärung von Frau Kötter einfügen (`impressum.html`, `datenschutz.html`)
- [ ] Echte Telefon- und WhatsApp-Nummern statt der Platzhalter 05462 00000 und 0170 0000000
- [ ] Echte Fotos statt KI-Bilder (nur in der Übung erlaubt)
- [ ] Postfach info@malerbetrieb-koetter.de bei all-inkl anlegen, Formular einmal live testen
- [ ] Domain umziehen (Auth-Code vom Baukasten), danach Baukasten kündigen
- [ ] Google-Unternehmensprofil einrichten (Extra aus dem Angebot)
